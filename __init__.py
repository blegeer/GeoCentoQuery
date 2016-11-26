# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GeoCentoViewer
                                 A QGIS plugin
 Query GeoCento sources and view metadata
                             -------------------
        begin                : 2016-11-16
        copyright            : (C) 2016 by Beau Legeer
        email                : beau.legeer@digitalglobe.com
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
    """Load GeoCentoViewer class from file GeoCentoViewer.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .GeoCenterViewer import GeoCentoViewer
    return GeoCentoViewer(iface)
