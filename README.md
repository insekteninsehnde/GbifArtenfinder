# GBIF Artenfinder

Interaktive Karten-Oberfläche zur Suche von Artnachweisen (Biodiversitätsdaten) aus [GBIF](https://www.gbif.org) in einem frei wählbaren Gebiet. Das gesamte Programm ist **eine einzige HTML-Datei** (`GBIFArtenfinder.html`), die lokal im Browser läuft. Es gibt keine eigene Serverkomponente und keine Datenbank.

> **Wichtiger Hinweis zu diesem Dokument:** Die Abschnitte zu Lizenzen, Datenschutz und Nutzungsbedingungen (Kapitel 9) wurden nach bestem Wissen und anhand der zum Zeitpunkt der Erstellung (16.11.2026) öffentlich einsehbaren Bedingungen der Anbieter erstellt. Sie sind **keine Rechtsberatung** und können nicht garantieren, dass jede Nutzung rechtlich einwandfrei ist. Bedingungen ändern sich; maßgeblich sind immer die Originaltexte der Anbieter (Links in Kapitel 9). Bei Veröffentlichung, kommerzieller Nutzung oder Weitergabe personenbezogener Daten sollte eine fachkundige Rechtsprüfung erfolgen.

> **Zu den Abbildungen:** Die Bilder in diesem Dokument sind **Schemazeichnungen** (SVG), keine Bildschirmfotos. Sie zeigen Aufbau und Abläufe, nicht das exakte Aussehen. Eigene Screenshots können unter `docs/img/` ergänzt werden.

---

## Inhalt

1. [Funktionsumfang](#1-funktionsumfang)
2. [Voraussetzungen und Start](#2-voraussetzungen-und-start)
3. [Aufbau der Oberfläche](#3-aufbau-der-oberfläche)
4. [Suche Schritt für Schritt](#4-suche-schritt-für-schritt)
5. [Flächen: zeichnen, speichern, laden, Verwaltungsgrenzen](#5-flächen-zeichnen-speichern-laden-verwaltungsgrenzen)
6. [Filter, Raster, Karte](#6-filter-raster-karte)
7. [Ergebnisliste, Details, Phänologie, Export](#7-ergebnisliste-details-phänologie-export)
8. [Datenflüsse und optionaler Proxy](#8-datenflüsse-und-optionaler-proxy)
9. [Rechtliches: Lizenzen, Nutzungsbedingungen, Datenschutz](#9-rechtliches-lizenzen-nutzungsbedingungen-datenschutz)
10. [Bekannte Einschränkungen](#10-bekannte-einschränkungen)
11. [Änderungsübersicht](#11-änderungsübersicht)

---

## 1. Funktionsumfang

- Suche nach **Art oder Familie** (wissenschaftlicher oder deutscher Name, Autovervollständigung über GBIF).
- Suchgebiet als **Rechteck/Umkreis** (1–20 km Radius oder frei aufgezogen) oder als **frei gezeichnete Fläche** (Polygon mit verschiebbaren Ecken).
- **Flächen speichern und laden** als lokale GeoJSON-Datei (auch per Drag & Drop auf die Karte).
- **Verwaltungsgrenze** eines Ortes/einer Region optional anzeigen und als Suchfläche oder als gezeichnete, bearbeitbare Fläche übernehmen.
- Serverseitige **Filter**: Jahr, Jahreszeit, Aufnahmeart, nur mit Foto, Koordinatengenauigkeit.
- **TK25-Raster** (MTB, Quadrant, Minutenfeld) als dünne Linien mit Beschriftung.
- Karte mit **Marker-Clustering** und umschaltbaren Hintergrundkarten.
- Ergebnisliste mit Textfilter, Sortierung, MTB-Quadrant je Fund, optionalem Nachladen von Details, **Phänologie-Grafik** (Funde pro Kalenderwoche).
- Export: **CSV** und **GeoJSON**; **Link** zum Teilen der Suche; Sprung ins **GBIF-Portal** mit gleicher Suche.

![Schema der Oberfläche](docs/img/01-oberflaeche.svg)

---

## 2. Voraussetzungen und Start

| Punkt | Angabe |
|---|---|
| Browser | aktueller Desktop- oder Mobilbrowser (Chrome, Firefox, Edge, Safari) |
| Internet | **erforderlich** (GBIF, Kartenkacheln, Nominatim, CDN-Bibliotheken) |
| Installation | keine; Datei `GBIFArtenfinder.html` per Doppelklick öffnen |
| Optional | Python 3 für den lokalen Proxy (Kapitel 8) |

**Hinweis zu `file://`:** Wird die Datei direkt von der Festplatte geöffnet, senden Browser keinen Referer. Manche Dienste (insbesondere die OSM-Kachelserver und Nominatim) verlangen laut ihren Richtlinien eine Identifikation der Anwendung. Dadurch können Kacheln oder Ortssuche ausbleiben oder blockiert werden. Abhilfe: Datei über einen eigenen kleinen Webserver ausliefern (z. B. `python -m http.server`) oder eine eigene Kachel-/Geocoding-Quelle eintragen (siehe Kapitel 9.4).

---

## 3. Aufbau der Oberfläche

**Kopfbereich**

1. **Art oder Familie suchen** – Eingabe mit Vorschlägen; ein Klick auf einen Vorschlag setzt den Taxon-Schlüssel. Ohne Auswahl wird der Name bei GBIF abgeglichen.
2. **Ort suchen** – Ort, PLZ oder Region; „Ort finden“ setzt das Suchkästchen dorthin. Alternativ auf die Karte klicken.
3. **Kästchen-Radius** – 1, 2, 5, 10, 20 km Radius oder „Individuell gezogen“.
4. **Bei GBIF suchen** – startet die Suche.
5. **Verwaltungsgrenze** – Checkbox und zwei Übernahme-Buttons (Kapitel 5.4).
6. **Filterzeile** – Jahr, Monate, Aufnahmeart, Foto, Genauigkeit, MTB/Q/MF-Raster, Standort, Link, GBIF-Portal, GeoJSON.

**Kartenbereich** mit Modusleiste (`▭ Rechteck`, `⬠ Fläche zeichnen`, `✓ Schließen & suchen`, `↶ Punkt zurück`, `✕ Neu`, `💾 Fläche speichern`, `📂 Fläche laden`) und Ebenenwahl oben rechts (OpenStreetMap, Topografie, Satellit).

**Ergebnisbereich** mit Trefferzahl, Textfilter, Sortierung, „🔎 Details nachladen“, CSV-Download und der Phänologie-Grafik.

---

## 4. Suche Schritt für Schritt

1. **Art eingeben** (z. B. `Vanessa cardui`, `Pieridae`, `Weißlinge`, `Rotmilan`) und einen Vorschlag wählen.
2. **Ort eingeben** und „Ort finden“ klicken, oder auf die Karte klicken. Es erscheint ein Suchkästchen mit dem gewählten Radius.
3. Optional **Filter** setzen (Kapitel 6.1). Jede Filteränderung startet die Suche neu.
4. **Bei GBIF suchen** klicken. Der Fortschritt wird angezeigt; Treffer erscheinen als Marker bzw. Cluster und in der Liste.
5. Das Rechteck lässt sich an den Griffen ziehen („Individuell gezogen“).

Es werden höchstens **1.000 Funde pro Suche** geladen; die Anzeige nennt die Gesamtzahl bei GBIF. Bei größeren Treffermengen Gebiet verkleinern oder Zeitfilter nutzen.

---

## 5. Flächen: zeichnen, speichern, laden, Verwaltungsgrenzen

![Ablauf der Flächenfunktionen](docs/img/02-flaechen.svg)

### 5.1 Fläche zeichnen

1. `⬠ Fläche zeichnen` wählen.
2. Auf der Karte nacheinander Eckpunkte setzen. `↶ Punkt zurück` entfernt den letzten.
3. Mit mindestens drei Punkten auf den **Startpunkt** klicken oder `✓ Schließen & suchen`. Die Suche startet.
4. Nachbearbeiten: Ecke **ziehen** (Verschieben), **Rechtsklick** (Löschen, mindestens drei Ecken), kleinen **Kantenpunkt anklicken** (Ecke einfügen). Selbstüberschneidende Flächen werden von GBIF nicht akzeptiert.
5. `✕ Neu` verwirft die Fläche.

### 5.2 Fläche speichern

`💾 Fläche speichern` fragt nach einem Namen und lädt die Datei `<Name>.geojson.json` herunter. Sie liegt **nur lokal** auf deinem Rechner; die Anwendung sendet sie nirgendwohin.

### 5.3 Fläche laden

`📂 Fläche laden` öffnet einen Dateidialog; alternativ eine Datei **auf die Karte ziehen**. Akzeptiert werden GeoJSON-Dateien mit `Polygon` oder `MultiPolygon` (bei `FeatureCollection`: erstes Polygon; bei `MultiPolygon`: erster Teil). Die Fläche wird geladen, die Karte zoomt hin, die Suche startet.

Format (GeoJSON nach [RFC 7946](https://www.rfc-editor.org/rfc/rfc7946), Koordinaten als `[Länge, Breite]`):

```json
{
  "type": "FeatureCollection",
  "features": [{
    "type": "Feature",
    "properties": { "name": "Suchfläche", "saved": "2026-11-16T10:00:00.000Z" },
    "geometry": { "type": "Polygon", "coordinates": [[[9.96, 52.31], [10.02, 52.31], [10.02, 52.35], [9.96, 52.31]]] }
  }]
}
```

### 5.4 Verwaltungsgrenze

1. Im Ortsfeld einen Ort oder eine Region eingeben, **Verwaltungsgrenze anzeigen** aktivieren und „Ort finden“ bzw. Enter wählen.
2. Die Grenze erscheint violett gestrichelt (Quelle: OpenStreetMap über Nominatim; es wird der erste Treffer mit Flächengeometrie verwendet, bei mehrdeutigen Namen kann das ein falsches Gebiet sein – Zusatz wie „Sehnde, Niedersachsen“ hilft).
3. Zwei Übernahmearten:

| Button | Wirkung |
|---|---|
| **Als gezeichnete Fläche** | Vereinfachte Grenze (ca. 60 Ecken, größter Teil des Gebiets) wird zu einer normalen, **bearbeitbaren** Fläche. |
| **Als Suchfläche (exakte Grenze)** | Abfrage an GBIF mit vereinfachter Fläche (ca. 150 Ecken); angezeigt werden anschließend **nur Funde innerhalb der vollen, exakten Grenze** (alle Teilflächen). Das Bearbeiten einer Ecke hebt den exakten Filter auf. |

Grenzen der Genauigkeit: Durch die Vereinfachung kann ein schmaler Randstreifen bei der GBIF-Abfrage fehlen; Löcher (Enklaven) werden nicht herausgerechnet.

---

## 6. Filter, Raster, Karte

### 6.1 Filter (serverseitig bei GBIF)

| Filter | GBIF-Parameter | Bedeutung |
|---|---|---|
| Jahr von/bis | `year` | Bereich, z. B. 2015–2025 |
| Monate | `month` | Frühling 3–5, Sommer 6–8, Herbst 9–11, Winter 12, 1, 2 |
| Aufnahmeart | `basisOfRecord` | Beobachtung, Maschinell, Präparat/Beleg, Literatur |
| nur mit Foto | `mediaType=StillImage` | nur Funde mit Bild |
| Genauigkeit ≤ 1 km | `coordinateUncertaintyInMeters=0,1000` | schließt ungenaue Koordinaten aus; Funde ohne Angabe können dadurch ebenfalls entfallen |

### 6.2 TK25-Raster (MTB / Quadrant / Minutenfeld)

![Aufbau des TK25-Rasters](docs/img/03-mtb-raster.svg)

Checkbox **MTB/Q/MF-Raster** zeichnet dünne Linien: MTB (6′ × 10′) ab Zoomstufe 8, Quadranten (3′ × 5′) ab 11, Minutenfelder (1′ × 1′) ab 13; Beschriftung ab Zoom 9/12/15. Die Rasterdefinition entspricht der MTB-Angabe in der Fundliste: Ursprung 55°54′ N / 5°50′ E, Blattnummer = Zeile von Nord + Spalte von West, Quadrant 1 = NW, 2 = NO, 3 = SW, 4 = SO, Minutenfeld 1–15 zeilenweise von NW. Zahlen sind **berechnet**, nicht amtlich geprüft; bei Unsicherheit mit der amtlichen TK25 abgleichen. Für Gebiete außerhalb des Rasters (Zeile/Spalte > 99) wird nichts angezeigt.

### 6.3 Karte

- **Cluster:** Nahe Marker werden zusammengefasst; Zoom löst sie auf.
- **Hintergrund:** OpenStreetMap, Topografie (OpenTopoMap), Satellit (Esri). Hinweise zu den Bedingungen in Kapitel 9.4.
- **📍 Mein Standort:** setzt ein Suchkästchen auf den Browser-Standort (Freigabe durch den Nutzer erforderlich).
- **🔗 Link kopieren:** schreibt Art, Gebiet (Rechteck oder Fläche) und Filter in den URL-Teil nach `#` und kopiert die Adresse. Beim Öffnen eines solchen Links wird die Suche wiederhergestellt. Bei lokalen Dateien enthält der Link den lokalen Pfad.
- **↗ GBIF-Portal:** öffnet gbif.org mit Taxon und Gebiet.

---

## 7. Ergebnisliste, Details, Phänologie, Export

- **Liste:** zeigt je Fund Art, Datum, Ort, Datensatz sowie MTB-Quadrant. Textfilter durchsucht u. a. Ortsteil, Quelle, Jahr. Sortierung: neueste/älteste, Fundort, Datenquelle.
- **🔎 Details nachladen:** für bis zu 50 aktuell gefilterte Funde werden Beobachter- und Ortsdetails über GBIF (`/verbatim`), Nominatim (Rückwärtssuche, gedrosselt auf ca. eine Anfrage je 1,1 s), die iNaturalist-API (bei iNaturalist-Nachweisen) und – nur mit aktiviertem Proxy – Nachweis-Seiten nachgeladen. **Dabei können personenbezogene Daten (Beobachternamen) entstehen**, siehe Kapitel 9.6.
- **Phänologie-Grafik:** Balkendiagramm der Funde je Kalenderwoche, alle Jahre zusammengefasst, nach Lebensstadium eingefärbt, soweit erkennbar. Die Höhe spiegelt auch die Beobachtungsintensität (viel Beobachter im Sommer), nicht allein die Häufigkeit der Art.
- **CSV:** u. a. Datensatz, Rechteinhaber, **Lizenz** je Fund. Diese Spalten sollten bei Weitergabe erhalten bleiben (Kapitel 9.3).
- **GeoJSON-Export:** alle Funde mit Koordinaten als Punkte; Eigenschaften einschließlich Lizenzfeld.

---

## 8. Datenflüsse und optionaler Proxy

![Datenflüsse](docs/img/04-datenfluss.svg)

Beim Laden der Seite und bei Nutzung werden Anfragen **direkt aus deinem Browser** an folgende Dienste gesendet; dabei wird jeweils deine IP-Adresse übermittelt:

| Dienst | Zweck | Gesendet (Auszug) |
|---|---|---|
| `api.gbif.org` | Artsuche, Funde, Namensabgleich, `/verbatim` | Suchbegriff, Taxon, Gebiet (Rechteck oder WKT-Polygon), Filter, Fund-ID |
| `nominatim.openstreetmap.org` | Ortssuche, Verwaltungsgrenze, Rückwärtssuche | Suchtext, Koordinaten einzelner Funde |
| Kartenkacheln (OSM, OpenTopoMap, Esri) | Hintergrundkarte | sichtbarer Kartenausschnitt (Kachelkoordinaten) |
| `api.inaturalist.org` | nur bei „Details nachladen“ und iNaturalist-Funden | Beobachtungsnummer |
| `unpkg.com`, `cdn.tailwindcss.com` | Leaflet, Cluster-Plugin, Tailwind | Standard-Webanfrage |
| `fonts.googleapis.com`, `fonts.gstatic.com` | Schriftart Inter | Standard-Webanfrage |

**Proxy (optional):** In den Einstellungen „Proxy für Nachweis-Seiten“ kann ein lokaler Proxy (Standard `http://127.0.0.1:8787`) eingetragen werden, um Nachweis-Seiten abzurufen, die der Browser wegen CORS nicht direkt laden darf; optional mit Headless-Browser (Playwright/Chromium). Das Skript `proxy_server.py` ist **nicht Bestandteil dieser Lieferung**. Ohne Proxy funktioniert alles andere. Einzige gespeicherte Einstellung: `localStorage`-Eintrag `gbifProxyPrefs` (URL, Haken). Zur rechtlichen Einordnung des automatisierten Seitenabrufs siehe Kapitel 9.7.

---

## 9. Rechtliches: Lizenzen, Nutzungsbedingungen, Datenschutz

Stand der Recherche: 16.11.2026. Keine Rechtsberatung.

### 9.1 Lizenz dieses Programms

`GBIFArtenfinder.html` enthält eigenen Programmcode sowie – per CDN nachgeladen, nicht eingebettet – Drittbibliotheken (9.2). **Eine Lizenz für den eigenen Code ist noch nicht festgelegt.** Ohne ausdrückliche Lizenz gilt das gesetzliche Urheberrecht (alle Rechte vorbehalten). Die Urheberin bzw. der Urheber muss entscheiden:

```
Lizenz des Programmcodes:  [HIER EINTRAGEN, z. B. MIT, EUPL-1.2, GPL-3.0-or-later oder "alle Rechte vorbehalten"]
Copyright (c) [Jahr] [Name]
```

Wird der Code unter einer Lizenz veröffentlicht, die eine `LICENSE`-Datei erwartet (z. B. MIT), diese Datei dem Projekt beilegen. Die gewählte Lizenz muss mit den Bedingungen der Drittbibliotheken vereinbar sein (alle unten genannten sind permissiv bzw. im Fall der Schrift/Karten nicht Teil des Codes).

### 9.2 Drittsoftware (Code)

| Komponente | Version | Lizenz | Urheberrechtsvermerk |
|---|---|---|---|
| [Leaflet](https://leafletjs.com) | 1.9.4 | BSD-2-Clause | © 2010–2023 Vladimir Agafonkin; © 2010–2011 CloudMade |
| [Leaflet.markercluster](https://github.com/Leaflet/Leaflet.markercluster) | 1.5.3 | MIT | © 2012 David Leaver |
| [Tailwind CSS](https://tailwindcss.com) (Play-CDN-Skript) | per CDN, unversioniert | MIT | © Tailwind Labs, Inc. |
| [Inter](https://rsms.me/inter/) (Schrift über Google Fonts) | per Google Fonts | SIL Open Font License 1.1 | © The Inter Project Authors |

Die Vermerke wurden aus dem Gedächtnis des Verfassers und öffentlichen Projektangaben übernommen; **vor einer Weitergabe bitte gegen die LICENSE-Dateien der jeweiligen Projekte prüfen**, insbesondere Jahreszahlen.

Da die Bibliotheken nur geladen und nicht in die Datei kopiert werden, besteht für diese Datei keine Pflicht, den Lizenztext mitzuliefern. **Wer die Bibliotheken in die Datei einbettet oder zusammen mit der Datei verteilt, muss Copyright-Hinweis und Lizenztext beilegen.** Zur Orientierung der Lizenztext von Leaflet (BSD-2-Clause):

```
BSD 2-Clause License

Copyright (c) 2010-2023, Vladimir Agafonkin
Copyright (c) 2010-2011, CloudMade
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this
   list of conditions and the following disclaimer in the documentation and/or
   other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
THE POSSIBILITY OF SUCH DAMAGE.
```

Für MIT-lizenzierte Komponenten gilt: Copyright-Vermerk und der MIT-Lizenztext müssen bei Weitergabe des Codes enthalten sein. Das Tailwind-Play-CDN-Skript ist laut Tailwind **nicht für den Produktivbetrieb gedacht**; für öffentliche Angebote CSS vorab kompilieren.

### 9.3 Fundmeldungen (GBIF-Daten)

- **Lizenz je Datensatz:** GBIF stellt Daten unter **CC0**, **CC BY** oder **CC BY-NC** bereit. Die Lizenz gilt für den jeweiligen Datensatz bzw. Fund und steht im Feld `license` (in der Anwendung als Spalte „Lizenz“ in CSV und GeoJSON). Es gibt **keine einheitliche Lizenz** für alle Ergebnisse.
- **Namensnennung (CC BY/CC BY-NC):** Datenherausgeber/Rechteinhaber angemessen nennen. Die Spalten „Datensatz“ und „Rechteinhaber“ im Export dienen dazu und sollten bei Weitergabe nicht entfernt werden.
- **Nicht-kommerziell (CC BY-NC):** Nutzung nur nicht-kommerziell. Die Abgrenzung ist nicht einheitlich; GBIF empfiehlt Nutzung nach Treu und Glauben und im Zweifel Rückfrage beim Datenherausgeber.
- **Data User Agreement:** Bei der Nutzung von GBIF-vermittelten Daten gilt das [GBIF Data User Agreement](https://www.gbif.org/terms/data-user): u. a. Herkunftsangaben bei Weitergabe beibehalten, Lizenzbedingungen der Datenherausgeber beachten (sie haben im Konfliktfall Vorrang), keine Störung der API, Nutzung auf eigenes Risiko, Gewähr für Datenqualität wird nicht übernommen.
- **Zitierung:** GBIF empfiehlt, die **empfohlene Zitierung** der Datensätze bzw. eines GBIF-Downloads mit DOI zu verwenden. Die Anwendung erzeugt **keine DOI-Zitierung**; wer für Publikationen zitieren muss, sollte die Suche im GBIF-Portal (Button „↗ GBIF-Portal“) als **GBIF-Download** erneut ausführen, um eine zitierfähige DOI zu erhalten.
- **Artnamen:** Die Namensvorschläge stammen aus der GBIF-Taxonomie (u. a. GBIF Backbone Taxonomy, CC BY 4.0, GBIF Secretariat) und der Suche über deutsche Trivialnamen.
- **Datenqualität:** Koordinaten und Bestimmungen sind unterschiedlich zuverlässig; Funde können fehlerhaft, ungenau oder generalisiert sein (z. B. Schutz sensibler Arten). Kein Anspruch auf Vollständigkeit.

### 9.4 Karten, Geocoding, Grenzen

**OpenStreetMap-Daten** stehen unter der **Open Database License (ODbL) 1.0**. Zwingend: Quellenangabe „© OpenStreetMap-Mitwirkende“ mit Link zu <https://www.openstreetmap.org/copyright> (in der Karte enthalten). Abgeleitete Datenbanken (z. B. gespeicherte Verwaltungsgrenzen, die du weitergibst) unterliegen den ODbL-Bedingungen (Namensnennung, Weitergabe unter gleichen Bedingungen). Die vom Programm gespeicherten Flächen können aus OSM-Grenzen abgeleitet sein; bei Weitergabe daher Quelle und ODbL nennen.

**OSM-Kacheln** (`tile.openstreetmap.org`): Es gilt die [Tile Usage Policy](https://operations.openstreetmap.org/policies/tiles/) (kein Massen-Download, Cache-Header beachten, bei Webseiten ein gültiger Referer). Die ausgelieferten Kacheln stehen laut OSM-Wiki unter CC BY-SA. Für Anwendungen mit vielen Nutzern oder Produktivbetrieb einen eigenen oder kommerziellen Kachelanbieter verwenden.

**OpenTopoMap:** Kartendaten © OpenStreetMap-Mitwirkende, SRTM; Kartendarstellung © OpenTopoMap, Lizenz **CC BY-SA 3.0**. Die Anwendung zeigt die verlangte Quellenangabe an. Es gilt fairer Gebrauch; keine Massenabrufe.

**Esri World Imagery (Satellit):** Dienst und Bilder unterliegen den Nutzungsbedingungen von Esri und den Bildanbietern (Quellenangabe: „Esri, Maxar, Earthstar Geographics, and the GIS User Community“). **Die Bedingungen für den Abruf der Kacheln ohne Esri-Konto bzw. API-Schlüssel wurden hier nicht abschließend geprüft.** Für Veröffentlichung oder kommerzielle Nutzung vorab die aktuellen Esri-Bedingungen prüfen oder die Ebene entfernen.

**Nominatim** (Ortssuche, Verwaltungsgrenzen, Rückwärtssuche): Der öffentliche Server ([Usage Policy](https://operations.osmfoundation.org/policies/nominatim/)) erlaubt höchstens **eine Anfrage pro Sekunde je Anwendung**, verlangt eine **gültige Referer- oder User-Agent-Angabe**, **Zwischenspeichern** wiederholter Anfragen, deutlich sichtbare Quellenangabe und untersagt Autocomplete und Massenabfragen. Der Ist-Zustand dieser Anwendung:

- Die Rückwärtssuche wird auf ca. 1,1 s getaktet.
- **Ortssuche und Grenzabruf sind nicht gedrosselt und nicht zwischengespeichert.**
- Ein Browser kann den User-Agent nicht anpassen; bei `file://` fehlt der Referer.

Für gelegentliche Einzelnutzung ist das in der Praxis meist unproblematisch, **für intensive oder öffentliche Nutzung ist es nicht regelkonform**. Dann eigene Nominatim-Instanz oder einen kommerziellen Anbieter einsetzen und die Adressen im Quelltext (`nominatim.openstreetmap.org`) ersetzen.

### 9.5 Schriftarten und CDN-Einbindung (Datenschutz)

Die Seite lädt Leaflet und Plugin von **unpkg.com**, Tailwind von **cdn.tailwindcss.com** und die Schrift von **Google Fonts**. Dabei wird die **IP-Adresse an diese Anbieter übermittelt**. Deutsche Gerichte haben die dynamische Einbindung von Google Fonts ohne Einwilligung teils als Datenschutzverstoß gewertet (z. B. LG München I, Urteil vom 20.01.2022, Az. 3 O 17493/20). Für private, lokale Nutzung ist das praktisch unkritisch; **für eine öffentliche Webseite sollten alle Ressourcen lokal gehostet werden** (Inter ist unter der SIL OFL 1.1 frei verwendbar).

### 9.6 Personenbezogene Daten

- **Beobachternamen** und ähnliche Angaben in Fundmeldungen (z. B. aus `/verbatim` oder der iNaturalist-API) sind **personenbezogene Daten** im Sinne der DSGVO. Sie werden im Browser angezeigt und können in den CSV-Export gelangen.
- Für **private oder wissenschaftliche Einzelnutzung** ist das üblicherweise unproblematisch. Wer solche Daten **veröffentlicht, weitergibt oder dauerhaft speichert**, braucht eine Rechtsgrundlage (Art. 6 DSGVO), muss Informationspflichten erfüllen und Betroffenenrechte beachten.
- Der **Standort-Button** fragt die Freigabe im Browser ab; der Standort wird nicht gespeichert, fließt aber als Suchgebiet in die Anfrage an GBIF und Nominatim.
- Die Anwendung selbst speichert **keine Nutzerdaten** außer dem lokalen Proxy-Eintrag (`localStorage`). Gespeicherte Flächen liegen nur in der von dir heruntergeladenen Datei.
- Bildrechte: Fotos von Funden (Medien) haben eigene Lizenzen (häufig CC BY-NC). Vor jeder Weitergabe oder Veröffentlichung von Bildern die Medienlizenz und die Urheberangabe prüfen; der Filter „nur mit Foto“ sagt nichts über die Lizenz aus.

### 9.7 iNaturalist und Nachweis-Seiten

- **iNaturalist-API:** Nutzung nach den iNaturalist-Nutzungsbedingungen; die API ist für die Anwendungsentwicklung, nicht für massenhaftes Abgreifen gedacht. Jede Beobachtung und jedes Foto behält die Lizenz der Urheberin bzw. des Urhebers (CC0, CC BY, CC BY-NC oder alle Rechte vorbehalten); Namensnennung beachten.
- **Automatisierter Abruf fremder Webseiten (Proxy)**, insbesondere von naturgucker/enjoynature.net: Er kann gegen die **Nutzungsbedingungen** der Seiten und gegebenenfalls gegen **Datenbankschutzrechte** (§§ 87a ff. UrhG) oder `robots.txt`-Vorgaben verstoßen. Vor Aktivierung des Proxys die Bedingungen der jeweiligen Seite prüfen und nur Einzelabrufe im Rahmen persönlicher Nutzung durchführen. Standardmäßig ist der Proxy **aus**.

### 9.8 Haftung und Gewährleistung

Das Programm wird **ohne Gewähr** bereitgestellt, soweit gesetzlich zulässig (keine Zusicherung der Richtigkeit, Vollständigkeit oder Eignung). Fundmeldungen sind nicht für naturschutzrechtliche Gutachten, Eingriffsplanungen oder Artenschutzprüfungen geeignet, ohne sie fachlich zu prüfen. Sensible Fundorte geschützter Arten nicht veröffentlichen.

### 9.9 Checkliste vor Weitergabe oder Veröffentlichung

- [ ] Lizenz für den eigenen Code festgelegt und `LICENSE` beigelegt
- [ ] Bibliotheken lokal gehostet (kein unpkg/Tailwind-CDN/Google Fonts) oder Datenschutzhinweis vorhanden
- [ ] Kachelquellen geprüft (OSM-Policy, Esri-Bedingungen) bzw. eigener Kachelserver
- [ ] Nominatim: eigene Instanz oder Drosselung/Cache ergänzt
- [ ] Exportierte Funde mit Lizenz-, Rechteinhaber- und Datensatzangabe weitergegeben; CC BY-NC beachtet
- [ ] GBIF-Download mit DOI für Publikationen erzeugt und zitiert
- [ ] Keine personenbezogenen Daten ohne Rechtsgrundlage veröffentlicht
- [ ] Impressum/Datenschutzerklärung bei öffentlicher Bereitstellung

---

## 10. Bekannte Einschränkungen

- Die Erweiterungen (Flächen speichern/laden, Verwaltungsgrenzen, Filter, Raster, Cluster, Hintergrundkarten, Link, Exporte) wurden **nicht in einem echten Browser getestet**; nur die Syntax des JavaScripts wurde geprüft. Fehler sind möglich.
- Höchstens 1.000 Funde je Suche; GBIF-Suche mit Polygon nur mit gültigen, nicht selbstüberschneidenden Flächen.
- Verwaltungsgrenze: vereinfacht, erster passender Nominatim-Treffer, nur größter Teil bei Mehrteilgebieten als Fläche, keine Löcher.
- MTB/Q/MF sind berechnet und nur im deutschen TK25-Rasterbereich definiert.
- Nicht enthalten: mehrere Arten gleichzeitig, Artenliste des Gebiets, Heatmap, Markerfarben nach Merkmal, Dark Mode, mobile Tab-Ansicht, Abbruch laufender Nominatim-Abfragen.
- `proxy_server.py` liegt nicht bei.

---

## 11. Änderungsübersicht

| Erweiterung | Kurzbeschreibung |
|---|---|
| Flächen speichern/laden | GeoJSON-Datei, Drag & Drop |
| Verwaltungsgrenze | Anzeige, Übernahme als gezeichnete Fläche oder als exakte Suchfläche |
| Filter | Jahr, Jahreszeit, Aufnahmeart, Foto, Genauigkeit (serverseitig) |
| MTB/Q/MF-Raster | dünne Linien und Beschriftung |
| Karte | Marker-Clustering, drei Hintergrundkarten |
| Teilen/Export | Link mit Suchstatus, GeoJSON, GBIF-Portal-Sprung, Standort |
| Stabilität | Abbruch veralteter Suchläufe |
| Quellenangaben | Attribution für OpenTopoMap und Esri ergänzt, OSM-Hinweis „-Mitwirkende“ |
