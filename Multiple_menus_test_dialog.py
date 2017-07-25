# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Multiple_menusDialog
                                 A QGIS plugin
 Display multiple menus
                             -------------------
        begin                : 2017-07-11
        git sha              : $Format:%H$
        copyright            : (C) 2017 by GFD
        email                : hoa.lq@gfd.com.vn
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from PyQt4 import QtGui, uic
from qgis.core import QgsCoordinateReferenceSystem

FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'Multiple_menus_test_dialog_base.ui'))

class Multiple_menusDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(Multiple_menusDialog, self).__init__(parent)
        self.setupUi(self)

