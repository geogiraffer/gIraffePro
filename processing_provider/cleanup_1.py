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
Name : cleanup_1
Group : GIraffePro
With QGIS : 34001
"""

from qgis.core import Qgis
from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.PyQt.QtGui import QIcon
from pathlib import Path
import processing


class cleanup_1(QgsProcessingAlgorithm):
    def icon(self):
        return QIcon(str(Path(__file__).parent.parent / "logo_giraffe.png"))

    def flags(self):
        return (
            super().flags()
            | Qgis.ProcessingAlgorithmFlag.HideFromToolbox
            | Qgis.ProcessingAlgorithmFlag.HideFromModeler
        )

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                "input_splinter_1",
                "input_splinter_1",
                types=[Qgis.ProcessingSourceType.VectorPolygon],
                defaultValue=None,
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                "output_healed_1",
                "output_healed_1",
                type=Qgis.ProcessingSourceType.VectorAnyGeometry,
                createByDefault=True,
                supportsAppend=True,
                defaultValue=QgsProcessing.TEMPORARY_OUTPUT,
            )
        )

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm
        # progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(5, model_feedback)
        results = {}
        outputs = {}

        # Splitter Erkennen
        alg_params = {
            "FIELD_LENGTH": 0,
            "FIELD_NAME": "area",
            "FIELD_PRECISION": 0,
            "FIELD_TYPE": 1,  # Integer (32 bit)
            "FORMULA": "$area",
            "INPUT": self.parameterAsVectorLayer(
                parameters, "input_splinter_1", context
            ),
            "OUTPUT": QgsProcessing.TEMPORARY_OUTPUT,
        }
        outputs["SplitterErkennen"] = processing.run(
            "native:fieldcalculator",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Splitter nicht NULL
        alg_params = {
            "FIELD": "area",
            "INPUT": outputs["SplitterErkennen"]["OUTPUT"],
            "OPERATOR": 9,  # is not null
            "VALUE": None,
            "OUTPUT": QgsProcessing.TEMPORARY_OUTPUT,
        }
        outputs["SplitterNichtNull"] = processing.run(
            "native:extractbyattribute",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Splitter gr 15
        alg_params = {
            "FIELD": "area",
            "INPUT": outputs["SplitterNichtNull"]["OUTPUT"],
            "OPERATOR": 2,  # >
            "VALUE": "15",
            "OUTPUT": QgsProcessing.TEMPORARY_OUTPUT,
        }
        outputs["SplitterGr15"] = processing.run(
            "native:extractbyattribute",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Flächenfeld löschen
        alg_params = {
            "COLUMN": ["area"],
            "INPUT": outputs["SplitterGr15"]["OUTPUT"],
            "OUTPUT": QgsProcessing.TEMPORARY_OUTPUT,
        }
        outputs["FlchenfeldLschen"] = processing.run(
            "native:deletecolumn",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Geometrien reparieren
        alg_params = {
            "INPUT": outputs["FlchenfeldLschen"]["OUTPUT"],
            "METHOD": 1,  # Structure
            "OUTPUT": parameters.get(
                "output_healed_1", QgsProcessing.TEMPORARY_OUTPUT
            ),
        }
        outputs["GeometrienReparieren"] = processing.run(
            "native:fixgeometries",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )
        results["output_healed_1"] = outputs["GeometrienReparieren"]["OUTPUT"]
        return results

    def name(self):
        return "cleanup_1"

    def displayName(self):
        return "cleanup_1"

    def group(self):
        return "gIraffePro"

    def groupId(self):
        return "gIraffePro"

    def createInstance(self):
        return cleanup_1()
