# gIraffePro

**Grüne Infrastruktur frühzeitig filtern und einschätzen – in jedem Projekt!**

Version 1.0.6 · Stand: 31. Oktober 2026

[Homepage](https://giraffepro.de/) · [Quellcode](https://github.com/geogiraffer/gIraffePro/) · [Fehler melden](https://github.com/geogiraffer/gIraffePro/issues) · [Releases](https://github.com/geogiraffer/gIraffePro/releases)

> **English summary:** gIraffePro is a QGIS Processing plugin for preparing protected-area datasets and screening potential conflicts with planned infrastructure using configurable buffers and traffic-light ratings.

## Zweck

gIraffePro unterstützt die frühe Einschätzung möglicher Konflikte zwischen geplanten Infrastrukturvorhaben und grüner Bestandsinfrastruktur. Das Plugin bereitet Fachdaten mit einer nutzerdefinierten Bewertung vor und verarbeitet sie anschließend entlang einer Projektachse innerhalb variabler Suchräume.

Die Ergebnisse dienen einer überschlägigen planerischen Einschätzung. Sie ersetzen keine fachliche Prüfung oder behördliche Entscheidung. Aussagekraft und Vollständigkeit hängen von den Eingangsdaten, der gewählten Bewertung und den Puffereinste

## Voraussetzungen

- QGIS ab Version 3.40 laut Plugin-Metadaten.
- Aktivierte QGIS-Verarbeitung (Processing) und die verwendeten nativen QGIS-Algorithmen.
- Geeignete Punkt-, Linien- und Flächendaten sowie eine Projektachse als Linienlayer.
- Schreibbare Ausgabeordner; für das Hauptwerkzeug zusätzlich die abgefragten QGIS-Layerstile im QML-Format.
- Für Abstände in Metern geeignete und fachlich konsistente Koordinatenreferenzsysteme.

Die Python-Module verwenden QGIS/PyQGIS und die Python-Standardbibliothek; sie sind keine eigenständig ausführbaren Python-Skripte.

### Getestete Umgebung

Das Plugin wurde vom Projektentwickler bisher mit **QGIS 3.44 unter Fedora Linux in einer Mamba-Umgebung** getestet. Andere QGIS-Versionen, Betriebssysteme und Installationsarten sind damit nicht als getestet ausgewiesen. Die Mindestversion 3.40 in den Metadaten ist von diesem dokumentierten Teststand zu unterscheiden.

## Installation

1. Die fertige Plugin-ZIP aus einem [Release](https://github.com/geogiraffer/gIraffePro/releases) herunterladen, sofern dort bereitgestellt.
2. In QGIS **Erweiterungen → Erweiterungen verwalten und installieren → Aus ZIP installieren** öffnen.
3. Die ZIP auswählen, installieren und das Plugin aktivieren.
4. Bei einem Update QGIS neu starten, falls noch alte Einträge oder Icons angezeigt werden.

In der ZIP muss direkt der Ordner `giraffePro/` mit `metadata.txt` und `__init__.py` liegen. Die ZIP muss vor der Installation nicht entpackt werden. Automatisch erzeugte GitHub-Quellcodearchive sind bei einer zusätzlichen Repository-Ordnerebene nicht direkt installierbar; verwende den ausdrücklich bereitgestellten Plugin-ZIP-Anhang eines Releases.

## Werkzeuge

Im Processing-Provider **gIraffePro** stehen zwei Gruppen bereit:

| Gruppe | Werkzeug | Aufgabe |
| --- | --- | --- |
| Vorbereitung | Fachdatenbewertung | Fachdaten bewerten und als GeoJSON speichern |
| Verarbeitung | Green Infrastructure fast filter and estimation Project (gIraffePro) | Bewertete Fachdaten im Suchraum verarbeiten und Ergebnisse erzeugen |

Beide Werkzeuge sind außerdem über das Plugin-Menü und eigene Toolbar-Schaltflächen erreichbar. 

### 1. Vorbereitung: Fachdatenbewertung

Das Werkzeug verarbeitet folgende elf Eingaben. Punkt-, Linien- und Flächenvarianten derselben Fachdatenart erhalten bewusst denselben Wertfeldnamen.

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

1. Die Fachlayer auswählen.
2. Die Bewertung von **1 bis 3** je Datensatz fachlich festlegen; voreingestellte Werte können geändert werden.
3. Bundesland-Kennung und Ausgabeordner angeben.
4. Werkzeug ausführen. Linien und Flächen durchlaufen vorher die Geometriereparatur; Punktdaten erhalten das Wertfeld direkt.

Die Ausgabe erfolgt je Fachdatenart als eigene GeoJSON-Datei, beispielsweise `gIraffePro_FFH_Ni.geojson`. Die Kennung `Ni` ergibt sich aus der Eingabe für das Bundesland. Vor einem erneuten Lauf mit identischen Dateinamen vorhandene Ergebnisse sichern oder einen anderen Ausgabeordner verwenden.

### 2. Verarbeitung: Hauptwerkzeug

1. Die Projektachse und die Breite des Suchraums angeben.
2. Die vorbereiteten Fachdaten den passenden Eingaben zuordnen.
3. Puffer für punktuelle und lineare Schutzobjekte festlegen; weitere Parameter entsprechend dem Dialog befüllen.
4. QML-Layerstile, Streckenbezeichnung sowie Ordner für Ergebnisse, Info-Layer und temporäre Dateien auswählen.
5. Verarbeitung starten und Ergebnisse fachlich prüfen.

Das Hauptwerkzeug erstellt unter anderem Ausgaben für QGIS, X2Bim und InfraMaps sowie einen Info-Layer. Je nach Ausgabe werden GeoPackage, GeoJSON und temporäre Shapefiles verwendet. Die tatsächlichen Zielpfade ergeben sich aus den gewählten Ordnern und der Streckenbezeichnung.

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

Beim Packen aus dem übergeordneten Verzeichnis nur den Plugin-Ordner einschließen, beispielsweise:

```bash
zip -r gIraffePro_1.0.6.zip giraffePro/ -x '*/__pycache__/*' '*.pyc' '*~'
```

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

## Kontakt

- Projekt: <https://giraffepro.de/>
- Repository: <https://github.com/geogiraffer/gIraffePro/>
- Fehlermeldungen und Vorschläge: <https://github.com/geogiraffer/gIraffePro/issues>
- Autor: Dennis Klingspor
- E-Mail: <kontakt@geobuilder.net>

## Mitwirken

Fehlermeldungen, Fragen und Verbesserungsvorschläge können über die [GitHub-Issues](https://github.com/geogiraffer/gIraffePro/issues) eingereicht werden. Hilfreich sind dabei die Plugin- und QGIS-Version, das Betriebssystem, eine Beschreibung der Arbeitsschritte und die vollständige Fehlermeldung. Für Beispieldaten müssen die nötigen Weitergaberechte vorliegen.


