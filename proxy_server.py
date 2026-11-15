#!/usr/bin/env python3
"""
Lokaler Proxy für den GBIF Artenfinder
=======================================
Ruft Nachweis-Seiten (z. B. naturgucker / enjoynature.net) für die HTML-Datei ab und
umgeht damit die CORS-Sperre des Browsers. Optional wird die Seite in einem echten
Headless-Browser (Playwright/Chromium) ausgeführt, damit auch Seiten funktionieren,
die ihre Inhalte erst per JavaScript nachladen.

Start (Windows/Mac/Linux):
    python proxy_server.py

Für JavaScript-Seiten (empfohlen, einmalig installieren):
    pip install playwright
    python -m playwright install chromium

Optionen:
    python proxy_server.py --port 8787 --allow meinedomain.de --allow andere.org

Sicherheit:
  * Lauscht nur auf 127.0.0.1 (nur dein Rechner).
  * Ruft nur Hosts aus der Positivliste ab (kein offener Proxy).
  * Max. 1 Anfrage pro Sekunde je Host (höflich zu den Betreibern).
Bitte Nutzungsbedingungen der abgerufenen Seiten beachten; Beobachternamen sind
personenbezogene Daten.
"""
import argparse, json, sys, time, urllib.request, urllib.error
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

DEFAULT_ALLOWED = [
    "naturgucker.de", "enjoynature.net", "observation.org", "waarneming.nl",
    "observado.org", "ornitho.de", "inaturalist.org", "artenfinder.net",
    "ebird.org", "gbif.org",
]
UA = "Mozilla/5.0 (compatible; GBIF-Artenfinder-Proxy/1.0; +local)"
MIN_GAP = 1.0   # Sekunden zwischen Anfragen an denselben Host

allowed = list(DEFAULT_ALLOWED)
last_hit = {}
pw = None
browser = None
render_error = None


def host_allowed(host):
    host = (host or "").lower()
    return any(host == a or host.endswith("." + a) for a in allowed)


def polite_wait(host):
    gap = time.time() - last_hit.get(host, 0)
    if gap < MIN_GAP:
        time.sleep(MIN_GAP - gap)
    last_hit[host] = time.time()


def ensure_browser():
    """Startet Chromium beim ersten Bedarf (im selben Thread wie der Server)."""
    global pw, browser, render_error
    if browser or render_error:
        return browser
    try:
        from playwright.sync_api import sync_playwright
        pw = sync_playwright().start()
        browser = pw.chromium.launch(headless=True)
    except Exception as e:  # Playwright fehlt oder Chromium nicht installiert
        render_error = f"Playwright nicht verfügbar ({e.__class__.__name__}). " \
                       "Installation: pip install playwright && python -m playwright install chromium"
    return browser


def fetch_plain(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "de,en;q=0.7"})
    with urllib.request.urlopen(req, timeout=25) as r:
        raw = r.read(5_000_000)
        charset = r.headers.get_content_charset() or "utf-8"
        return {"status": r.status, "final_url": r.geturl(),
                "html": raw.decode(charset, errors="replace"), "text": "", "rendered": False}


def fetch_rendered(url):
    b = ensure_browser()
    if not b:
        raise RuntimeError(render_error or "Browser nicht verfügbar")
    ctx = b.new_context(user_agent=UA, locale="de-DE")
    page = ctx.new_page()
    try:
        resp = page.goto(url, wait_until="networkidle", timeout=40000)
        page.wait_for_timeout(1500)  # Nachladen (z. B. IntraWeb-Sitzung) abwarten
        return {"status": resp.status if resp else 0, "final_url": page.url,
                "html": page.content(), "text": page.inner_text("body"), "rendered": True}
    finally:
        ctx.close()


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Private-Network", "true")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Private-Network", "true")
        self.end_headers()

    def do_GET(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        if u.path == "/health":
            try:
                import playwright  # noqa: F401
                has_pw = True
            except ImportError:
                has_pw = False
            return self._send(200, {"ok": True, "playwright": has_pw, "allowed": allowed})
        if u.path != "/fetch":
            return self._send(404, {"error": "Unbekannter Pfad"})

        url = (q.get("url") or [""])[0]
        render = (q.get("render") or ["0"])[0] == "1"
        p = urlparse(url)
        if p.scheme not in ("http", "https") or not p.hostname:
            return self._send(400, {"error": "Ungültige URL"})
        if not host_allowed(p.hostname):
            return self._send(403, {"error": f"Host '{p.hostname}' nicht erlaubt. "
                                             f"Mit --allow {p.hostname} freigeben."})
        try:
            polite_wait(p.hostname)
            data = fetch_rendered(url) if render else fetch_plain(url)
            return self._send(200, data)
        except urllib.error.HTTPError as e:
            return self._send(200, {"error": f"HTTP {e.code} von {p.hostname}"})
        except Exception as e:
            return self._send(200, {"error": f"{e.__class__.__name__}: {e}"})

    def log_message(self, fmt, *args):
        sys.stderr.write("[proxy] " + (fmt % args) + "\n")


def main():
    ap = argparse.ArgumentParser(description="Lokaler Abruf-Proxy für den GBIF Artenfinder")
    ap.add_argument("--port", type=int, default=8787)
    ap.add_argument("--allow", action="append", default=[], help="zusätzlich erlaubte Domain")
    args = ap.parse_args()
    allowed.extend(a.lower() for a in args.allow)
    # Bewusst einzelner Thread: Playwright (sync) darf nur im Erzeuger-Thread laufen
    srv = HTTPServer(("127.0.0.1", args.port), Handler)
    print(f"Proxy läuft auf http://127.0.0.1:{args.port}  (beenden mit Strg+C)")
    print("Erlaubte Hosts:", ", ".join(allowed))
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        if browser: browser.close()
        if pw: pw.stop()


if __name__ == "__main__":
    main()
