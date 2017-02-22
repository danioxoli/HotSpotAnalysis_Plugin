# -*- coding: utf-8 -*-
"""
/***************************************************************************
 HotspotAnalysis
                                 A QGIS plugin
 This plugin implements the statistics needed for the Hotspot Analysis
                             -------------------
        begin                : 2017-02-22
        copyright            : (C) 2017 by Daniele Oxoli, Gabriele Prestifilippo, Mayra Zurbaràn, Stanly Shaji / Politecnico Di Milano
        email                : daniele.oxoli@polimi.it
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load HotspotAnalysis class from file HotspotAnalysis.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .hotspot_analysis import HotspotAnalysis
    return HotspotAnalysis(iface)
