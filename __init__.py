# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Multiple_menus
                                 A QGIS plugin
 Display multiple menus
                             -------------------
        begin                : 2017-07-11
        copyright            : (C) 2017 by GFD
        email                : hoa.lq@gfd.com.vn
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
    """Load Multiple_menus class from file Multiple_menus.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .Multiple_menus_test import Multiple_menus
    return Multiple_menus(iface)
