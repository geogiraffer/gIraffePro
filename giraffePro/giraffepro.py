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

from pathlib import Path

from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtGui import QIcon
from qgis.core import QgsApplication

import processing

from .processing_provider.giraffepro_provider import GIraffeProProvider


class GIraffeProPlugin:

    def __init__(self, iface):
        self.iface = iface
        self.provider = None
        self.action = None
        self.assessment_action = None

    def initGui(self):

        # ---------------------------------------------------------
        # Processing Provider registrieren
        # ---------------------------------------------------------

        self.provider = GIraffeProProvider()

        QgsApplication.processingRegistry().addProvider(
            self.provider
        )

        # ---------------------------------------------------------
        # Icon laden
        # ---------------------------------------------------------

        plugin_dir = Path(__file__).resolve().parent
        icon_path = plugin_dir / "logo_giraffe.png"

        icon = QIcon(str(icon_path))
     

        # ---------------------------------------------------------
        # Toolbar-Button erzeugen
        # ---------------------------------------------------------

        self.action = QAction(
            icon,
            "Green Infrastructure fast filter and estimation Project (gIraffePro)",
            self.iface.mainWindow()
        )

        self.action.setToolTip(
            "Filtern und Einschätzen grüner Bestandsinfrastruktur in frühen Planungsphasen"
        )

        self.action.setStatusTip(
            "Startet den gIraffePro-Algorithmus"
        )

        self.action.triggered.connect(
            self.runGreenInfrastructureFFEProject
        )

        # ---------------------------------------------------------
        # Button zur QGIS-Toolbar hinzufügen
        # ---------------------------------------------------------
        self.iface.addPluginToMenu("&gIraffePro", self.action)

        self.iface.addToolBarIcon(
            self.action
        )

        # Separate entry point for preparing and rating the specialist datasets.
        assessment_icon = QIcon(str(plugin_dir / "logo_fachdatenbewertung.png"))
        self.assessment_action = QAction(
            assessment_icon, "Fachdatenbewertung", self.iface.mainWindow()
        )
        self.assessment_action.setToolTip("Fachdaten bewerten und als geojson speichern")
        self.assessment_action.triggered.connect(self.runFachdatenbewertung)
        self.iface.addPluginToMenu("&gIraffePro", self.assessment_action)
        self.iface.addToolBarIcon(self.assessment_action)

    def runFachdatenbewertung(self):
        processing.execAlgorithmDialog("giraffepro:fachdatenbewertung")

    def runGreenInfrastructureFFEProject(self):

        processing.execAlgorithmDialog(
            "giraffepro:giraffe_main"
        )

    def unload(self):

        if self.assessment_action is not None:
            self.iface.removePluginMenu("&gIraffePro", self.assessment_action)
            self.iface.removeToolBarIcon(self.assessment_action)
            self.assessment_action.deleteLater()
            self.assessment_action = None

        # Toolbar-Button entfernen
        if self.action is not None:

            self.iface.removePluginMenu("&gIraffePro", self.action)
            self.iface.removeToolBarIcon(
                self.action
            )

            self.action.deleteLater()
            self.action = None

        # Processing Provider entfernen
        if self.provider is not None:

            QgsApplication.processingRegistry().removeProvider(
                self.provider
            )

            self.provider = None