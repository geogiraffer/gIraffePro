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

from qgis.core import QgsProcessingProvider

from .giraffe_main import GreenInfrastructureFFEProject
from .fachdatenbewertung import Giraffepro_fachdatenbewertung
from .cleanup_1 import cleanup_1
from .cleanup_2 import cleanup_2

from qgis.PyQt.QtGui import QIcon
from pathlib import Path


class GIraffeProProvider(QgsProcessingProvider):
    
    def loadAlgorithms(self):
        self.addAlgorithm(GreenInfrastructureFFEProject())
        self.addAlgorithm(Giraffepro_fachdatenbewertung())
        self.addAlgorithm(cleanup_1())
        self.addAlgorithm(cleanup_2())

    def id(self):
        return "giraffepro"

    def name(self):
        return "gIraffePro"

    def longName(self):
        return "Green Infrastructure fast filter and estimation Project (gIraffePro)"
        
    def icon(self): return QIcon(str(Path(__file__).parent.parent / "logo_giraffe.png"))
        