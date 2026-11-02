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

"""Shared definitions and input checks for the optional subject datasets."""
from qgis.core import QgsProcessingException

DATASETS = [{'code': 'FFH', 'prepare': '_ffh_geometrie', 'weight': '_ffh_bewertung_13', 'main': '_fachdatum_fd_ffh', 'geometry': 'Polygon', 'field': 'Wert_FFH', 'info': 'Info_FFH', 'result_key': 'VektorobjektInDateiSpeichernFfh'}, {'code': 'LSG', 'prepare': '_lsg_geometrie', 'weight': '_lsg_bewertung_13', 'main': '_fd_lsg', 'geometry': 'Polygon', 'field': 'Wert_LSG', 'info': 'Info_LSG', 'result_key': 'VektorobjektInDateiSpeichernLsg'}, {'code': 'LSG_LIN', 'prepare': '_lsg_geometrie_lin', 'weight': '_lsg_lin_bewertung_13', 'main': '_fd_lsg_linear', 'geometry': 'LineString', 'field': 'Wert_LSG', 'info': 'Info_LSG_lin', 'result_key': 'VektorobjektInDateiSpeichernLsgLinear'}, {'code': 'ND_PKT', 'prepare': '_nd_geometrie_pkt', 'weight': '_nd_pkt_bewertung_13', 'main': '_fd_natiurdenkmal_punkt_28', 'geometry': 'Point', 'field': 'Wert_ND', 'info': 'Info_ND_pkt', 'result_key': 'VektorobjektInDateiSpeichernNdPunkt'}, {'code': 'ND_LIN', 'prepare': '_nd_geometrie_lin', 'weight': '_nd_lin_bewertung_13', 'main': '_fd_nd__linear_28', 'geometry': 'LineString', 'field': 'Wert_ND', 'info': 'Info_ND_lin', 'result_key': 'VektorobjektInDateiSpeichernNdLinear'}, {'code': 'ND', 'prepare': '_nd_geometrie', 'weight': '_nd_bewertung_13', 'main': '_fd_nd__28', 'geometry': 'Polygon', 'field': 'Wert_ND', 'info': 'Info_ND', 'result_key': 'VektorobjektInDateiSpeichernNd'}, {'code': 'SPA', 'prepare': '_spa_geometrie', 'weight': '_spa_bewertung_13', 'main': '_fd_spa', 'geometry': 'Polygon', 'field': 'Wert_SPA', 'info': 'Info_SPA', 'result_key': 'VektorobjektInDateiSpeichernSpa'}, {'code': 'NSG', 'prepare': '_nsg_geometrie', 'weight': '_nsg_bewertung_13', 'main': '_fd_nsg', 'geometry': 'Polygon', 'field': 'Wert_NSG', 'info': 'Info_NSG', 'result_key': 'VektorobjektInDateiSpeichernNsg'}, {'code': 'GLB_PKT', 'prepare': '_glb_geometrie_pkt', 'weight': '_glb_pkt_bewertung_13', 'main': '_fd_gesch_landschaftsbestandteil_glb_punkt_29', 'geometry': 'Point', 'field': 'Wert_GLB', 'info': 'Info_GLB_Pkt', 'result_key': 'VektorobjektInDateiSpeichernGlbPunkt'}, {'code': 'GLB_LIN', 'prepare': '_glb_geometrie_lin', 'weight': '_glb_lin_bewertung_13', 'main': '_fd_glb_linear_29', 'geometry': 'LineString', 'field': 'Wert_GLB', 'info': 'Info_GLB_Ln', 'result_key': 'VektorobjektInDateiSpeichernGlbLinie'}, {'code': 'GLB', 'prepare': '_glb_geometrie', 'weight': '_glb_bewertung_13', 'main': '_fd_glb_29', 'geometry': 'Polygon', 'field': 'Wert_GLB', 'info': 'Info_GLB_Poly', 'result_key': 'VektorobjektInDateiSpeichernGlbPoly'}]


def selected_datasets(algorithm, parameters, context, stage):
    """Resolve supplied layers; distinguish an omitted input from a broken source."""
    selected = []
    for spec in DATASETS:
        key = spec[stage]
        raw = parameters.get(key)
        if raw is None or (isinstance(raw, str) and not raw.strip()):
            continue
        layer = algorithm.parameterAsVectorLayer(parameters, key, context)
        if layer is None or not layer.isValid():
            raise QgsProcessingException(f"{spec['code']}: Die angegebene Datenquelle kann nicht geladen werden.")
        if stage == 'main' and layer.fields().indexFromName(spec['field']) < 0:
            raise QgsProcessingException(
                f"{spec['code']}: Das Wertfeld {spec['field']} fehlt. "
                "Bitte den Datensatz zuerst mit der Fachdatenbewertung vorbereiten.")
        selected.append((spec, layer))
    if not selected:
        raise QgsProcessingException("Bitte mindestens einen Fachdatensatz (Eingaben 1 bis 11) auswählen.")
    return selected


def maximum_expression(fields):
    """A subset may have just one field; NULL from a union is not a rating."""
    terms = ['coalesce("' + field.replace('"', '""') + '", 0)' for field in fields]
    return terms[0] if len(terms) == 1 else 'max(' + ','.join(terms) + ')'
