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
Name : cleanup_2
Group : GIraffePro
With QGIS : 34001
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.PyQt.QtGui import QIcon
from pathlib import Path
import processing


class cleanup_2(QgsProcessingAlgorithm):
    def icon(self): return QIcon(str(Path(__file__).parent.parent / "logo_giraffe.png"))

    def flags(self):
        return (super().flags()
                | QgsProcessingAlgorithm.FlagHideFromToolbox
                | QgsProcessingAlgorithm.FlagHideFromModeler)

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('input_splinter_2', 'input_splinter_2', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('output_healed_2', 'output_healed_2', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=QgsProcessing.TEMPORARY_OUTPUT))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(3, model_feedback)
        results = {}
        outputs = {}

        # Puffer positiv
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 3,
            'END_CAP_STYLE': 2,  # Square
            'INPUT': self.parameterAsVectorLayer(parameters, 'input_splinter_2', context),
            'JOIN_STYLE': 1,  # Miter
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['PufferPositiv'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Puffer_negativ
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': -3,
            'END_CAP_STYLE': 2,  # Square
            'INPUT': outputs['PufferPositiv']['OUTPUT'],
            'JOIN_STYLE': 1,  # Miter
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Puffer_negativ'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Geometrie_reparieren
        alg_params = {
            'INPUT': outputs['Puffer_negativ']['OUTPUT'],
            'METHOD': 1,  # Structure
            'OUTPUT': parameters.get('output_healed_2', QgsProcessing.TEMPORARY_OUTPUT),
        }
        outputs['Geometrie_reparieren'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['output_healed_2'] = outputs['Geometrie_reparieren']['OUTPUT']
        return results

    def name(self):
        return 'cleanup_2'

    def displayName(self):
        return 'cleanup_2'

    def group(self):
        return 'gIraffePro'

    def groupId(self):
        return 'gIraffePro'

    def createInstance(self):
        return cleanup_2()
