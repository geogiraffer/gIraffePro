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
/***************************************************************************
 GIraFFE-Pro - Green Infrastructure fast filter and estimation Project
                                 A QGIS plugin
                              -------------------
        begin                : 2026-01-01
        copyright            : (C) 2026 by Dennis Klingspor
        email                : klingspor@geobilder.de
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 3 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""

__author__ = 'Dennis Klingspor'
__date__ = '2026-01-01'
__copyright__ = '(C) 2026 by Dennis Klingspor'


# noinspection PyPep8Naming
def classFactory(iface):
    from .giraffepro import GIraffeProPlugin
    return GIraffeProPlugin(iface)