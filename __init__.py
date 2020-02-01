# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Numerical digitize - sets up a Qgis actions for append and edit features
 by inserting or changing digital values of vertex's coordinates
 A QGIS plugin
                              -------------------
        begin                : 2010 year
        git sha              : $Format:%H$
        copyright (C) 2010 Cédric Möri, with stuff from Stefan Ziegler
                      2019 Igor Chumichev
        email                : desertwolf@inbox.ru
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

def classFactory(iface):
    """Load NumericalDigitize class from file NumericalDigitize.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    from .numericalDigitize import NumericalDigitize
    return NumericalDigitize(iface)
