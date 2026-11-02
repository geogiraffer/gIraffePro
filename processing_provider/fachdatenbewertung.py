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

from qgis.core import QgsProcessing, QgsProcessingException
from .fachdaten_schema import selected_datasets
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
        self.addParameter(QgsProcessingParameterVectorLayer('_ffh_geometrie', '1. FFH Geometrie', types=[QgsProcessing.TypeVectorPolygon], optional=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('_ffh_bewertung_13', '1. FFH Bewertung (1-3)', type=QgsProcessingParameterNumber.Integer, minValue=1, maxValue=3, defaultValue=3))
        self.addParameter(QgsProcessingParameterVectorLayer('_lsg_geometrie', '2. LSG Geometrie', types=[QgsProcessing.TypeVectorPolygon], optional=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('_lsg_bewertung_13', '2. LSG Bewertung (1-3)', type=QgsProcessingParameterNumber.Integer, minValue=1, maxValue=3, defaultValue=1))
        self.addParameter(QgsProcessingParameterVectorLayer('_lsg_geometrie_lin', '3. LSG Geometrie (lin)', types=[QgsProcessing.TypeVectorLine], optional=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('_lsg_lin_bewertung_13', '3. LSG lin Bewertung (1-3)', type=QgsProcessingParameterNumber.Integer, minValue=1, maxValue=3, defaultValue=1))
        self.addParameter(QgsProcessingParameterVectorLayer('_nd_geometrie_pkt', '4. ND Geometrie (pkt)', types=[QgsProcessing.TypeVectorPoint], optional=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('_nd_pkt_bewertung_13', '4. ND pkt Bewertung (1-3)', type=QgsProcessingParameterNumber.Integer, minValue=1, maxValue=3, defaultValue=3))
        self.addParameter(QgsProcessingParameterVectorLayer('_nd_geometrie_lin', '5. ND Geometrie (lin)', types=[QgsProcessing.TypeVectorLine], optional=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('_nd_lin_bewertung_13', '5. ND lin Bewertung (1-3)', type=QgsProcessingParameterNumber.Integer, minValue=1, maxValue=3, defaultValue=3))
        self.addParameter(QgsProcessingParameterVectorLayer('_nd_geometrie', '6. ND Geometrie', types=[QgsProcessing.TypeVectorPolygon], optional=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('_nd_bewertung_13', '6. ND Bewertung (1-3)', type=QgsProcessingParameterNumber.Integer, minValue=1, maxValue=3, defaultValue=3))
        self.addParameter(QgsProcessingParameterVectorLayer('_spa_geometrie', '7. SPA Geometrie', types=[QgsProcessing.TypeVectorPolygon], optional=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('_spa_bewertung_13', '7. SPA Bewertung (1-3)', type=QgsProcessingParameterNumber.Integer, minValue=1, maxValue=3, defaultValue=3))
        self.addParameter(QgsProcessingParameterVectorLayer('_nsg_geometrie', '8. NSG Geometrie', types=[QgsProcessing.TypeVectorPolygon], optional=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('_nsg_bewertung_13', '8. NSG Bewertung (1-3)', type=QgsProcessingParameterNumber.Integer, minValue=1, maxValue=3, defaultValue=2))
        self.addParameter(QgsProcessingParameterVectorLayer('_glb_geometrie_pkt', '9. GLB Geometrie (pkt)', types=[QgsProcessing.TypeVectorPoint], optional=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('_glb_pkt_bewertung_13', '9. GLB pkt Bewertung (1-3)', type=QgsProcessingParameterNumber.Integer, minValue=1, maxValue=3, defaultValue=2))
        self.addParameter(QgsProcessingParameterVectorLayer('_glb_geometrie_lin', '10. GLB Geometrie (lin)', types=[QgsProcessing.TypeVectorLine], optional=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('_glb_lin_bewertung_13', '10. GLB lin Bewertung (1-3)', type=QgsProcessingParameterNumber.Integer, minValue=1, maxValue=3, defaultValue=2))
        self.addParameter(QgsProcessingParameterVectorLayer('_glb_geometrie', '11. GLB Geometrie', types=[QgsProcessing.TypeVectorPolygon], optional=True, defaultValue=None))
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

    def checkParameterValues(self, parameters, context):
        valid, message = super().checkParameterValues(parameters, context)
        if not valid:
            return valid, message
        try:
            selected_datasets(self, parameters, context, 'prepare')
        except QgsProcessingException as error:
            return False, str(error)
        return True, ''

    def processAlgorithm(self, parameters, context, model_feedback):
        selected = selected_datasets(self, parameters, context, 'prepare')
        feedback = QgsProcessingMultiStepFeedback(len(selected) * 2, model_feedback)
        results = {}
        output_dir = Path(self.parameterAsFile(parameters, 'giraffepro_ordner', context))
        bundesland = self.parameterAsString(parameters, 'bundesland_zb_ni_ffh_sh', context)
        for index, (spec, layer) in enumerate(selected):
            feedback.setCurrentStep(index * 2)
            if feedback.isCanceled():
                return {}
            if spec['geometry'] != 'Point':
                layer = processing.run('native:fixgeometries', {
                    'INPUT': layer, 'METHOD': 1, 'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT,
                }, context=context, feedback=feedback, is_child_algorithm=True)['OUTPUT']
            feedback.setCurrentStep(index * 2 + 1)
            if feedback.isCanceled():
                return {}
            rating = self.parameterAsInt(parameters, spec['weight'], context)
            output = processing.run('native:fieldcalculator', {
                'FIELD_LENGTH': 10, 'FIELD_NAME': spec['field'],
                'FIELD_PRECISION': 0, 'FIELD_TYPE': 1, 'FORMULA': str(rating),
                'INPUT': layer,
                'OUTPUT': str(output_dir / f"gIraffePro_{spec['code']}_{bundesland}.geojson"),
            }, context=context, feedback=feedback, is_child_algorithm=True)
            results['OUTPUT_' + spec['code']] = output['OUTPUT']
        return results

    def icon(self):
        return QIcon(str(Path(__file__).parent.parent / 'logo_fachdatenbewertung.png'))

    def shortHelpString(self):
        return ('Alle Fachdateneingaben sind optional; mindestens ein Datensatz ist erforderlich. '
                'Nicht ausgewählte Fachdaten werden übersprungen. '
                'Bewertet Fachdaten mit jeweils einem Wert von 1 bis 3. '
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
