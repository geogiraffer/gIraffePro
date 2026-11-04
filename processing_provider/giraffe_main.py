# -*- coding: utf-8 -*-
# Copyright (C) 2026 Dennis Klingspor
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This file is part of gIraffePro.
#
# gIraffePro is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# gIraffePro is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gIraffePro. If not, see <https://www.gnu.org/licenses/>.

"""
Model exported as python.
Name : Green Infrastructure fast filter and estimation Project (GIraFFE-Pro)
Group : gIraffePro
With QGIS : 34001
"""

from qgis.core import (
    Qgis,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterNumber,
    QgsProcessingParameterFile,
    QgsProcessingParameterString,
    QgsCoordinateReferenceSystem,
    QgsProcessingException,
    QgsProcessingUtils,
)
from qgis.PyQt.QtGui import QIcon
from qgis.core import QgsExpression
from pathlib import Path
import processing
from .fachdaten_schema import selected_datasets, maximum_expression


class GreenInfrastructureFFEProject(QgsProcessingAlgorithm):
    def icon(self):
        return QIcon(str(Path(__file__).parent.parent / "logo_giraffe.png"))

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                "streckenabschnitt_linie",
                "Projektachse (Linie)",
                types=[Qgis.ProcessingSourceType.VectorLine],
                defaultValue=None,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                "puffer_m",
                "Suchraum (m)",
                type=Qgis.ProcessingNumberParameterType.Integer,
                defaultValue=50,
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                "_fachdatum_fd_ffh",
                "1. Fachdatensatz: FFH",
                optional=True,
                types=[Qgis.ProcessingSourceType.VectorPolygon],
                defaultValue=None,
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                "_fd_lsg",
                "2. Fachdatensatz: LSG",
                optional=True,
                types=[Qgis.ProcessingSourceType.VectorPolygon],
                defaultValue=None,
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                "_fd_lsg_linear",
                "3. Fachdatensatz: LSG linear",
                optional=True,
                types=[Qgis.ProcessingSourceType.VectorLine],
                defaultValue="",
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                "puffer_lsg_linear_m",
                "Puffer LSG linear (m)",
                type=Qgis.ProcessingNumberParameterType.Integer,
                defaultValue=20,
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                "_fd_natiurdenkmal_punkt_28",
                "4. Fachdatensatz: Natiurdenkmal Punkt (§28)",
                optional=True,
                types=[Qgis.ProcessingSourceType.VectorPoint],
                defaultValue=None,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                "puffer_nd_punkt_m",
                "Puffer ND Punkt (m)",
                type=Qgis.ProcessingNumberParameterType.Integer,
                defaultValue=20,
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                "_fd_nd__linear_28",
                "5. Fachdatensatz: ND  linear (§28)",
                optional=True,
                types=[Qgis.ProcessingSourceType.VectorLine],
                defaultValue=None,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                "puffer_nd_linear_m",
                "Puffer ND linear (m)",
                type=Qgis.ProcessingNumberParameterType.Integer,
                defaultValue=20,
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                "_fd_nd__28",
                "6. Fachdatensatz: ND  (§28)",
                optional=True,
                types=[Qgis.ProcessingSourceType.VectorPolygon],
                defaultValue=None,
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                "_fd_spa",
                "7. Fachdatensatz: SPA",
                optional=True,
                types=[Qgis.ProcessingSourceType.VectorPolygon],
                defaultValue=None,
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                "_fd_nsg",
                "8. FD: NSG",
                optional=True,
                types=[Qgis.ProcessingSourceType.VectorPolygon],
                defaultValue=None,
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                "_fd_gesch_landschaftsbestandteil_glb_punkt_29",
                (
                    "9. Fachdatensatz: gesch. Landschaftsbestandteil (GLB) "
                    "punkt (§29)"
                ),
                optional=True,
                types=[Qgis.ProcessingSourceType.VectorPoint],
                defaultValue=None,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                "puffer_glb_pkt_m",
                "Puffer GLB pkt. (m)",
                type=Qgis.ProcessingNumberParameterType.Integer,
                defaultValue=20,
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                "_fd_glb_linear_29",
                "10. Fachdatensatz: GLB linear (§29)",
                optional=True,
                types=[Qgis.ProcessingSourceType.VectorLine],
                defaultValue=None,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                "puffer_glb_lin_m",
                "Puffer GLB lin. (m)",
                type=Qgis.ProcessingNumberParameterType.Integer,
                defaultValue=20,
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                "_fd_glb_29",
                "11. Fachdatensatz: GLB (§29)",
                optional=True,
                types=[Qgis.ProcessingSourceType.VectorPolygon],
                defaultValue=None,
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                "_fd_30_biotope_linear_optional_nach_kreisabfrage",
                (
                    "12. Fachdatensatz: §30 Biotope linear (optional nach "
                    "Kreisabfrage)"
                ),
                optional=True,
                types=[Qgis.ProcessingSourceType.VectorPolygon],
                defaultValue=None,
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                "_fd_30_biotope_punktuell_optional_nach_kreisabfrage",
                (
                    "13. Fachdatensatz: §30 Biotope punktuell (optional nach "
                    "Kreisabfrage)"
                ),
                optional=True,
                types=[Qgis.ProcessingSourceType.VectorPoint],
                defaultValue=None,
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                "_fd_30_biotope_flchig_optional_nach_kreisabfrage",
                (
                    "14. Fachdatensatz: §30 Biotope flächig (optional nach "
                    "Kreisabfrage)"
                ),
                optional=True,
                types=[Qgis.ProcessingSourceType.VectorPolygon],
                defaultValue=None,
            )
        )
        self.addParameter(
            QgsProcessingParameterFile(
                "layerstil_ampel_qml",
                "Layerstil Ampel (*.qml)",
                behavior=Qgis.ProcessingFileParameterBehavior.File,
                fileFilter="Alle Dateien (*.*)",
                defaultValue=None,
            )
        )
        self.addParameter(
            QgsProcessingParameterFile(
                "layerstil_abfraggrenze_qml",
                "Layerstil Abfraggrenze (*.qml)",
                behavior=Qgis.ProcessingFileParameterBehavior.File,
                fileFilter="Alle Dateien (*.*)",
                defaultValue=None,
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                "strecke", "Strecke", multiLine=False, defaultValue=None
            )
        )
        self.addParameter(
            QgsProcessingParameterFile(
                "zielordner_giraffepro_ergebnis",
                "Zielordner gIraffePro Ergebnis",
                behavior=Qgis.ProcessingFileParameterBehavior.Folder,
                fileFilter="All files (*.*)",
                defaultValue=None,
            )
        )
        self.addParameter(
            QgsProcessingParameterFile(
                "zielordner_giraffepro_infolayer",
                "Zielordner gIraffePro Info-Layer",
                behavior=Qgis.ProcessingFileParameterBehavior.Folder,
                fileFilter="All files (*.*)",
                defaultValue=None,
            )
        )
        self.addParameter(
            QgsProcessingParameterFile(
                "zielordner_tmp_dateien",
                "Zielordner tmp. Dateien",
                behavior=Qgis.ProcessingFileParameterBehavior.Folder,
                fileFilter="All files (*.*)",
                defaultValue=None,
            )
        )

        for name in (
            "_fd_30_biotope_linear_optional_nach_kreisabfrage",
            "_fd_30_biotope_punktuell_optional_nach_kreisabfrage",
            "_fd_30_biotope_flchig_optional_nach_kreisabfrage",
        ):
            self.parameterDefinition(name).setHelp(
                (
                    "Reservierte Eingabe: §30-Biotope werden im bisherigen "
                    "Arbeitsablauf noch nicht ausgewertet. Für einen Lauf ist "
                    "mindestens ein Fachdatensatz aus den Eingaben 1 bis 11 "
                    "erforderlich."
                )
            )

    def checkParameterValues(self, parameters, context):
        valid, message = super().checkParameterValues(parameters, context)
        if not valid:
            return valid, message
        try:
            selected_datasets(self, parameters, context, "main")
        except QgsProcessingException as error:
            return False, str(error)
        return True, ""

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm
        # progress reports are adjusted for the
        # overall progress through the model
        selected = selected_datasets(self, parameters, context, "main")
        feedback = QgsProcessingMultiStepFeedback(
            len(selected) * 8 + 80, model_feedback
        )
        results = {}
        outputs = {}

        # 1. Werte aus den Parametern auslesen (als Text/String)
        folder_path_res = self.parameterAsString(
            parameters, "zielordner_giraffepro_ergebnis", context
        )
        folder_path_info = self.parameterAsString(
            parameters, "zielordner_giraffepro_infolayer", context
        )
        folder_path_tmp = self.parameterAsString(
            parameters, "zielordner_tmp_dateien", context
        )
        suffix = self.parameterAsString(parameters, "strecke", context)

        # 2. Den Zielpfad dynamisch und plattformunabhängig zusammenbauen
        # info
        info = str(Path(folder_path_info) / f"gIraffePro_Info_{suffix}.gpkg")

        # x2BIM-RES
        res_x2bim_lim = str(
            Path(folder_path_res)
            / f"gIraffePro_X2Bim_Abfragegrenzen_{suffix}.geojson"
        )
        res_x2bim_yel = str(
            Path(folder_path_res) / f"gIraffePro_X2Bim_Gelb_{suffix}.geojson"
        )
        res_x2bim_red = str(
            Path(folder_path_res) / f"gIraffePro_X2Bim_Rot_{suffix}.geojson"
        )
        res_x2bim_gre = str(
            Path(folder_path_res) / f"gIraffePro_X2Bim_gre_{suffix}.geojson"
        )

        # inframaps-res
        res_inframaps = str(
            Path(folder_path_res) / f"gIraffePro_InfraMaps_{suffix}.geojson"
        )
        res_inframaps_lim = str(
            Path(folder_path_res)
            / f"gIraffePro_InfraMaps_Abfragegrenzen_{suffix}.geojson"
        )

        # qgis-res
        res_qgis = str(
            Path(folder_path_res) / f"gIraffePro_QGIS_{suffix}.gpkg"
        )

        # tmp
        tmp_qgis_tlc = str(
            Path(folder_path_tmp) / f"gIraffePro_QGIS-Ampel_{suffix}.shp"
        )
        tmp_qgis_buf = str(
            Path(folder_path_tmp) / f"gIraffePro_QGIS-0_{suffix}.shp"
        )
        tmp_qgis_lim = str(
            Path(folder_path_tmp)
            / f"gIraffePro_QGIS_Abfragegrenzen_{suffix}.shp"
        )

        # Evaluate only selected inputs. Each supplied source keeps its own
        # Info layer;
        # omitted inputs create neither a processing branch nor an output file.
        step = [0]

        def run(algorithm, values):
            feedback.setCurrentStep(step[0])
            step[0] += 1
            return processing.run(
                algorithm,
                values,
                context=context,
                feedback=feedback,
                is_child_algorithm=True,
            )

        def resolve(layer):
            if isinstance(layer, str):
                layer = QgsProcessingUtils.mapLayerFromString(layer, context)
            if layer is None or not layer.isValid():
                raise QgsProcessingException(
                    "Ein Verarbeitungsergebnis konnte nicht geladen werden."
                )
            return layer

        def drop_existing(
            layer, fields, destination=QgsProcessing.TEMPORARY_OUTPUT
        ):
            names = resolve(layer).fields().names()
            columns = [name for name in fields if name in names]
            if columns:
                return run(
                    "native:deletecolumn",
                    {"INPUT": layer, "COLUMN": columns, "OUTPUT": destination},
                )["OUTPUT"]
            if destination != QgsProcessing.TEMPORARY_OUTPUT:
                return run(
                    "native:savefeatures",
                    {"INPUT": layer, "OUTPUT": destination},
                )["OUTPUT"]
            return layer

        def union(layers):
            combined = layers[0]
            for overlay in layers[1:]:
                combined = run(
                    "native:union",
                    {
                        "INPUT": combined,
                        "OVERLAY": overlay,
                        "OVERLAY_FIELDS_PREFIX": "",
                        "OUTPUT": QgsProcessing.TEMPORARY_OUTPUT,
                    },
                )["OUTPUT"]
            return combined

        axis = self.parameterAsVectorLayer(
            parameters, "streckenabschnitt_linie", context
        )
        outputs["Streckenabschnittspuffer"] = run(
            "native:buffer",
            {
                "INPUT": axis,
                "DISTANCE": self.parameterAsDouble(
                    parameters, "puffer_m", context
                ),
                "DISSOLVE": False,
                "END_CAP_STYLE": 0,
                "JOIN_STYLE": 0,
                "MITER_LIMIT": 2,
                "SEGMENTS": 5,
                "OUTPUT": QgsProcessing.TEMPORARY_OUTPUT,
            },
        )
        outputs["StreckenabschnittpufferBereinigt"] = run(
            "native:dissolve",
            {
                "INPUT": outputs["Streckenabschnittspuffer"]["OUTPUT"],
                "FIELD": [],
                "OUTPUT": QgsProcessing.TEMPORARY_OUTPUT,
            },
        )
        outputs["GeometrienReparierenStreckenpuffer"] = run(
            "native:fixgeometries",
            {
                "INPUT": outputs["StreckenabschnittpufferBereinigt"]["OUTPUT"],
                "METHOD": 1,
                "OUTPUT": QgsProcessing.TEMPORARY_OUTPUT,
            },
        )
        search = outputs["GeometrienReparierenStreckenpuffer"]["OUTPUT"]
        buffers = {
            "LSG_LIN": "puffer_lsg_linear_m",
            "ND_PKT": "puffer_nd_punkt_m",
            "ND_LIN": "puffer_nd_linear_m",
            "GLB_PKT": "puffer_glb_pkt_m",
            "GLB_LIN": "puffer_glb_lin_m",
        }
        groups = {}
        info_layers = []
        subject_results = {}
        for spec, layer in selected:
            if feedback.isCanceled():
                return {}
            if spec["geometry"] != "Point":
                layer = run(
                    "native:fixgeometries",
                    {
                        "INPUT": layer,
                        "METHOD": 1,
                        "OUTPUT": QgsProcessing.TEMPORARY_OUTPUT,
                    },
                )["OUTPUT"]
            if spec["code"] in buffers:
                layer = run(
                    "native:buffer",
                    {
                        "INPUT": layer,
                        "DISTANCE": self.parameterAsDouble(
                            parameters, buffers[spec["code"]], context
                        ),
                        "DISSOLVE": False,
                        "END_CAP_STYLE": 0,
                        "JOIN_STYLE": 0,
                        "MITER_LIMIT": 2,
                        "SEGMENTS": 5,
                        "OUTPUT": QgsProcessing.TEMPORARY_OUTPUT,
                    },
                )["OUTPUT"]
            clipped = run(
                "native:intersection",
                {
                    "INPUT": search,
                    "OVERLAY": layer,
                    "INPUT_FIELDS": [],
                    "OVERLAY_FIELDS": [],
                    "OUTPUT": QgsProcessing.TEMPORARY_OUTPUT,
                },
            )["OUTPUT"]
            # Keep the original fachdatum attributes in the Info export.
            info_path = str(
                Path(folder_path_tmp) / f"{spec['info']}_{suffix}.shp"
            )
            cleaned = drop_existing(clipped, ["fid"])
            info_output = run(
                "native:savefeatures",
                {
                    "INPUT": cleaned,
                    "OUTPUT": info_path,
                },
            )["OUTPUT"]
            info_layers.append(info_output)
            subject_results["OUTPUT_" + spec["result_key"]] = info_output
            # Unique fields prevent union suffixes from depending on which
            # variants exist.
            weight = "weight_" + spec["code"].lower()
            weighted = run(
                "native:fieldcalculator",
                {
                    "INPUT": clipped,
                    "FIELD_NAME": weight,
                    "FIELD_TYPE": 1,
                    "FIELD_LENGTH": 10,
                    "FIELD_PRECISION": 0,
                    "FORMULA": QgsExpression.quotedColumnRef(spec["field"]),
                    "OUTPUT": QgsProcessing.TEMPORARY_OUTPUT,
                },
            )["OUTPUT"]
            weighted = run(
                "native:retainfields",
                {
                    "INPUT": weighted,
                    "FIELDS": [weight],
                    "OUTPUT": QgsProcessing.TEMPORARY_OUTPUT,
                },
            )["OUTPUT"]
            groups.setdefault(spec["field"], []).append((weighted, weight))

        outputs["InfolayerErzeugen"] = run(
            "native:package",
            {
                "LAYERS": info_layers,
                "OUTPUT": info,
                "OVERWRITE": True,
                "SAVE_STYLES": True,
                "SAVE_METADATA": True,
                "EXPORT_RELATED_LAYERS": False,
                "SELECTED_FEATURES_ONLY": False,
            },
        )
        group_layers = []
        for field, variants in groups.items():
            merged = union([layer for layer, _ in variants])
            if field in ("Wert_LSG", "Wert_ND", "Wert_GLB"):
                merged = run(
                    "giraffepro:cleanup_1",
                    {
                        "input_splinter_1": merged,
                        "output_healed_1": QgsProcessing.TEMPORARY_OUTPUT,
                    },
                )["output_healed_1"]
            maximum = run(
                "native:fieldcalculator",
                {
                    "INPUT": merged,
                    "FIELD_NAME": field,
                    "FIELD_TYPE": 1,
                    "FIELD_LENGTH": 10,
                    "FIELD_PRECISION": 0,
                    "FORMULA": maximum_expression(
                        [weight for _, weight in variants]
                    ),
                    "OUTPUT": QgsProcessing.TEMPORARY_OUTPUT,
                },
            )["OUTPUT"]
            maximum = run(
                "native:retainfields",
                {
                    "INPUT": maximum,
                    "FIELDS": [field],
                    "OUTPUT": QgsProcessing.TEMPORARY_OUTPUT,
                },
            )["OUTPUT"]
            maximum = run(
                "native:fixgeometries",
                {
                    "INPUT": maximum,
                    "METHOD": 1,
                    "OUTPUT": QgsProcessing.TEMPORARY_OUTPUT,
                },
            )["OUTPUT"]
            group_layers.append(maximum)
        outputs["VereinigenMehrere"] = {"OUTPUT": union(group_layers)}
        rating_fields = list(groups)
        tail_start = step[0]
        feedback.pushInfo(
            "Berücksichtigte Fachdaten: "
            + ", ".join(spec["code"] for spec, _ in selected)
        )
        feedback.pushInfo(
            "Nicht ausgewählte Fachdaten sind nicht Teil dieser Auswertung. "
            "Eine grüne Darstellung bestätigt keine Konfliktfreiheit."
        )

        # Splitter_bereinigen_giraffe
        alg_params = {
            "input_splinter_1": outputs["VereinigenMehrere"]["OUTPUT"],
            "output_healed_1": QgsProcessing.TEMPORARY_OUTPUT,
        }
        outputs["Splitter_bereinigen_giraffe"] = processing.run(
            "giraffepro:cleanup_1",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        feedback.setCurrentStep(tail_start + 1)
        if feedback.isCanceled():
            return {}

        # Max Wert filtern
        alg_params = {
            "FIELD_LENGTH": 0,
            "FIELD_NAME": "Bewertung",
            "FIELD_PRECISION": 0,
            "FIELD_TYPE": 1,  # Integer (32 bit)
            "FORMULA": maximum_expression(rating_fields),
            "INPUT": outputs["Splitter_bereinigen_giraffe"]["output_healed_1"],
            "OUTPUT": QgsProcessing.TEMPORARY_OUTPUT,
        }
        outputs["MaxWertFiltern"] = processing.run(
            "native:fieldcalculator",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        feedback.setCurrentStep(tail_start + 2)
        if feedback.isCanceled():
            return {}

        # Tabelle bereinigen giraffe Ergebnis
        alg_params = {
            "COLUMN": rating_fields,
            "INPUT": outputs["MaxWertFiltern"]["OUTPUT"],
            "OUTPUT": QgsProcessing.TEMPORARY_OUTPUT,
        }
        outputs["TabelleBereinigengiraffeErgebnis"] = processing.run(
            "native:deletecolumn",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        feedback.setCurrentStep(tail_start + 3)
        if feedback.isCanceled():
            return {}

        # Geometrien reparieren giraffe Ergebnis
        alg_params = {
            "INPUT": outputs["TabelleBereinigengiraffeErgebnis"]["OUTPUT"],
            "METHOD": 1,  # Structure
            "OUTPUT": QgsProcessing.TEMPORARY_OUTPUT,
        }
        outputs["GeometrienReparierengiraffeErgebnis"] = processing.run(
            "native:fixgeometries",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        feedback.setCurrentStep(tail_start + 4)
        if feedback.isCanceled():
            return {}

        # Vereinfachen giraffe Bewertung
        alg_params = {
            "FIELD": ["Bewertung"],
            "INPUT": outputs["GeometrienReparierengiraffeErgebnis"]["OUTPUT"],
            "SEPARATE_DISJOINT": False,
            "OUTPUT": QgsProcessing.TEMPORARY_OUTPUT,
        }
        outputs["VereinfachengiraffeBewertung"] = processing.run(
            "native:dissolve",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        feedback.setCurrentStep(tail_start + 5)
        if feedback.isCanceled():
            return {}

        # giraffe Ampel
        alg_params = {
            "COLUMN": ["fid"],
            "INPUT": outputs["VereinfachengiraffeBewertung"]["OUTPUT"],
            "OUTPUT": tmp_qgis_tlc,
        }
        outputs["giraffeAmpel"] = {
            "OUTPUT": drop_existing(alg_params["INPUT"], ["fid"], tmp_qgis_tlc)
        }

        feedback.setCurrentStep(tail_start + 6)
        if feedback.isCanceled():
            return {}

        # Auflösen_giraffe_Ergebnis
        alg_params = {
            "FIELD": [],
            "INPUT": outputs["GeometrienReparierengiraffeErgebnis"]["OUTPUT"],
            "SEPARATE_DISJOINT": False,
            "OUTPUT": QgsProcessing.TEMPORARY_OUTPUT,
        }
        outputs["Auflsen_giraffe_ergebnis"] = processing.run(
            "native:dissolve",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        feedback.setCurrentStep(tail_start + 7)
        if feedback.isCanceled():
            return {}

        # Layer in Projekt laden Ampel
        alg_params = {
            "INPUT": outputs["giraffeAmpel"]["OUTPUT"],
            "NAME": "gIraffePro Ampel",
        }
        outputs["LayerInProjektLadenAmpel"] = processing.run(
            "native:loadlayer",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        feedback.setCurrentStep(tail_start + 8)
        if feedback.isCanceled():
            return {}

        # Geometrien reparieren giraffe Aufgeloest
        alg_params = {
            "INPUT": outputs["Auflsen_giraffe_ergebnis"]["OUTPUT"],
            "METHOD": 1,  # Structure
            "OUTPUT": QgsProcessing.TEMPORARY_OUTPUT,
        }
        outputs["GeometrienReparierengiraffeAufgeloest"] = processing.run(
            "native:fixgeometries",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        feedback.setCurrentStep(tail_start + 9)
        if feedback.isCanceled():
            return {}

        # Infra Maps Viewer geoJson 4326
        alg_params = {
            "INPUT": outputs["giraffeAmpel"]["OUTPUT"],
            "OPERATION": None,
            "TARGET_CRS": QgsCoordinateReferenceSystem("EPSG:4326"),
            "OUTPUT": QgsProcessing.TEMPORARY_OUTPUT,
        }
        outputs["InfraMapsViewerGeojson4326"] = processing.run(
            "native:reprojectlayer",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        feedback.setCurrentStep(tail_start + 10)
        if feedback.isCanceled():
            return {}

        # Layerstil setzen Ampel
        alg_params = {
            "INPUT": outputs["LayerInProjektLadenAmpel"]["OUTPUT"],
            "STYLE": parameters["layerstil_ampel_qml"],
        }
        outputs["LayerstilSetzenAmpel"] = processing.run(
            "native:setlayerstyle",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        feedback.setCurrentStep(tail_start + 11)
        if feedback.isCanceled():
            return {}

        # Vektorobjekt in Datei speichern Streckenpuffer
        alg_params = {
            "DATASOURCE_OPTIONS": None,
            "INPUT": outputs["StreckenabschnittpufferBereinigt"]["OUTPUT"],
            "LAYER_NAME": None,
            "LAYER_OPTIONS": None,
            "OUTPUT": QgsProcessing.TEMPORARY_OUTPUT,
        }
        outputs["VektorobjektInDateiSpeichernStreckenpuffer"] = processing.run(
            "native:savefeatures",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        feedback.setCurrentStep(tail_start + 12)
        if feedback.isCanceled():
            return {}

        # Differenz Ergebnis Streckenpuffer
        alg_params = {
            "GRID_SIZE": None,
            "INPUT": outputs["GeometrienReparierenStreckenpuffer"]["OUTPUT"],
            "OUTPUT": tmp_qgis_buf,
            "OVERLAY": outputs["GeometrienReparierengiraffeAufgeloest"][
                "OUTPUT"
            ],
        }
        outputs["DifferenzErgebnisStreckenpuffer"] = processing.run(
            "native:difference",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        feedback.setCurrentStep(tail_start + 13)
        if feedback.isCanceled():
            return {}

        # giraffe Ergebnis InfraMaps
        alg_params = {
            "ACTION_ON_EXISTING_FILE": 0,  # Create or overwrite file
            "DATASOURCE_OPTIONS": None,
            "INPUT": outputs["InfraMapsViewerGeojson4326"]["OUTPUT"],
            "LAYER_NAME": None,
            "LAYER_OPTIONS": None,
            "OUTPUT": res_inframaps,
        }
        outputs["giraffeErgebnisInframaps"] = processing.run(
            "native:savefeatures",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        feedback.setCurrentStep(tail_start + 14)
        if feedback.isCanceled():
            return {}

        # Abfrageraum QGIS
        alg_params = {
            "INPUT": outputs["VektorobjektInDateiSpeichernStreckenpuffer"][
                "OUTPUT"
            ],
            "OUTPUT": tmp_qgis_lim,
        }
        outputs["AbfrageraumQgis"] = processing.run(
            "native:polygonstolines",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        feedback.setCurrentStep(tail_start + 15)
        if feedback.isCanceled():
            return {}

        # Layer reprojizieren 3857 giraffe Ergebnis
        alg_params = {
            "INPUT": outputs["giraffeErgebnisInframaps"]["OUTPUT"],
            "OPERATION": None,
            "TARGET_CRS": QgsCoordinateReferenceSystem("EPSG:3857"),
            "OUTPUT": QgsProcessing.TEMPORARY_OUTPUT,
        }
        outputs["LayerReprojizieren3857giraffeErgebnis"] = processing.run(
            "native:reprojectlayer",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        feedback.setCurrentStep(tail_start + 16)
        if feedback.isCanceled():
            return {}

        # Mehr- zu einteilig Abfrageraum
        alg_params = {
            "INPUT": outputs["AbfrageraumQgis"]["OUTPUT"],
            "OUTPUT": QgsProcessing.TEMPORARY_OUTPUT,
        }
        outputs["MehrZuEinteiligAbfrageraum"] = processing.run(
            "native:multiparttosingleparts",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        feedback.setCurrentStep(tail_start + 17)
        if feedback.isCanceled():
            return {}

        # Layer in Projekt laden Abfragegrenze
        alg_params = {
            "INPUT": outputs["AbfrageraumQgis"]["OUTPUT"],
            "NAME": "Abfragegrenze",
        }
        outputs["LayerInProjektLadenAbfragegrenze"] = processing.run(
            "native:loadlayer",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        feedback.setCurrentStep(tail_start + 18)
        if feedback.isCanceled():
            return {}

        # Layer in Projekt laden keine Kollision
        alg_params = {
            "INPUT": outputs["DifferenzErgebnisStreckenpuffer"]["OUTPUT"],
            "NAME": "gIraffePro - keine Überlagerung ausgewählter Fachdaten",
        }
        outputs["LayerInProjektLadenKeineKollision"] = processing.run(
            "native:loadlayer",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        feedback.setCurrentStep(tail_start + 19)
        if feedback.isCanceled():
            return {}

        # Mehr- zu einteilig X2BIM
        alg_params = {
            "INPUT": outputs["LayerReprojizieren3857giraffeErgebnis"][
                "OUTPUT"
            ],
            "OUTPUT": QgsProcessing.TEMPORARY_OUTPUT,
        }
        outputs["MehrZuEinteiligX2bim"] = processing.run(
            "native:multiparttosingleparts",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        feedback.setCurrentStep(tail_start + 20)
        if feedback.isCanceled():
            return {}

        # Abfrageraum X2BIM
        alg_params = {
            "CONVERT_CURVED_GEOMETRIES": False,
            "INPUT": outputs["MehrZuEinteiligAbfrageraum"]["OUTPUT"],
            "OPERATION": None,
            "OUTPUT": res_x2bim_lim,
            "TARGET_CRS": QgsCoordinateReferenceSystem("EPSG:3857"),
        }
        outputs["AbfrageraumX2bim"] = processing.run(
            "native:reprojectlayer",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        feedback.setCurrentStep(tail_start + 21)
        if feedback.isCanceled():
            return {}

        # giraffe Ergebnis QGIS
        alg_params = {
            "EXPORT_RELATED_LAYERS": False,
            "LAYERS": [
                outputs["giraffeAmpel"]["OUTPUT"],
                outputs["DifferenzErgebnisStreckenpuffer"]["OUTPUT"],
                outputs["AbfrageraumQgis"]["OUTPUT"],
            ],
            "OUTPUT": res_qgis,
            "OVERWRITE": False,
            "SAVE_METADATA": True,
            "SAVE_STYLES": True,
            "SELECTED_FEATURES_ONLY": False,
        }
        outputs["giraffeErgebnisQgis"] = processing.run(
            "native:package",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        feedback.setCurrentStep(tail_start + 22)
        if feedback.isCanceled():
            return {}

        # Nach Attribut extrahieren - gelb
        alg_params = {
            "FIELD": "Bewertung",
            "INPUT": outputs["MehrZuEinteiligX2bim"]["OUTPUT"],
            "OPERATOR": 0,  # =
            "VALUE": "2",
            "OUTPUT": QgsProcessing.TEMPORARY_OUTPUT,
        }
        outputs["NachAttributExtrahierenGelb"] = processing.run(
            "native:extractbyattribute",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        feedback.setCurrentStep(tail_start + 23)
        if feedback.isCanceled():
            return {}

        # Splitter_bereinigen_gelb
        alg_params = {
            "OUTPUT": res_x2bim_yel,
            "input_splinter_2": outputs["NachAttributExtrahierenGelb"][
                "OUTPUT"
            ],
        }
        outputs["Splitter_bereinigen_gelb"] = processing.run(
            "giraffepro:cleanup_2",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        feedback.setCurrentStep(tail_start + 24)
        if feedback.isCanceled():
            return {}

        # Layerstil setzen KK
        alg_params = {
            "INPUT": outputs["LayerInProjektLadenKeineKollision"]["OUTPUT"],
            "STYLE": parameters["layerstil_ampel_qml"],
        }
        outputs["LayerstilSetzenKk"] = processing.run(
            "native:setlayerstyle",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        feedback.setCurrentStep(tail_start + 25)
        if feedback.isCanceled():
            return {}

        # Layerstil setzen
        alg_params = {
            "INPUT": outputs["LayerInProjektLadenAbfragegrenze"]["OUTPUT"],
            "STYLE": parameters["layerstil_abfraggrenze_qml"],
        }
        outputs["LayerstilSetzen"] = processing.run(
            "native:setlayerstyle",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        feedback.setCurrentStep(tail_start + 26)
        if feedback.isCanceled():
            return {}

        # Abfrageraum Inframaps
        alg_params = {
            "CONVERT_CURVED_GEOMETRIES": False,
            "INPUT": outputs["AbfrageraumX2bim"]["OUTPUT"],
            "OPERATION": None,
            "OUTPUT": res_inframaps_lim,
            "TARGET_CRS": QgsCoordinateReferenceSystem("EPSG:4326"),
        }
        outputs["AbfrageraumInframaps"] = processing.run(
            "native:reprojectlayer",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        feedback.setCurrentStep(tail_start + 27)
        if feedback.isCanceled():
            return {}

        # Nach Attribut extrahieren rot
        alg_params = {
            "FIELD": "Bewertung",
            "INPUT": outputs["MehrZuEinteiligX2bim"]["OUTPUT"],
            "OPERATOR": 0,  # =
            "VALUE": "3",
            "OUTPUT": QgsProcessing.TEMPORARY_OUTPUT,
        }
        outputs["NachAttributExtrahierenRot"] = processing.run(
            "native:extractbyattribute",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        feedback.setCurrentStep(tail_start + 28)
        if feedback.isCanceled():
            return {}

        # Nach Attribut extrahieren gruen
        alg_params = {
            "FIELD": "Bewertung",
            "INPUT": outputs["MehrZuEinteiligX2bim"]["OUTPUT"],
            "OPERATOR": 0,  # =
            "VALUE": "1",
            "OUTPUT": QgsProcessing.TEMPORARY_OUTPUT,
        }
        outputs["NachAttributExtrahierenGruen"] = processing.run(
            "native:extractbyattribute",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        feedback.setCurrentStep(tail_start + 29)
        if feedback.isCanceled():
            return {}

        # Splitter_bereinigen_rot
        alg_params = {
            "OUTPUT": res_x2bim_red,
            "input_splinter_2": outputs["NachAttributExtrahierenRot"][
                "OUTPUT"
            ],
        }
        outputs["Splitter_bereinigen_rot"] = processing.run(
            "giraffepro:cleanup_2",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        feedback.setCurrentStep(tail_start + 30)
        if feedback.isCanceled():
            return {}

        # Splitter_bereinigen_gruen
        alg_params = {
            "OUTPUT": res_x2bim_gre,
            "input_splinter_2": outputs["NachAttributExtrahierenGruen"][
                "OUTPUT"
            ],
        }
        outputs["Splitter_bereinigen_gruen"] = processing.run(
            "giraffepro:cleanup_2",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        results["OUTPUT_InfolayerErzeugen"] = info
        results["OUTPUT_AbfrageraumX2bim"] = res_x2bim_lim
        results["OUTPUT_Splitter_bereinigen_gelb"] = res_x2bim_yel
        results["OUTPUT_Splitter_bereinigen_rot"] = res_x2bim_red
        results["OUTPUT_Splitter_bereinigen_gruen"] = res_x2bim_gre
        results["OUTPUT_giraffeErgebnisInframaps"] = res_inframaps
        results["OUTPUT_AbfrageraumInframaps"] = res_inframaps_lim
        results["OUTPUT_giraffeErgebnisQgis"] = res_qgis
        results["OUTPUT_giraffeAmpel"] = tmp_qgis_tlc
        results["OUTPUT_DifferenzErgebnisStreckenpuffer"] = tmp_qgis_buf
        results["OUTPUT_AbfrageraumQgis"] = tmp_qgis_lim
        results.update(subject_results)
        return results

    def name(self):
        return "giraffe_main"

    def displayName(self):
        return (
            "Green Infrastructure fast filter and estimation Project "
            "(gIraffePro)"
        )

    def group(self):
        return "Verarbeitung"

    def groupId(self):
        return "verarbeitung"

    def shortHelpString(self):
        return (
            '<html><body><p><!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" '
            '"http://www.w3.org/TR/REC-html40/strict.dtd">\n<html><head><meta '
            'name="qrichtext" content="1" /><style '
            'type="text/css">\n</style></head><body style=" '
            "font-family:'Sans Serif'; font-size:9pt; font-weight:400; "
            'font-style:normal;">\n<p style=" margin-top:0px; '
            "margin-bottom:0px; margin-left:0px; margin-right:0px; "
            '-qt-block-indent:0; text-indent:0px;">Die deutsche '
            "Naturschutzgesetzgebung differenziert Flächen und Objekte nach "
            "ihrem Schutzstatus. Viele dieser Geometrien sind Teil einer "
            "grünen Infrastruktur und werden von den Behörden als "
            "Gendateninfrastruktur bereit gestellt. Das planerische Gewicht "
            "der beauflagten Flächen steigt stetig. Eine frühe Kenntnis "
            "vorhandener Restriktionen trägt maßgeblich zum Projekterfolg "
            "bei.\n\nDie Datengrundlage ist jedoch ebenso umfangreich wie "
            "vielfältig. Und oft auch erheblich fragmentiert. Zudem ist "
            "naturschutzfachlicher Sachverstand in der Regel in die erste "
            "Ideenskizzen eines Infrastrukturprojektes noch nicht "
            "eingebunden.\nDas Green Infrastructure fast filtering and "
            "estimation project verwendet nach Ampellogik vorklassifizierte "
            "Datensätze beauflagter Flächen und dünnt landesweite "
            "Flickenteppiche anhand variabler Puffer aus. Das Ergebnis "
            "ermöglicht Planern und Projektsteuerern eine schnelle, "
            "überschlägige Einschätzung vorhandener Zugriffshürden - "
            "gIraffePro vermeidet und minimiert Konfliktpotenzial von Beginn "
            "an. </p>\n<br>\n<h2>Eingaben</h2>\n<h3>Projektachse</h3>\n<p>Achs"
            "e einer Linienbaustelle. (Liniengeometrie)</p>\n<h3>Suchraum "
            "(m)</h3>\n<p>Suchraum des Vorhabens beidseitig der "
            "Achse</p>\n<h3>Fachdatensätze</h3>\n<p>Alle Fachdateneingaben "
            "sind optional. Mindestens ein Datensatz aus den Eingaben 1 bis "
            "11 ist erforderlich. Nur ausgewählte Fachdaten werden "
            "verarbeitet und im Info-Layer ausgegeben. Nicht ausgewählte "
            "Daten sind nicht Teil der Aussage. Die §30-Eingaben 12 bis 14 "
            "sind in diesem Arbeitsablauf weiterhin nicht "
            "ausgewertet.</p>\n<p>Bestandteile der grünen INfrastruktur: FFH "
            "und SPA Gebiete, Landschaftsschutzgebiete, Naturschuitzgebiete, "
            "Naturdenkmäler und geschützte Landschaftsbestandteile. Punkt und "
            "Liniendatensätze benötigen einen Puffer. Die EIngangsdaten "
            "müssen über Werfelder verfügen, die der gIraffePro-Logik "
            "entsprechen.</p>\n<h3>Ampelstil</h3>\n<p>gIraffePro-Layerstil "
            "(*.qml) in Ampellogik</p>\n<h3>Stil der "
            "Abfragegrenze</h3>\n<p>gIraffePro-Layerstil (*.qml) der "
            "Abfragegrenze</p>\n<h3>Strecke</h3>\n<p>Bezeichnung des "
            "Berzugsraumes</p>\n<h3>gIraffePro "
            "Ergebnis</h3>\n<p>Ausgabeordner der Ampellogik. Speicherort für "
            "bewertete Flächen mit Restriktionen, Abfragegrenze, Flächen ohne "
            "Restriktionen. Ausgegeben werden Datensätze zur Verwendung in "
            "X2Bim (Plattform der DB E&C), InfraMaps (Plattform der DB "
            "InfraGo) und zur Verwendung in QGis. Für die beiden "
            "Projektarbeitsviewer werden Suchraumgrenzen und "
            "Flächengeometrieen der Ampellogik separat voneinander generiert. "
            "</p>\n<h3>gIraffePro Info Layer</h3>\n<p>Ausgabeordner des Info "
            "Layers (ggpkg, EPSG 25832). Speicherort für Detailinfos zu den "
            "bewerteten Schutzgebieten und Objekten. </p>\n<h3>temporäre "
            "Dateien</h3>\n<p>Kontrolldateien, die bei Ablauf des "
            "Arbeitsprozesses erstellt werden</p>\n<p "
            'style="-qt-paragraph-type:empty; margin-top:0px; '
            "margin-bottom:0px; margin-left:0px; margin-right:0px; "
            '-qt-block-indent:0; text-indent:0px;"><br '
            '/></p></body></html></p>\n<p align="right">Algorithm version: '
            "1.0</p></body></html>"
        )

    def createInstance(self):
        return GreenInfrastructureFFEProject()
