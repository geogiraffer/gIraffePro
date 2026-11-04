# gIraffePro

**Grüne Infrastruktur in der Projektphase 0 sichtbar machen.**

Plugin-Version 1.0.7 · Dokumentation: 2. November 2026

[Homepage](https://giraffepro.de/) · [Quellcode](https://github.com/geogiraffer/gIraffePro/) · [Fehler melden](https://github.com/geogiraffer/gIraffePro/issues) · [Releases](https://github.com/geogiraffer/gIraffePro/releases)

> **English summary:** gIraffePro is a QGIS Processing plugin that supports early decisions on linear infrastructure projects. It filters existing environmental datasets and uses an adjustable three-level weighting scheme, configurable search areas and traffic-light maps to make potential environmental constraints visible to project managers and steering groups. It supports preliminary screening and does not replace a detailed environmental assessment.

## Zweck

gIraffePro unterstützt die überschlägige Einschätzung potenzieller Betroffenheiten grüner Infrastruktur bei linienförmigen Infrastrukturvorhaben. Das Plugin bereitet vorhandene naturschutzfachliche Daten auf und wertet sie entlang einer Projektachse innerhalb variabler Suchräume aus.

Bereits vor der vertieften Planung – in der **Projektphase 0** – werden wichtige räumliche Weichen gestellt. Logistik, Technik und Flächenmanagement priorisieren Flächen anhand ihrer jeweiligen Anforderungen. Umweltplanerischer Sachverstand ist zu diesem Zeitpunkt häufig noch nicht eingebunden. gIraffePro bereitet Umweltinformationen für Entscheidungstragende in Management und Projektsteuerung verständlich auf. So können Steuerungsgremien potenzielle Betroffenheiten frühzeitig in die Abwägung räumlicher Lösungsansätze einbeziehen und planerischen Risiken begegnen, bevor sich eine Planung verfestigt.

Das Vorbereitungswerkzeug enthält einen **Vorschlag für ein dreistufiges Gewichtungsschema**, das fachkundige Nutzende prüfen und an die Fragestellung anpassen können. Die anschließende Ampeldarstellung reduziert die Komplexität für einen schnellen Überblick; ein ergänzender Info-Layer erhält den Bezug zu den zugrunde liegenden Fachdaten.

Die Aussagekraft hängt von Datenumfang, Aktualität, Gewichtung und Puffereinstellungen ab. **Eine grüne Darstellung bestätigt keine Konfliktfreiheit.** Die Ergebnisse unterstützen eine erste Orientierung und ersetzen keine vertiefte umweltfachliche Prüfung oder fachrechtliche Zulassung.

## Voraussetzungen

- QGIS ab Version 3.40 laut Plugin-Metadaten.
- Aktivierte QGIS-Verarbeitung (Processing) und die verwendeten nativen QGIS-Algorithmen.
- Geeignete Punkt-, Linien- und Flächendaten sowie eine Projektachse als Linienlayer.
- Schreibbare Ausgabeordner; für das Hauptwerkzeug zusätzlich die abgefragten QGIS-Layerstile im QML-Format.
- Für Abstände in Metern geeignete und fachlich konsistente Koordinatenreferenzsysteme.

Die Python-Module verwenden QGIS/PyQGIS und die Python-Standardbibliothek; sie sind keine eigenständig ausführbaren Python-Skripte.

### Getestete Umgebung

Die dokumentierte Testumgebung ist **QGIS 3.44 unter Fedora Linux in einer Mamba-Umgebung**.

## Installation

1. Die fertige Plugin-ZIP aus einem [Release](https://github.com/geogiraffer/gIraffePro/releases) herunterladen, sofern dort bereitgestellt.
2. In QGIS **Erweiterungen → Erweiterungen verwalten und installieren → Aus ZIP installieren** öffnen.
3. Die ZIP auswählen, installieren und das Plugin aktivieren.
4. Bei einem Update QGIS anschließend neu starten, damit Provider und Algorithmen vollständig neu geladen werden.

In der ZIP muss direkt der Ordner `giraffePro/` mit `metadata.txt` und `__init__.py` liegen. Die ZIP muss vor der Installation nicht entpackt werden. Automatisch erzeugte GitHub-Quellcodearchive sind bei einer zusätzlichen Repository-Ordnerebene nicht direkt installierbar; verwende den ausdrücklich bereitgestellten Plugin-ZIP-Anhang eines Releases.

## Werkzeuge

Im Processing-Provider **gIraffePro** stehen zwei Gruppen bereit:

| Gruppe | Werkzeug | Aufgabe |
| --- | --- | --- |
| Vorbereitung | Fachdatenbewertung | Fachdaten bewerten und als GeoJSON speichern |
| Verarbeitung | Green Infrastructure fast filter and estimation Project (gIraffePro) | Bewertete Fachdaten im Suchraum verarbeiten und Ergebnisse erzeugen |

Beide Werkzeuge sind außerdem über das Plugin-Menü und eigene Toolbar-Schaltflächen erreichbar. 

### Optionale Fachdaten ab Version 1.0.7

Alle unterstützten Fachdaten-Eingaben sind in beiden Werkzeugen **optional**. Mindestens ein Fachdatensatz muss gewählt werden. Beispielsweise sind Läufe nur mit FFH, nur mit NSG oder nur mit punktuellen Naturdenkmalen möglich. Projektachse, Suchraum und Ausgabeangaben bleiben für das Hauptwerkzeug erforderlich. Bewertungs- und Pufferwerte einer ausgelassenen Eingabe werden nicht verwendet.

Nicht gewählte Fachdaten werden übersprungen: Sie erzeugen keine Vorbereitungsdateien und keine eigenen Info-Layer. Geometrievarianten einer Gruppe werden nur aus den tatsächlich vorhandenen Eingaben zusammengeführt. Fehlende Wertfelder und nicht lesbare, ausdrücklich angegebene Datenquellen führen zu einer verständlichen Fehlermeldung.

**Die Aussage gilt nur für die ausgewählten Eingangsdaten.** Nicht berücksichtigte Schutzbelange können nicht aus dem Ergebnis abgeleitet werden. Eine grüne Darstellung bestätigt keine Konfliktfreiheit. Die zusätzlichen §30-Biotop-Eingaben 12–14 des bisherigen Hauptdialogs werden weiterhin nicht ausgewertet.

### 1. Vorbereitung: Fachdatenbewertung

Das Werkzeug verarbeitet folgende elf Eingaben. Punkt-, Linien- und Flächenvarianten derselben Fachdatenart erhalten bewusst denselben Wertfeldnamen.

Die voreingestellten Werte von **1 bis 3** sind ein Vorschlag für ein Gewichtungsschema und keine allgemeingültige oder behördliche Einstufung. Fachkundige Nutzende können die Werte prüfen und anpassen. Das verwendete Schema und etwaige Änderungen sollten für die spätere Einordnung der Ergebnisse dokumentiert werden.

| Nr. | Fachdaten | Geometrie | Wertfeld |
| --- | --- | --- | --- |
| 1 | FFH-Gebiet (FFH) | Fläche | `Wert_FFH` |
| 2 | Landschaftsschutzgebiet (LSG) | Fläche | `Wert_LSG` |
| 3 | Landschaftsschutzgebiet (LSG) | Linie | `Wert_LSG` |
| 4 | Naturdenkmal (ND) | Punkt | `Wert_ND` |
| 5 | Naturdenkmal (ND) | Linie | `Wert_ND` |
| 6 | Naturdenkmal (ND) | Fläche | `Wert_ND` |
| 7 | Vogelschutzgebiet (SPA) | Fläche | `Wert_SPA` |
| 8 | Naturschutzgebiet (NSG) | Fläche | `Wert_NSG` |
| 9 | geschützte Landschaftsbestandteile (GLB) | Punkt | `Wert_GLB` |
| 10 | geschützte Landschaftsbestandteile (GLB)  | Linie | `Wert_GLB` |
| 11 | geschützte Landschaftsbestandteile (GLB)  | Fläche | `Wert_GLB` |

1. Einen oder mehrere Fachlayer auswählen; die übrigen Fachdaten-Eingaben leer lassen.
2. Das vorgeschlagene Gewichtungsschema fachlich prüfen und die Bewertung von **1 bis 3** je Datensatz bei Bedarf anpassen.
3. Bundesland-Kennung und Ausgabeordner angeben.
4. Werkzeug ausführen. Linien und Flächen durchlaufen vorher die Geometriereparatur; Punktdaten erhalten das Wertfeld direkt.

Die Ausgabe erfolgt je Fachdatenart als eigene GeoJSON-Datei, beispielsweise `gIraffePro_FFH_Ni.geojson`. Die Kennung `Ni` ergibt sich aus der Eingabe für das Bundesland. Vor einem erneuten Lauf mit identischen Dateinamen vorhandene Ergebnisse sichern oder einen anderen Ausgabeordner verwenden.

### 2. Verarbeitung: Hauptwerkzeug

1. Die Projektachse und die Breite des Suchraums angeben.
2. Einen oder mehrere vorbereitete Fachdatensätze zuordnen; nicht benötigte Eingaben leer lassen.
3. Puffer für punktuelle und lineare Schutzobjekte festlegen; weitere Parameter entsprechend dem Dialog befüllen.
4. QML-Layerstile, Streckenbezeichnung sowie Ordner für Ergebnisse, Info-Layer und temporäre Dateien auswählen.
5. Verarbeitung starten und Ergebnisse fachlich prüfen.

Das Hauptwerkzeug erstellt unter anderem Ausgaben für QGIS, X2Bim und InfraMaps sowie einen Info-Layer. Je nach Ausgabe werden GeoPackage, GeoJSON und temporäre Shapefiles verwendet. Die tatsächlichen Zielpfade ergeben sich aus den gewählten Ordnern und der Streckenbezeichnung.

## Beispiel: Bahnstrecke 2200 in Niedersachsen

Das Beispiel zeigt den Weg von vorhandenen Strecken- und Naturschutzdaten zur aufbereiteten Entscheidungsgrundlage für eine frühe Projektphase.

- [Beispielpaket herunterladen: gIraffePro_Strecke2200.zip](https://github.com/geogiraffer/gIraffePro/releases/download/v1.0.6/gIraffePro_Strecke2200.zip)
- [Release mit Plugin und Beispielpaket](https://github.com/geogiraffer/gIraffePro/releases/tag/v1.0.6)
- [Bebilderte Anleitung auf der Homepage](https://giraffepro.de/docs/GIRAFFEPRO/BEISPIEL/)

1. Das vollständige Beispielpaket herunterladen und entpacken. Die Ordnerstruktur beibehalten.
2. Die beiliegende `README.md` lesen. Sie erläutert den Inhalt, den Arbeitsablauf sowie Datenquellen und Nutzungsbedingungen.
3. `gIraffePro_Beispiel.qgz` in QGIS öffnen. Die lokalen Datenquellen werden über relative Pfade eingebunden.
4. Die Arbeitsschritte mit den Werkzeugen **Vorbereitung** und **Verarbeitung** nachvollziehen; Hinweise und Parameter in der Beispiel-README beachten.

**Die beiden ZIP-Dateien haben unterschiedliche Zwecke:** Die Plugin-ZIP wird in QGIS über „Aus ZIP installieren“ installiert. Das Beispielpaket wird dagegen entpackt und als QGIS-Projekt geöffnet.

Alle im Beispiel bereitgestellten Ausgangsdaten wurden im **November 2026** heruntergeladen. Das Bezugsjahr 2026 ist nicht mit dem jeweiligen fachlichen Datenstand gleichzusetzen. Maßgeblich sind die Angaben und Originalunterlagen im Beispielpaket. Die Softwarelizenz des Plugins gilt nicht automatisch für die Geodaten.

## Entwicklung und Paketaufbau

- `__init__.py`: Plugin-Einstieg und `classFactory`.
- `giraffepro.py`: Menü-, Toolbar- und Provider-Anbindung.
- `processing_provider/giraffepro_provider.py`: Registrierung der Werkzeuge.
- `processing_provider/fachdatenbewertung.py`: Vorbereitung der Fachdaten.
- `processing_provider/giraffe_main.py`: Hauptverarbeitung.
- `processing_provider/cleanup_1.py` und `cleanup_2.py`: interne Verarbeitungsschritte.
- `metadata.txt`: Plugin-Metadaten.
- `LICENSE`: vollständiger GPLv3-Lizenztext.

Technische IDs wie `giraffepro:fachdatenbewertung` und `giraffepro:giraffe_main` bleiben unabhängig von sichtbaren Bezeichnungen stabil.


## Lizenz

Copyright (C) 2026 Dennis Klingspor.

Der Programmcode von **gIraffePro** wird unter der **GNU General Public License, Version 3 oder – nach deiner Wahl – einer späteren Version** veröffentlicht. SPDX-Kennung: **`GPL-3.0-or-later`**. Der vollständige Lizenztext ist als Datei `LICENSE` im Plugin-Paket enthalten; online steht er bei der [GNU](https://www.gnu.org/licenses/gpl-3.0.html).

Die Software darf unter den Bedingungen dieser Lizenz genutzt, verändert und weitergegeben werden. Sie wird ohne die in der GPL ausgeschlossenen Gewährleistungen bereitgestellt; maßgeblich ist der vollständige Lizenztext. Die Veröffentlichung unter GPL überträgt nicht die Urheberschaft auf Dritte.

Die Lizenzangabe **GPL-3.0-or-later** bezieht sich auf den Programmcode. Für die nachfolgend bezeichnete Zeichnung und die daraus abgeleiteten Plugin-Logos gilt die gesonderte Grafiklizenz. Die Lizenzen von QGIS und weiteren verwendeten Komponenten bleiben unberührt.

### Zeichnung und Plugin-Logos

Die ursprüngliche schwarz-weiße Giraffenzeichnung stammt von **[Caterina Behrendt](https://www.caterinabehrendt.de/)**.

Die Originalzeichnung und die daraus abgeleiteten Plugin-Logos werden unter **[Creative Commons Namensnennung – Weitergabe unter gleichen Bedingungen 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/)** weitergegeben.

| Grafik | Herkunft und Bearbeitung | Lizenz |
| --- | --- | --- |
| Ursprüngliche Giraffenzeichnung | Caterina Behrendt | CC BY-SA 4.0 |
| `logo_giraffe.png` | Auf Grundlage der Zeichnung von Caterina Behrendt; mit ChatGPT/OpenAI-Bildgenerierung ergänzt | CC BY-SA 4.0 |
| `logo_fachdatenbewertung.png` | Auf Grundlage derselben Zeichnung; mit ChatGPT/OpenAI-Bildgenerierung ergänzt | CC BY-SA 4.0 |

Bei einer Weiterverwendung sind die Urheberin, der Lizenzlink und die vorgenommenen Änderungen angemessen anzugeben. Bearbeitungen sind bei Weitergabe unter CC BY-SA 4.0 oder einer zulässigen kompatiblen Lizenz bereitzustellen. Maßgeblich ist der [vollständige Lizenztext](https://creativecommons.org/licenses/by-sa/4.0/legalcode.de).

Empfohlene Herkunftsangabe für die bearbeiteten Plugin-Logos:

> Giraffenzeichnung: Caterina Behrendt, https://www.caterinabehrendt.de/ — CC BY-SA 4.0, https://creativecommons.org/licenses/by-sa/4.0/. Für gIraffePro mit ChatGPT/OpenAI-Bildgenerierung bearbeitet: Kreisrahmen und Landschaft ergänzt; zusätzlich eine Variante mit grauen Landschaftskonturen erstellt.

Die Grafiklizenz gilt unabhängig von der GPL-Lizenz des Programmcodes. Die Kennzeichnung nennt die menschliche Urheberin der Ausgangszeichnung und macht die anschließende KI-Bearbeitung transparent.

### Geodaten des Beispiels

Für die Geodaten gelten die jeweiligen Quellen- und Lizenzangaben unabhängig von GPL und Grafiklizenz:

- **ATKIS-Streckennetz / LGLN:** CC BY 4.0.
- **NLWKN-Schutzgebiete und Schutzobjekte:** Datenlizenz Deutschland – Namensnennung – Version 2.0 (`dl-de/by-2-0`).
- **BKG-Verwaltungsgebiete VG250:** Datenlizenz Deutschland – Namensnennung – Version 2.0 (`dl-de/by-2-0`).
- **OpenStreetMap-Hintergrund:** Quellenvermerk „© OpenStreetMap contributors“ und die [OpenStreetMap-Nutzungs- und Lizenzhinweise](https://www.openstreetmap.org/copyright) beachten; die Hintergrundkarte wird online geladen.

Vollständige Datensatz- und Bearbeitungshinweise stehen in der README und den Lizenzunterlagen des Beispielpakets. Für die Kartenabbildungen auf der Homepage sind sie zusätzlich unter [Lizenzen und Grafiken](https://giraffepro.de/docs/GIRAFFEPRO/GRAFIKEN/) dokumentiert.

## Kontakt

- Projekt: <https://giraffepro.de/>
- Repository: <https://github.com/geogiraffer/gIraffePro/>
- Fehlermeldungen und Vorschläge: <https://github.com/geogiraffer/gIraffePro/issues>
- Autor: Dennis Klingspor
- E-Mail: <kontakt@geobuilder.net>

## Mitwirken

Fehlermeldungen, Fragen und Verbesserungsvorschläge können über die [GitHub-Issues](https://github.com/geogiraffer/gIraffePro/issues) eingereicht werden. Hilfreich sind dabei die Plugin- und QGIS-Version, das Betriebssystem, eine Beschreibung der Arbeitsschritte und die vollständige Fehlermeldung. Für Beispieldaten müssen die nötigen Weitergaberechte vorliegen.


## Änderungen in Version 1.0.7

- Alle elf unterstützten Fachdaten-Eingaben in Vorbereitung und Verarbeitung sind optional; mindestens ein Fachdatensatz bleibt erforderlich.
- Nicht ausgewählte Eingaben werden übersprungen und erzeugen keine eigenen Vorbereitungsdateien oder Info-Layer.
- Zusammenführung und Gewichtung berücksichtigen nur vorhandene Datensätze und Geometrievarianten.
- Nicht lesbare, ausdrücklich angegebene Datenquellen und fehlende Wertfelder werden mit einer Fehlermeldung zurückgewiesen.
- Der Puffer für lineare Naturdenkmäler wird korrekt als numerischer Wert gelesen.
- Hauptergebnis-Pfade werden als Zeichenketten statt versehentlicher Ein-Element-Tupel zurückgegeben.
- Der bisherige Ergebnis-Layername „keine Kollision“ wurde zu „keine Überlagerung ausgewählter Fachdaten“ präzisiert.

