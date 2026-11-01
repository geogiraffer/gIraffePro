# gIraffePro – Beispiel Strecke 2200
[Beispielprojekt herunterladen (ZIP)](https://github.com/geogiraffer/gIraffePro/releases/download/v1.0.6/gIraffePro_Strecke2200.zip)

Dieses Datenpaket enthält ein QGIS-Projekt und Eingangsdaten zum Ausprobieren von **gIraffePro**. Das Beispiel zeigt, wie sich Fachdaten zu Natur und Landschaft vorbereiten und entlang einer Projektachse auswerten lassen. Die Ergebnisse dienen einer ersten räumlichen Einschätzung in frühen Planungsphasen.

- [Projektwebsite und Anleitung](https://giraffepro.de/)
- [Plugin und Quellcode](https://github.com/geogiraffer/gIraffePro/)
- [Plugin-Releases](https://github.com/geogiraffer/gIraffePro/releases)
- [Fehler melden und Fragen stellen](https://github.com/geogiraffer/gIraffePro/issues)

## Voraussetzungen

- QGIS; das Plugin wurde bisher mit **QGIS 3.44 unter Fedora in einer Mamba-Umgebung** getestet. Die beiliegende Projektdatei wurde zuletzt mit QGIS 3.44.7 gespeichert.
- Installiertes und aktiviertes Plugin **gIraffePro** für die Verarbeitungsschritte.
- Internetzugang für die optionale OpenStreetMap-Hintergrundkarte. Die übrigen Daten liegen lokal bei.

Das Paket enthält die Eingangsdaten und Arbeitsordner, jedoch keine bereits berechneten gIraffePro-Ergebnisse. **Alle im Paket bereitgestellten Ausgangsdaten wurden im November 2026 heruntergeladen.** Das Bezugsjahr für die Quellenvermerke ist daher **2026**; es ist vom jeweiligen fachlichen Datenstand zu unterscheiden.

## Schnellstart

1. Das vollständige Datenpaket herunterladen und entpacken. Die Ordnerstruktur beibehalten.
2. `gIraffePro_Beispiel.qgz` in QGIS öffnen. Die lokalen Datenquellen sind mit **relativen Pfaden** eingebunden.
3. Zu Beginn enthält das Projekt vier Layer: `DE_VG250_lan`, `ver03_l`, `Strecke_2200` und die Online-Hintergrundkarte `OpenStreetMap`.
4. Als Projektachse für die Verarbeitung den bereits eingebundenen Layer `Strecke_2200` verwenden. Er verweist auf `01_Land_Atkis/Strecke_2200.geojson`; ein zusätzlicher Import ist nicht erforderlich.
5. Die benötigten Fachdaten aus `02_Land_Fachdaten` laden. Dazu die jeweiligen ZIP-Dateien in eigene Unterordner entpacken und die darin enthaltenen `.shp`-Dateien hinzufügen. Alle zugehörigen Shapefile-Dateien zusammen aufbewahren. Die Original-ZIP-Dateien mit Erläuterungen und Lizenzhinweisen erhalten.
6. In der **Verarbeitungswerkzeugkiste → gIraffePro → Vorbereitung** die **Fachdatenbewertung** öffnen und die Fachdaten den passenden Eingaben zuordnen. Dauerhafte Ergebnisse beispielsweise in `03_gIP_Fachdaten` speichern.
7. Unter **gIraffePro → Verarbeitung** den Hauptalgorithmus öffnen. Die Beispielachse und die vorbereiteten Fachdaten auswählen und die Puffer- und Bewertungsparameter passend zum Beispiel einstellen. Ergebnisse in `04_gIP_Ergebniss`, Info-Layer in `05_gIP_Info` speichern.
8. Bei Bedarf die Stildateien aus `99_Stil` über die QGIS-Layereigenschaften laden. Das Projekt anschließend speichern.

Die vollständige Erläuterung der Werkzeuge und Parameter steht auf der [Projektwebsite](https://giraffepro.de/). Dieses Paket legt keine verbindlichen Pufferabstände oder fachlich allgemein gültigen Bewertungswerte fest.

**Hinweis zum Koordinatensystem:** Das Projekt und die lokalen, bereits eingebundenen Vektordaten verwenden **ETRS89 / UTM Zone 32N (EPSG:25832)**. Für die räumliche Verarbeitung sind geeignete metrische Koordinatensysteme und die jeweiligen Werkzeuganforderungen zu beachten. Die OpenStreetMap-Karte wird in EPSG:3857 bereitgestellt und von QGIS für die Anzeige umprojiziert.

## Inhalt und Ordnerstruktur

| Datei oder Ordner | Inhalt / Zweck |
|---|---|
| `gIraffePro_Beispiel.qgz` | QGIS-Projekt mit relativen Datenpfaden |
| `00_Hintergrund/VWG/` | Verwaltungsgebiete VG250 als GeoJSON, Metadaten und mitgelieferte BKG-Lizenzunterlagen |
| `01_Land_Atkis/ver03_l.geojson` | ATKIS-Streckennetz als Hintergrund- und Orientierungsdaten; im Projekt eingebunden |
| `01_Land_Atkis/Strecke_2200.geojson` | Beispielachse Strecke 2200; im Projekt eingebunden |
| `01_Land_Atkis/20241015_AGNB_LGLN_.pdf` | Mitgelieferte LGLN-Nutzungsbedingungen; Abschnitt 7 behandelt offene Geodaten |
| `02_Land_Fachdaten/` | Elf ZIP-Pakete mit Schutzgebiets- und Schutzobjektdaten einschließlich Begleitunterlagen |
| `03_gIP_Fachdaten/` | Arbeitsordner für vorbereitete und bewertete Fachdaten; anfangs leer |
| `04_gIP_Ergebniss/` | Arbeitsordner für Verarbeitungsergebnisse; anfangs leer |
| `05_gIP_Info/` | Arbeitsordner für Info-Layer; anfangs leer |
| `98_giP_tmp/` | Arbeitsordner für Zwischenergebnisse; anfangs leer |
| `99_Stil/Abfragegrenze_Stil.qml` | QGIS-Stildatei für die Abfragegrenze |
| `99_Stil/Ampel_Stil.qml` | QGIS-Stildatei für die Ampeldarstellung |

Die Schreibweise der Ordner entspricht dem bereitgestellten Paket. Git speichert leere Ordner nicht: Bei Bedarf die Arbeitsordner nach dem Herunterladen anlegen oder im Repository mit einer `.gitkeep`-Datei erhalten.

## Enthaltene Fachdaten

| Eingabe im Beispiel | Datei | Inhalt / Geometrie |
|---|---|---|
| 1. FFH | `FFH.zip` | Fauna-Flora-Habitat-Gebiete, Flächen |
| 2. LSG | `LSG.zip` | Landschaftsschutzgebiete, Flächen |
| 3. LSG lin | `LSG_line.zip` | Landschaftsschutzgebiete, Linien |
| 4. ND pkt | `ND_point.zip` | Naturdenkmale, Punkte |
| 5. ND lin | `ND_line.zip` | Naturdenkmale, Linien |
| 6. ND | `ND.zip` | Naturdenkmale, Flächen |
| 7. SPA | `BSG.zip` | Europäische Vogelschutzgebiete, Flächen; im Paket abweichend als BSG benannt |
| 8. NSG | `NSG.zip` | Naturschutzgebiete, Flächen |
| 9. GLB pkt | `GLB_point.zip` | Geschützte Landschaftsbestandteile, Punkte |
| 10. GLB lin | `GLB_line.zip` | Geschützte Landschaftsbestandteile, Linien |
| 11. GLB | `GLB.zip` | Geschützte Landschaftsbestandteile, Flächen |

`BSG.zip` enthält das Shapefile `EU_Vogelschutzgebiete_TK50.shp`; dieses ist der Eingabe SPA zuzuordnen. Die verschiedenen Geometrieausprägungen einer Fachdatengruppe werden im weiteren Arbeitsablauf gemeinsam behandelt.

## Datenquellen und Datenstände

### Natur- und Landschaftsdaten Niedersachsen

Bereitstellung über die Umweltkarten des Niedersächsischen Ministeriums für Umwelt, Energie und Klimaschutz; Rechteinhaber und Datenbereitsteller laut den beiliegenden Lizenzunterlagen ist der **Niedersächsische Landesbetrieb für Wasserwirtschaft, Küsten- und Naturschutz (NLWKN)**.

- [Natura 2000: Europäische Vogelschutzgebiete und gemeldete FFH-Gebiete in Niedersachsen](https://www.umwelt.niedersachsen.de/startseite/service/umweltkarten/natur_amp_landschaft/natura_2000/natura-2000-europaeische-vogelschutzgebiete-und-gemeldete-ffh-gebiete-in-niedersachsen-9124.html)
- [Naturschutzrechtlich besonders geschützte Teile von Natur und Landschaft](https://www.umwelt.niedersachsen.de/startseite/service/umweltkarten/natur_amp_landschaft/besonders_geschutzte_teile_von_natur_und_landschaft/naturschutzrechtlich-besonders-geschutzte-teile-von-natur-und-landschaft-9065.html)
- [NLWKN: Open Data und Nutzungsbedingungen](https://www.nlwkn.niedersachsen.de/opendata/)

Die Begleitdateien `Datenaktualitaet_Hinweise.txt` in den Paketen NSG, LSG, ND und GLB nennen den **Stand 31.12.2025, erste Veröffentlichung 2026**. Dieser Stand darf nicht pauschal auf FFH und Vogelschutzgebiete übertragen werden; für diese gelten die jeweiligen Begleitunterlagen. Das FFH-Paket enthält unter anderem eine Gebietsliste von Juli 2025. Das ist kein Nachweis für ein einheitliches Aktualitätsdatum sämtlicher Geometrien und Attribute.

Datenbezug und Zusammenstellung dieses Beispielpakets: **November 2026**. Das Paket wird nicht automatisch mit den amtlichen Quellen synchronisiert.

### Verwaltungsgebiete VG250

Der Hintergrundlayer `DE_VG250_lan.geojson` enthält die Länderebene der Verwaltungsgebiete 1:250.000 des **Bundesamtes für Kartographie und Geodäsie (BKG)**. Die beiliegende `aktualitaet.txt` nennt den **Stand 01.01.2023**.

- [BKG: Verwaltungsgebiete VG250, Stand 01.01. – Produktseite](https://gdz.bkg.bund.de/index.php/default/open-data/verwaltungsgebiete-1-250-000-stand-01-01-vg250-01-01.html)
- [BKG-Website](https://www.bkg.bund.de/)

Die Produktseite ist als Bezugsquelle dokumentiert, auch wenn der Download zeitweise nicht erreichbar ist. Für dieses Beispiel ist kein erneuter Download erforderlich. Neuere Ausgaben können vom hier verwendeten Stand abweichen.

Die bereitgestellte Fassung liegt als GeoJSON in EPSG:25832 vor. Die ursprüngliche Ausgabe sowie weitere mögliche Bearbeitungsschritte sind im Paket nicht vollständig dokumentiert.

### ATKIS-Streckennetz und Beispielachse

Das Streckennetz stammt aus dem offenen Datenangebot des **Landesamtes für Geoinformation und Landesvermessung Niedersachsen (LGLN)**: [OpenGeoData.NI](https://ni-lgln-opengeodata.hub.arcgis.com/). Datenbezug: **November 2026**.

- `01_Land_Atkis/ver03_l.geojson`: Streckennetz mit ATKIS-Objekten der Objektart `AX_Bahnstrecke`.
- `01_Land_Atkis/Strecke_2200.geojson`: Beispielachse mit 370 Linienobjekten; das Attribut `nummerderbahnstrecke` enthält den Wert `2200`.
- `01_Land_Atkis/20241015_AGNB_LGLN_.pdf`: beigefügte Allgemeine Geschäfts- und Nutzungsbedingungen des LGLN, Stand 01.10.2024. **Abschnitt 7** nennt für das offene Angebot **Creative Commons Namensnennung 4.0 International (CC BY 4.0)** sowie den geforderten Quellenvermerk.

Beide GeoJSON-Dateien deklarieren EPSG:25832 und sind bereits mit relativen Pfaden in das QGIS-Projekt eingebunden. Die Beispielachse stellt die für das Beispiel ausgewählten Objekte der Strecke 2200 dar. Die bereitgestellten Fassungen verwenden unterschiedliche Geometrie- und Attributdarstellungen: Das Streckennetz enthält MultiLineString-Geometrien und ATKIS-Feldnamen, die Beispielachse LineString-Geometrien und ausgeschriebene Attributnamen. Die Beispielaufbereitung ist als Bearbeitung gekennzeichnet. Ein gesonderter einheitlicher fachlicher Datenstand des Streckennetzes ist aus den beigefügten Unterlagen nicht ersichtlich; das Downloadjahr 2026 ersetzt diese Angabe nicht.

Weitere Informationen: [LGLN-Nutzungsbedingungen](https://www.lgln.niedersachsen.de/startseite/wir_uber_uns_amp_organisation/logo/allgemeine-geschafts-und-nutzungsbedingungen-agnb-97401.html).

### OpenStreetMap

Die Hintergrundkarte wird als Online-XYZ-Dienst von `tile.openstreetmap.org` eingebunden. Kartenkacheln sind nicht Bestandteil des Datenpakets. Ohne Internet kann der Layer ausgeschaltet werden.

Quellenvermerk für Karten und Screenshots mit dieser Hintergrundkarte: **[© OpenStreetMap contributors](https://www.openstreetmap.org/copyright)**. Für den Kacheldienst gelten zusätzlich dessen [Nutzungsbedingungen](https://operations.osmfoundation.org/policies/tiles/).

## Lizenzen und Quellenvermerke

Die Softwarelizenz des Plugins und die Nutzungsbedingungen der Geodaten sind getrennt zu beachten. Die GPL des Plugins lizenziert nicht automatisch die hier mitgelieferten Fremddaten.

| Bestandteil | Lizenz / Hinweis |
|---|---|
| gIraffePro-Plugin | GPL-3.0-or-later; Lizenztext im Plugin-Repository |
| NLWKN-Fachdaten | Datenlizenz Deutschland – Namensnennung – Version 2.0 (`dl-de/by-2-0`); Lizenz-PDF in jedem Fachdaten-ZIP beachten |
| VG250 | Datenlizenz Deutschland – Namensnennung – Version 2.0; Unterlagen in `00_Hintergrund/VWG/` beachten |
| OpenStreetMap-Daten | Open Database License (ODbL); Quellenvermerk und Bedingungen des Kartendienstes beachten |
| ATKIS-Streckennetz und Achse 2200 | LGLN / OpenGeoData.NI; CC BY 4.0; Bearbeitung für das Beispiel. Abschnitt 7 der beiliegenden `01_Land_Atkis/20241015_AGNB_LGLN_.pdf` beachten |
| QGIS-Projekt, eigene Stile und README | Eine gesonderte Lizenzfestlegung für diese eigenen Bestandteile ist in diesem Paket noch nicht dokumentiert |

Lizenztext für NLWKN und BKG: [Datenlizenz Deutschland – Namensnennung – Version 2.0](https://www.govdata.de/dl-de/by-2-0).

Die Daten wurden im **November 2026** bezogen. Für die NLWKN-Daten lautet der Quellenvermerk daher:

> 2026 Niedersächsischer Landesbetrieb für Wasserwirtschaft, Küsten- und Naturschutz (NLWKN), https://www.nlwkn.niedersachsen.de/opendata/ – Datenlizenz Deutschland – Namensnennung – Version 2.0.

Für die VG250-Daten wird ebenfalls das Bezugsjahr **2026** angegeben. Der fachliche Datenstand bleibt **01.01.2023**:

> © GeoBasis-DE / [BKG](https://www.bkg.bund.de/) 2026 (Daten verändert), [dl-de/by-2-0](https://www.govdata.de/dl-de/by-2-0). Bereitgestellte Fassung: GeoJSON, EPSG:25832.

Für das ATKIS-Streckennetz und die im Beispiel verwendete Achse gilt:

> © GeoBasis-DE/[LGLN](https://www.lgln.niedersachsen.de/) 2026, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), Daten geändert. Quelle: [OpenGeoData.NI](https://ni-lgln-opengeodata.hub.arcgis.com/). Bearbeitung für das gIraffePro-Beispiel: Auswahl der Strecke 2200 und angepasste Datenaufbereitung.

Bei abgeleiteten, zugeschnittenen, umprojizierten oder bewerteten Daten sind die Änderungen kenntlich zu machen. Die ursprünglichen Quellen- und Lizenzhinweise sind zu erhalten. Bei veröffentlichten Karten und Screenshots gehören die verwendeten Quellenvermerke auch zur Darstellung; diese README allein ersetzt sie dort nicht.

## Aussagekraft und Grenzen

Das Beispiel veranschaulicht einen Arbeitsablauf und ersetzt weder eine umweltfachliche Prüfung noch eine rechtlich verbindliche Auskunft. Die Ampelfarben stellen eine Auswertung anhand der gewählten Eingangsdaten, Bewertungswerte und Puffer dar. Sie sind keine behördliche Einstufung und keine Aussage über die Genehmigungsfähigkeit eines Vorhabens.

Die NLWKN-Begleitunterlagen weisen für die besonders geschützten Teile von Natur und Landschaft auf die Aussagekraft im Maßstab der DTK25 hin. Die Natura-2000-Shapefiles sind als TK50-Datensätze bezeichnet. Rechtlich verbindliche Schutzgebietsgrenzen ergeben sich aus den maßgeblichen Verordnungen und veröffentlichten Karten, nicht aus dieser Beispielauswertung. Datenlücken oder fehlende Überlagerungen belegen nicht die Abwesenheit schutzwürdiger Belange.


