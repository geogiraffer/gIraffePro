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
Name : GIraffePro_Fachdatenbewertung
Group : gIraffePro
With QGIS : 34407
"""

from typing import Any, Optional

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingContext
from qgis.core import QgsProcessingFeedback, QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterString
from qgis.core import QgsProcessingParameterFile
from qgis.core import QgsProcessingOutputVectorLayer
from qgis.PyQt.QtGui import QIcon
from pathlib import Path
from qgis import processing


class Giraffepro_fachdatenbewertung(QgsProcessingAlgorithm):

    def initAlgorithm(self, config: Optional[dict[str, Any]] = None):
        self.addParameter(QgsProcessingParameterVectorLayer('_ffh_geometrie', '1. FFH Geometrie', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('_ffh_bewertung_13', '1. FFH Bewertung (1-3)', type=QgsProcessingParameterNumber.Integer, minValue=1, maxValue=3, defaultValue=3))
        self.addParameter(QgsProcessingParameterVectorLayer('_lsg_geometrie', '2. LSG Geometrie', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('_lsg_bewertung_13', '2. LSG Bewertung (1-3)', type=QgsProcessingParameterNumber.Integer, minValue=1, maxValue=3, defaultValue=1))
        self.addParameter(QgsProcessingParameterVectorLayer('_lsg_geometrie_lin', '3. LSG Geometrie (lin)', types=[QgsProcessing.TypeVectorLine], defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('_lsg_lin_bewertung_13', '3. LSG lin Bewertung (1-3)', type=QgsProcessingParameterNumber.Integer, minValue=1, maxValue=3, defaultValue=1))
        self.addParameter(QgsProcessingParameterVectorLayer('_nd_geometrie_pkt', '4. ND Geometrie (pkt)', types=[QgsProcessing.TypeVectorPoint], defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('_nd_pkt_bewertung_13', '4. ND pkt Bewertung (1-3)', type=QgsProcessingParameterNumber.Integer, minValue=1, maxValue=3, defaultValue=3))
        self.addParameter(QgsProcessingParameterVectorLayer('_nd_geometrie_lin', '5. ND Geometrie (lin)', types=[QgsProcessing.TypeVectorLine], defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('_nd_lin_bewertung_13', '5. ND lin Bewertung (1-3)', type=QgsProcessingParameterNumber.Integer, minValue=1, maxValue=3, defaultValue=3))
        self.addParameter(QgsProcessingParameterVectorLayer('_nd_geometrie', '6. ND Geometrie', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('_nd_bewertung_13', '6. ND Bewertung (1-3)', type=QgsProcessingParameterNumber.Integer, minValue=1, maxValue=3, defaultValue=3))
        self.addParameter(QgsProcessingParameterVectorLayer('_spa_geometrie', '7. SPA Geometrie', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('_spa_bewertung_13', '7. SPA Bewertung (1-3)', type=QgsProcessingParameterNumber.Integer, minValue=1, maxValue=3, defaultValue=3))
        self.addParameter(QgsProcessingParameterVectorLayer('_nsg_geometrie', '8. NSG Geometrie', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('_nsg_bewertung_13', '8. NSG Bewertung (1-3)', type=QgsProcessingParameterNumber.Integer, minValue=1, maxValue=3, defaultValue=2))
        self.addParameter(QgsProcessingParameterVectorLayer('_glb_geometrie_pkt', '9. GLB Geometrie (pkt)', types=[QgsProcessing.TypeVectorPoint], defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('_glb_pkt_bewertung_13', '9. GLB pkt Bewertung (1-3)', type=QgsProcessingParameterNumber.Integer, minValue=1, maxValue=3, defaultValue=2))
        self.addParameter(QgsProcessingParameterVectorLayer('_glb_geometrie_lin', '10. GLB Geometrie (lin)', types=[QgsProcessing.TypeVectorLine], defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('_glb_lin_bewertung_13', '10. GLB lin Bewertung (1-3)', type=QgsProcessingParameterNumber.Integer, minValue=1, maxValue=3, defaultValue=2))
        self.addParameter(QgsProcessingParameterVectorLayer('_glb_geometrie', '11. GLB Geometrie', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('_glb_bewertung_13', '11. GLB Bewertung (1-3)', type=QgsProcessingParameterNumber.Integer, minValue=1, maxValue=3, defaultValue=2))
        self.addParameter(QgsProcessingParameterString('bundesland_zb_ni_ffh_sh', 'Bundesland (z.B. Ni, FFH, SH...)', multiLine=False, defaultValue='Ni'))
        self.addParameter(QgsProcessingParameterFile('giraffepro_ordner', 'gIraffePro_Ordner', behavior=QgsProcessingParameterFile.Folder, fileFilter='Alle Dateien (*.*)', defaultValue=None))

        self.addOutput(QgsProcessingOutputVectorLayer('OUTPUT_FFH', 'FFH bewertet'))
        self.addOutput(QgsProcessingOutputVectorLayer('OUTPUT_LSG', 'LSG bewertet'))
        self.addOutput(QgsProcessingOutputVectorLayer('OUTPUT_LSG_LIN', 'LSG LIN bewertet'))
        self.addOutput(QgsProcessingOutputVectorLayer('OUTPUT_ND_PKT', 'ND PKT bewertet'))
        self.addOutput(QgsProcessingOutputVectorLayer('OUTPUT_ND_LIN', 'ND LIN bewertet'))
        self.addOutput(QgsProcessingOutputVectorLayer('OUTPUT_ND', 'ND bewertet'))
        self.addOutput(QgsProcessingOutputVectorLayer('OUTPUT_SPA', 'SPA bewertet'))
        self.addOutput(QgsProcessingOutputVectorLayer('OUTPUT_NSG', 'NSG bewertet'))
        self.addOutput(QgsProcessingOutputVectorLayer('OUTPUT_GLB_PKT', 'GLB PKT bewertet'))
        self.addOutput(QgsProcessingOutputVectorLayer('OUTPUT_GLB_LIN', 'GLB LIN bewertet'))
        self.addOutput(QgsProcessingOutputVectorLayer('OUTPUT_GLB', 'GLB bewertet'))

    def processAlgorithm(self, parameters: dict[str, Any], context: QgsProcessingContext, model_feedback: QgsProcessingFeedback) -> dict[str, Any]:
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(20, model_feedback)
        results = {}
        outputs = {}
        output_dir = Path(self.parameterAsFile(parameters, 'giraffepro_ordner', context))
        bundesland = self.parameterAsString(parameters, 'bundesland_zb_ni_ffh_sh', context)


        # Geometrien reparieren GLB
        alg_params = {
            'INPUT': parameters['_glb_geometrie'],
            'METHOD': 1,  # Structure
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['GeometrienReparierenGlb'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Geometrien reparieren FFH
        alg_params = {
            'INPUT': parameters['_ffh_geometrie'],
            'METHOD': 1,  # Structure
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['GeometrienReparierenFfh'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Feldrechner FFH
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Wert_FFH',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer (32 bit)
            'FORMULA': str(parameters['_ffh_bewertung_13']),
            'INPUT': outputs['GeometrienReparierenFfh']['OUTPUT'],
            'OUTPUT': str(output_dir / ('gIraffePro_FFH_' + bundesland + '.geojson'))
        }
        outputs['FeldrechnerFfh'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Feldrechner GLB
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Wert_GLB',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer (32 bit)
            'FORMULA': str(parameters['_glb_bewertung_13']),
            'INPUT': outputs['GeometrienReparierenGlb']['OUTPUT'],
            'OUTPUT': str(output_dir / ('gIraffePro_GLB_' + bundesland + '.geojson'))
        }
        outputs['FeldrechnerGlb'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Geometrien reparieren NSG
        alg_params = {
            'INPUT': parameters['_nsg_geometrie'],
            'METHOD': 1,  # Structure
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['GeometrienReparierenNsg'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Feldrechner GLB pkt
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Wert_GLB',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer (32 bit)
            'FORMULA': str(parameters['_glb_pkt_bewertung_13']),
            'INPUT': parameters['_glb_geometrie_pkt'],
            'OUTPUT': str(output_dir / ('gIraffePro_GLB_PKT_' + bundesland + '.geojson'))
        }
        outputs['FeldrechnerGlbPkt'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Geometrien reparieren LSG lin
        alg_params = {
            'INPUT': parameters['_lsg_geometrie_lin'],
            'METHOD': 1,  # Structure
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['GeometrienReparierenLsgLin'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Geometrien reparieren ND lin
        alg_params = {
            'INPUT': parameters['_nd_geometrie_lin'],
            'METHOD': 1,  # Structure
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['GeometrienReparierenNdLin'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Feldrechner NSG
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Wert_NSG',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer (32 bit)
            'FORMULA': str(parameters['_nsg_bewertung_13']),
            'INPUT': outputs['GeometrienReparierenNsg']['OUTPUT'],
            'OUTPUT': str(output_dir / ('gIraffePro_NSG_' + bundesland + '.geojson'))
        }
        outputs['FeldrechnerNsg'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Geometrien reparieren ND
        alg_params = {
            'INPUT': parameters['_nd_geometrie'],
            'METHOD': 1,  # Structure
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['GeometrienReparierenNd'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # Feldrechner ND lin
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Wert_ND',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer (32 bit)
            'FORMULA': str(parameters['_nd_lin_bewertung_13']),
            'INPUT': outputs['GeometrienReparierenNdLin']['OUTPUT'],
            'OUTPUT': str(output_dir / ('gIraffePro_ND_LIN_' + bundesland + '.geojson'))
        }
        outputs['FeldrechnerNdLin'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # Feldrechner ND pkt
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Wert_ND',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer (32 bit)
            'FORMULA': str(parameters['_nd_pkt_bewertung_13']),
            'INPUT': parameters['_nd_geometrie_pkt'],
            'OUTPUT': str(output_dir / ('gIraffePro_ND_PKT_' + bundesland + '.geojson'))
        }
        outputs['FeldrechnerNdPkt'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}

        # Geometrien reparieren GLB lin
        alg_params = {
            'INPUT': parameters['_glb_geometrie_lin'],
            'METHOD': 1,  # Structure
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['GeometrienReparierenGlbLin'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        # Geometrien reparieren SPA
        alg_params = {
            'INPUT': parameters['_spa_geometrie'],
            'METHOD': 1,  # Structure
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['GeometrienReparierenSpa'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}

        # Geometrien reparieren LSG
        alg_params = {
            'INPUT': parameters['_lsg_geometrie'],
            'METHOD': 1,  # Structure
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['GeometrienReparierenLsg'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        # Feldrechner SPA
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Wert_SPA',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer (32 bit)
            'FORMULA': str(parameters['_spa_bewertung_13']),
            'INPUT': outputs['GeometrienReparierenSpa']['OUTPUT'],
            'OUTPUT': str(output_dir / ('gIraffePro_SPA_' + bundesland + '.geojson'))
        }
        outputs['FeldrechnerSpa'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}

        # Feldrechner LSG
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Wert_LSG',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer (32 bit)
            'FORMULA': str(parameters['_lsg_bewertung_13']),
            'INPUT': outputs['GeometrienReparierenLsg']['OUTPUT'],
            'OUTPUT': str(output_dir / ('gIraffePro_LSG_' + bundesland + '.geojson'))
        }
        outputs['FeldrechnerLsg'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}

        # Feldrechner LSG lin
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Wert_LSG',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer (32 bit)
            'FORMULA': str(parameters['_lsg_lin_bewertung_13']),
            'INPUT': outputs['GeometrienReparierenLsgLin']['OUTPUT'],
            'OUTPUT': str(output_dir / ('gIraffePro_LSG_LIN_' + bundesland + '.geojson'))
        }
        outputs['FeldrechnerLsgLin'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}

        # Feldrechner ND
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Wert_ND',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer (32 bit)
            'FORMULA': str(parameters['_nd_bewertung_13']),
            'INPUT': outputs['GeometrienReparierenNd']['OUTPUT'],
            'OUTPUT': str(output_dir / ('gIraffePro_ND_' + bundesland + '.geojson'))
        }
        outputs['FeldrechnerNd'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(19)
        if feedback.isCanceled():
            return {}

        # Feldrechner GLB lin
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Wert_GLB',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer (32 bit)
            'FORMULA': str(parameters['_glb_lin_bewertung_13']),
            'INPUT': outputs['GeometrienReparierenGlbLin']['OUTPUT'],
            'OUTPUT': str(output_dir / ('gIraffePro_GLB_LIN_' + bundesland + '.geojson'))
        }
        outputs['FeldrechnerGlbLin'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['OUTPUT_FFH'] = outputs['FeldrechnerFfh']['OUTPUT']
        results['OUTPUT_LSG'] = outputs['FeldrechnerLsg']['OUTPUT']
        results['OUTPUT_LSG_LIN'] = outputs['FeldrechnerLsgLin']['OUTPUT']
        results['OUTPUT_ND_PKT'] = outputs['FeldrechnerNdPkt']['OUTPUT']
        results['OUTPUT_ND_LIN'] = outputs['FeldrechnerNdLin']['OUTPUT']
        results['OUTPUT_ND'] = outputs['FeldrechnerNd']['OUTPUT']
        results['OUTPUT_SPA'] = outputs['FeldrechnerSpa']['OUTPUT']
        results['OUTPUT_NSG'] = outputs['FeldrechnerNsg']['OUTPUT']
        results['OUTPUT_GLB_PKT'] = outputs['FeldrechnerGlbPkt']['OUTPUT']
        results['OUTPUT_GLB_LIN'] = outputs['FeldrechnerGlbLin']['OUTPUT']
        results['OUTPUT_GLB'] = outputs['FeldrechnerGlb']['OUTPUT']
        return results

    def icon(self):
        return QIcon(str(Path(__file__).parent.parent / 'logo_fachdatenbewertung.png'))

    def shortHelpString(self):
        return ('Bewertet Fachdaten mit jeweils einem Wert von 1 bis 3. '
                'Linien- und Flächengeometrien werden vorher repariert. '
                'Die Geojson-Dateien werden im gewählten gIraffePro-Ordner gespeichert. '
                'Dateinamen enthalten die Fachdatenart und das eingegebene Bundesland.')

    def name(self) -> str:
        return 'fachdatenbewertung'

    def displayName(self) -> str:
        return 'Fachdatenbewertung'

    def group(self) -> str:
        return 'Vorbereitung'

    def groupId(self) -> str:
        return 'vorbereitung'

    def createInstance(self):
        return self.__class__()
