# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Multiple_menus
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
from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.utils import *
import datetime

from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon, QFileDialog
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from Print_coordinate_system_dialog import checkcoordinatesysDialog
from Multiple_menus_test_dialog import Multiple_menusDialog
from Convertprj_dialog import ConvertprjBatchDialog

import os.path


class Multiple_menus:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):

        self.iface = iface

        pluginName = 'Multiple menus'
        userPluginPath = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/python/plugins/" + pluginName
        systemPluginPath = QgsApplication.prefixPath() + "/python/plugins/" + pluginName
        overrideLocale = bool(QSettings().value("locale/overrideFlag", False))

        # print 'userPluginPath: '+ userPluginPath
        if not overrideLocale:
            localeFullName = QLocale.system().name()
        else:
            localeFullName = QSettings().value("locale/userLocale", "")

        if QFileInfo(userPluginPath).exists():
            translationPath = userPluginPath + "/i18n/" + pluginName + "_" + localeFullName + ".qm"
        else:
            translationPath = systemPluginPath + "/i18n/" + pluginName + "_" + localeFullName + ".qm"
        # print translationPath
        self.localePath = translationPath

        if QFileInfo(self.localePath).exists():
            self.translator = QTranslator()
            self.translator.load(self.localePath)
            QCoreApplication.installTranslator(self.translator)
            # print('localepath exists')
            # print('translation debug info :' + ' overrideLocale=' + str(overrideLocale) + '; localeFullName=' +localeFullName + '; translationPath=' + translationPath )


        # Create the dialog (after translation) and keep reference
        self.dlgtool3 = checkcoordinatesysDialog()
        self.dlgtool1 = Multiple_menusDialog()
        self.dlgtool2 = ConvertprjBatchDialog()

        # Declare instance attributes
        # self.actions = []
        # self.menu = self.tr(u'&Convert coordinate system VN2000')
        # self.toolbar = self.iface.addToolBar(u'&Convert coordinate system VN2000')
        # self.toolbar.setObjectName(u'&Convert coordinate system VN2000')

        self.dlgtool2.lineEdit.clear()
        self.dlgtool2.toolButton.clicked.connect(self.select_output)
    # noinspection PyMethodMayBeStatic
    def tr(self, message):

        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('Multiple_menus', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):


        # # Create the dialog (after translation) and keep reference
        # self.dlg = Multiple_menusDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):

        # Create actions triggered by the plugin
        self.actionCheck = QAction(QIcon(os.path.join(os.path.dirname(__file__), "icon_2.png")),
                                   QtGui.QApplication.translate("Check, Defined and Convert CRS",
                                                                "Check Coordinate System (Kiểm tra thông tin HTĐ)", None,
                                                                QtGui.QApplication.UnicodeUTF8), self.iface.mainWindow())

        self.actionDefine = QAction(QIcon(os.path.join(os.path.dirname(__file__), "icon_1.png")),
                                   QtGui.QApplication.translate("Check, Defined and Convert CRS",
                                                                "Defined Coordinate System (Hiển thị HTĐ khớp với GE)", None,
                                                                QtGui.QApplication.UnicodeUTF8), self.iface.mainWindow())

        self.actionConvert = QAction(QIcon(os.path.join(os.path.dirname(__file__), "icon.png")),
                                   QtGui.QApplication.translate("Check, Defined and Convert CRS", "Convert Coordinate System (Chuyển hệ tọa độ)", None,
                                                                QtGui.QApplication.UnicodeUTF8), self.iface.mainWindow())
        # connect the action to the run method
        self.iface.addToolBarIcon(self.actionCheck)
        self.iface.addToolBarIcon(self.actionDefine)
        self.iface.addToolBarIcon(self.actionConvert)

        self.actionCheck.triggered.connect(self.runCheck)
        self.actionDefine.triggered.connect(self.runDefine)
        self.actionConvert.triggered.connect(self.runConvert)
        # adds buttons to labeling toolbar if exists

        self.toolBar = self.iface.pluginToolBar()
        self.iface.addPluginToMenu( "&" + QtGui.QApplication.translate("Multiple_menus", "Check, Defined and Convert CRS", None, QtGui.QApplication.UnicodeUTF8), self.actionCheck)
        self.iface.addPluginToMenu( "&" + QtGui.QApplication.translate("Multiple_menus", "Check, Defined and Convert CRS", None, QtGui.QApplication.UnicodeUTF8), self.actionDefine)
        self.iface.addPluginToMenu( "&" + QtGui.QApplication.translate("Multiple_menus", "Check, Defined and Convert CRS", None, QtGui.QApplication.UnicodeUTF8), self.actionConvert)

        # add to plugin toolbar


    def unload(self):
    # Remove the plugin menu item and icon
        self.toolBar.removeAction(self.actionDefine)

        self.iface.removePluginMenu("&" + QtGui.QApplication.translate("Multiple_menus", "Check, Defined and Convert CRS", None,
                                                                        QtGui.QApplication.UnicodeUTF8), self.actionCheck)
        self.iface.removePluginMenu("&" + QtGui.QApplication.translate("Multiple_menus", "Check, Defined and Convert CRS", None,
                                                                       QtGui.QApplication.UnicodeUTF8), self.actionDefine)
        self.iface.removePluginMenu("&" + QtGui.QApplication.translate("Multiple_menus", "Check, Defined and Convert CRS", None,
                                                                       QtGui.QApplication.UnicodeUTF8), self.actionConvert)

        # remove action from mLabelToolBar if exists
        toolbars = self.iface.mainWindow().findChildren(QToolBar)

        for toolbar in toolbars:
            if toolbar.objectName() == "mLabelToolBar":
                self.toolBar = toolbar
                # You have to save all of the actions from the toolbar
                actions = self.toolBar.actions()
                # then, you clear the complete toolbar
                self.toolBar.clear()
                # and you re-add only the actions yo uwant
                i = 0
                for a in actions:
                    self.toolBar.addAction(actions[i])
                    i = i + 1

#PLUGIN DEFINED COORDINATE SYSTEM
    def getCustom(self, htd_output,f):

        # VN2000 Hoi nhap mui 3
        htd_102_hn = "+proj=tmerc +lat_0=0 +lon_0=102 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_103_hn = "+proj=tmerc +lat_0=0 +lon_0=103 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_104_hn = "+proj=tmerc +lat_0=0 +lon_0=104 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_104_5_hn = "+proj=tmerc +lat_0=0 +lon_0=104.5 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_104_75_hn = "+proj=tmerc +lat_0=0 +lon_0=104.75 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_105_hn = "+proj=tmerc +lat_0=0 +lon_0=105 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_105_5_hn = "+proj=tmerc +lat_0=0 +lon_0=105.5 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_105_75_hn = "+proj=tmerc +lat_0=0 +lon_0=105.75 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_106_hn = "+proj=tmerc +lat_0=0 +lon_0=106 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_106_25_hn = "+proj=tmerc +lat_0=0 +lon_0=106.25 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_106_5_hn = "+proj=tmerc +lat_0=0 +lon_0=106.5 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_107_hn = "+proj=tmerc +lat_0=0 +lon_0=107 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_107_25_hn = "+proj=tmerc +lat_0=0 +lon_0=107.25 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_107_5_hn = "+proj=tmerc +lat_0=0 +lon_0=107.5 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_107_75_hn = "+proj=tmerc +lat_0=0 +lon_0=107.75 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_108_hn = "+proj=tmerc +lat_0=0 +lon_0=108 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_108_25_hn = "+proj=tmerc +lat_0=0 +lon_0=108.25 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_108_5_hn = "+proj=tmerc +lat_0=0 +lon_0=108.5 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"

        if htd_output == "System":
            return f.crs()
        elif htd_output == "VN2000 mui 3 KTT 102":
            custom = htd_102_hn
        elif htd_output == "VN2000 mui 3 KTT 103":
            custom = htd_103_hn
        elif htd_output == "VN2000 mui 3 KTT 104":
            custom = htd_104_hn
        elif htd_output == "VN2000 mui 3 KTT 104.5":
            custom = htd_104_5_hn
        elif htd_output == "VN2000 mui 3 KTT 104.75":
            custom = htd_104_75_hn
        elif htd_output == "VN2000 mui 3 KTT 105":
            custom = htd_105_hn
        elif htd_output == "VN2000 mui 3 KTT 105.5":
            custom = htd_105_5_hn
        elif htd_output == "VN2000 mui 3 KTT 105.75":
            custom = htd_105_75_hn
        elif htd_output == "VN2000 mui 3 KTT 106":
            custom = htd_106_hn
        elif htd_output == "VN2000 mui 3 KTT 106.25":
            custom = htd_106_25_hn
        elif htd_output == "VN2000 mui 3 KTT 106.5":
            custom = htd_106_5_hn
        elif htd_output == "VN2000 mui 3 KTT 107":
            custom = htd_107_hn
        elif htd_output == "VN2000 mui 3 KTT 107.25":
            custom = htd_107_25_hn
        elif htd_output == "VN2000 mui 3 KTT 107.5":
            custom = htd_107_5_hn
        elif htd_output == "VN2000 mui 3 KTT 107.75":
            custom = htd_107_75_hn
        elif htd_output == "VN2000 mui 3 KTT 108":
            custom = htd_108_hn
        elif htd_output == "VN2000 mui 3 KTT 108.25":
            custom = htd_108_25_hn
        elif htd_output == "VN2000 mui 3 KTT 108.5":
            custom = htd_108_5_hn
        res = QgsCoordinateReferenceSystem()
        res.createFromProj4(custom)
        return res

    def runDefine(self):
        """Run method that performs all the real work"""

        # Select the layers open in the legendInterface and add them to an array
        layers = self.iface.legendInterface().layers()
        layer_list = []
        # Append only Vector (type == 0) to the layer_list
        for layer in layers:
            if layer.type() == 0:
                layer_list.append(layer.name())
            else:
                pass
        # Add layer_list array to listWidget, clear layer if removed to layer in tools
        self.dlgtool1.listWidget.clear()
        self.dlgtool1.listWidget.addItems(layer_list)

        # show the dialog
        self.dlgtool1.show()
        # Run the dialog event loop
        result = self.dlgtool1.exec_()

        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass

        htd = self.dlgtool1.comboBox.currentText()
        for f in layers:
            if f.type() != 0:
                return False
            temp = self.getCustom(htd, f)
            if htd != "System":
                f.setCrs(temp)

# PLUGIN CONVERT COORDINATE SYSTEM
    # Select output file
    def select_output(self):
        output_dir = QFileDialog.getExistingDirectory(self.dlgtool2, "Chọn thư mục để lưu", "")
        self.dlgtool2.lineEdit.setText(output_dir)

    def runConvert(self):
        """Run method that performs all the real work"""

        # Select the layers open in the legendInterface and add them to an array
        layers = self.iface.legendInterface().layers()
        layer_list = []
        # Append only Vector (type == 0) to the layer_list
        for layer in layers:
            if layer.type() == 0:
                layer_list.append(layer.name())
            else:
                pass
        # Add layer_list array to listWidget, clear layer if removed to layer in tools
        self.dlgtool2.listWidget.clear()
        self.dlgtool2.listWidget.addItems(layer_list)

        # show the dialog
        self.dlgtool2.show()
        # Run the dialog event loop
        result = self.dlgtool2.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            # pass
            output_dir = self.dlgtool2.lineEdit.text()

            if not os.path.exists(output_dir):
                self.iface.messageBar().pushMessage("Khong co duong dan den thu muc",
                                                    "Vui long chon thu muc de luu file", 1, 5)
            if os.path.exists(output_dir):
                self.save_layers()

    def getCustom2(self, htd_output, f):
        # Coordinate UTM, WGS84
        crs_4326 = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
        htd_utm_48 = QgsCoordinateReferenceSystem(32648, QgsCoordinateReferenceSystem.EpsgCrsId)
        htd_utm_49 = QgsCoordinateReferenceSystem(32649, QgsCoordinateReferenceSystem.EpsgCrsId)

        # VN2000 Hoi nhap mui 3
        htd_102_hn = "+proj=tmerc +lat_0=0 +lon_0=102 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_103_hn = "+proj=tmerc +lat_0=0 +lon_0=103 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_104_hn = "+proj=tmerc +lat_0=0 +lon_0=104 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_104_5_hn = "+proj=tmerc +lat_0=0 +lon_0=104.5 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_104_75_hn = "+proj=tmerc +lat_0=0 +lon_0=104.75 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_105_hn = "+proj=tmerc +lat_0=0 +lon_0=105 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_105_5_hn = "+proj=tmerc +lat_0=0 +lon_0=105.5 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_105_75_hn = "+proj=tmerc +lat_0=0 +lon_0=105.75 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_106_hn = "+proj=tmerc +lat_0=0 +lon_0=106 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_106_25_hn = "+proj=tmerc +lat_0=0 +lon_0=106.25 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_106_5_hn = "+proj=tmerc +lat_0=0 +lon_0=106.5 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_107_hn = "+proj=tmerc +lat_0=0 +lon_0=107 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_107_25_hn = "+proj=tmerc +lat_0=0 +lon_0=107.25 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_107_5_hn = "+proj=tmerc +lat_0=0 +lon_0=107.5 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_107_75_hn = "+proj=tmerc +lat_0=0 +lon_0=107.75 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_108_hn = "+proj=tmerc +lat_0=0 +lon_0=108 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_108_25_hn = "+proj=tmerc +lat_0=0 +lon_0=108.25 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_108_5_hn = "+proj=tmerc +lat_0=0 +lon_0=108.5 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"

        if htd_output == "System":
            return f.crs()
        elif htd_output == "UTM Zone 48N - EPGS: 32648":
            return htd_utm_48
        elif htd_output == "UTM Zone 49N - EPGS: 32649":
            return htd_utm_49
        elif htd_output == "WGS84 Lat/long - EPGS: 4326":
            return crs_4326
        elif htd_output == "VN2000 mui 3 KTT 102" or htd_output == "VN-2000 Hoi nhap mui 3 KTT 102":
            custom = htd_102_hn
        elif htd_output == "VN2000 mui 3 KTT 103" or htd_output == "VN-2000 Hoi nhap mui 3 KTT 103":
            custom = htd_103_hn
        elif htd_output == "VN2000 mui 3 KTT 104" or htd_output == "VN-2000 Hoi nhap mui 3 KTT 104":
            custom = htd_104_hn
        elif htd_output == "VN2000 mui 3 KTT 104.5" or htd_output == "VN-2000 Hoi nhap mui 3 KTT 104.5":
            custom = htd_104_5_hn
        elif htd_output == "VN2000 mui 3 KTT 104.75" or htd_output == "VN-2000 Hoi nhap mui 3 KTT 104.75":
            custom = htd_104_75_hn
        elif htd_output == "VN2000 mui 3 KTT 105" or htd_output == "VN-2000 Hoi nhap mui 3 KTT 105":
            custom = htd_105_hn
        elif htd_output == "VN2000 mui 3 KTT 105.5" or htd_output == "VN-2000 Hoi nhap mui 3 KTT 105.5":
            custom = htd_105_5_hn
        elif htd_output == "VN2000 mui 3 KTT 105.75" or htd_output == "VN-2000 Hoi nhap mui 3 KTT 105.75":
            custom = htd_105_75_hn
        elif htd_output == "VN2000 mui 3 KTT 106" or htd_output == "VN-2000 Hoi nhap mui 3 KTT 106":
            custom = htd_106_hn
        elif htd_output == "VN2000 mui 3 KTT 106.25" or htd_output == "VN-2000 Hoi nhap mui 3 KTT 106.25":
            custom = htd_106_25_hn
        elif htd_output == "VN2000 mui 3 KTT 106.5" or htd_output == "VN-2000 Hoi nhap mui 3 KTT 106.5":
            custom = htd_106_5_hn
        elif htd_output == "VN2000 mui 3 KTT 107" or htd_output == "VN-2000 Hoi nhap mui 3 KTT 107":
            custom = htd_107_hn
        elif htd_output == "VN2000 mui 3 KTT 107.25" or htd_output == "VN-2000 Hoi nhap mui 3 KTT 107.25":
            custom = htd_107_25_hn
        elif htd_output == "VN2000 mui 3 KTT 107.5" or htd_output == "VN-2000 Hoi nhap mui 3 KTT 107.5":
            custom = htd_107_5_hn
        elif htd_output == "VN2000 mui 3 KTT 107.75" or htd_output == "VN-2000 Hoi nhap mui 3 KTT 107.75":
            custom = htd_107_75_hn
        elif htd_output == "VN2000 mui 3 KTT 108" or htd_output == "VN-2000 Hoi nhap mui 3 KTT 108":
            custom = htd_108_hn
        elif htd_output == "VN2000 mui 3 KTT 108.25" or htd_output == "VN-2000 Hoi nhap mui 3 KTT 108.25":
            custom = htd_108_25_hn
        elif htd_output == "VN2000 mui 3 KTT 108.5" or htd_output == "VN-2000 Hoi nhap mui 3 KTT 108.5":
            custom = htd_108_5_hn
        res = QgsCoordinateReferenceSystem()
        res.createFromProj4(custom)
        return res

    # save file shp
    def save_file(self, type):
        layers = self.iface.legendInterface().layers()
        if type == 'shp':
            output_dir = self.dlgtool2.lineEdit.text() + "/"  # + "/KETQUA_SHP/"
        elif type == 'tab':
            output_dir = self.dlgtool2.lineEdit.text() + "/"  # + "/KETQUA_TAB/"
        htd = self.dlgtool2.comboBox.currentText()
        htd_output = self.dlgtool2.comboBox_output.currentText()
        # create directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        for f in layers:
            if f.type() != 0:
                return False
            temp = self.getCustom2(htd, f)
            if htd != "System":
                f.setCrs(temp)
            if type == 'shp':
                ext = '.shp'
                writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",
                                                                 self.getCustom2(htd_output, f), "ESRI Shapefile")
            elif type == 'tab':
                ext = '.tab'
                writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".tab", "System",
                                                                 self.getCustom2(htd_output, f), "MapInfo File")
            if writer == QgsVectorFileWriter.NoError:
                self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ext + " tai " + output_dir, 0, 2)
            # else:
            #     self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ext + " tai " + output_dir, 1, 2)

    def save_layers(self):
        # if checkbox is checked, run the appropriate save function
        if self.dlgtool2.checkBox_shp.isChecked():
            self.save_file('shp')
        else:
            pass
        if self.dlgtool2.checkBox_tab.isChecked():
            self.save_file('tab')
        else:
            pass

# PLUGIN CHECK COORDINATE SYSTEM
    def runCheck(self):
        """Run method that performs all the real work"""
        # Select the layers open in the legendInterface and add them to an array
        crs = QgsCoordinateReferenceSystem()
        layers = self.iface.legendInterface().layers()
        layer_list = []
        # Declare coordinate system to print out screen
        # VN2000 Noi bo mui 3
        htd_103_nb = "+proj=tmerc +lat_0=0 +lon_0=103 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        htd_104_nb = "+proj=tmerc +lat_0=0 +lon_0=104 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        htd_104_5_nb = "+proj=tmerc +lat_0=0 +lon_0=104.5 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        htd_104_75_nb = "+proj=tmerc +lat_0=0 +lon_0=104.75 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        htd_105_nb = "+proj=tmerc +lat_0=0 +lon_0=105 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        htd_105_5_nb = "+proj=tmerc +lat_0=0 +lon_0=105.5 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        htd_105_75_nb = "+proj=tmerc +lat_0=0 +lon_0=105.75 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        htd_106_nb = "+proj=tmerc +lat_0=0 +lon_0=106 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        htd_106_25_nb = "+proj=tmerc +lat_0=0 +lon_0=106.25 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        htd_106_5_nb = "+proj=tmerc +lat_0=0 +lon_0=106.5 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        htd_107_nb = "+proj=tmerc +lat_0=0 +lon_0=107 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        htd_107_25_nb = "+proj=tmerc +lat_0=0 +lon_0=107.25 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        htd_107_5_nb = "+proj=tmerc +lat_0=0 +lon_0=107.5 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        htd_107_75_nb = "+proj=tmerc +lat_0=0 +lon_0=107.75 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        htd_108_nb = "+proj=tmerc +lat_0=0 +lon_0=108 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        htd_108_25_nb = "+proj=tmerc +lat_0=0 +lon_0=108.25 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        htd_108_5_nb = "+proj=tmerc +lat_0=0 +lon_0=108.5 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"

        # VN2000 Hoi nhap mui 3
        htd_103_hn = "+proj=tmerc +lat_0=0 +lon_0=103 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_104_hn = "+proj=tmerc +lat_0=0 +lon_0=104 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_104_5_hn = "+proj=tmerc +lat_0=0 +lon_0=104_5 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_104_75_hn = "+proj=tmerc +lat_0=0 +lon_0=104.75 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_105_hn = "+proj=tmerc +lat_0=0 +lon_0=105 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_105_5_hn = "+proj=tmerc +lat_0=0 +lon_0=105.5 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_105_75_hn = "+proj=tmerc +lat_0=0 +lon_0=105.75 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_106_hn = "+proj=tmerc +lat_0=0 +lon_0=106 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_106_25_hn = "+proj=tmerc +lat_0=0 +lon_0=106.25 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_106_5_hn = "+proj=tmerc +lat_0=0 +lon_0=106.5 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_107_hn = "+proj=tmerc +lat_0=0 +lon_0=107 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_107_25_hn = "+proj=tmerc +lat_0=0 +lon_0=107.25 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_107_5_hn = "+proj=tmerc +lat_0=0 +lon_0=107.5 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_107_75_hn = "+proj=tmerc +lat_0=0 +lon_0=107.75 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_108_hn = "+proj=tmerc +lat_0=0 +lon_0=108 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_108_25_hn = "+proj=tmerc +lat_0=0 +lon_0=108.25 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_108_5_hn = "+proj=tmerc +lat_0=0 +lon_0=108.5 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"

        # UTM 48,49
        htd_utm_48 = "+proj=utm +zone=48 +datum=WGS84 +units=m +no_defs"
        htd_utm_49 = "+proj=utm +zone=49 +datum=WGS84 +units=m +no_defs"

        # WGS84 Latlong - 4326
        htd_latlong_4326 = "+proj=longlat +datum=WGS84 +no_defs"

        #Loop all layers
        for layer in layers:
            if layer.crs().toProj4() == htd_103_nb :
                layer_list.append(layer.name() + " -->" + "VN-2000 Noi bo KTT 103 mui 3 ")
            elif layer.crs().toProj4() == htd_104_nb :
                layer_list.append(layer.name() + " -->" + "VN-2000 Noi bo KTT 104 mui 3 ")
            elif layer.crs().toProj4() == htd_104_5_nb :
                layer_list.append(layer.name() + " -->" + "VN-2000 Noi bo KTT 104.5 mui 3 ")
            elif layer.crs().toProj4() == htd_104_75_nb :
                layer_list.append(layer.name() + " -->" + "VN-2000 Noi bo KTT 104.75 mui 3 ")
            elif layer.crs().toProj4() == htd_105_nb :
                layer_list.append(layer.name() + " -->" + "VN-2000 Noi bo KTT 105 mui 3 ")
            elif layer.crs().toProj4() == htd_105_5_nb :
                layer_list.append(layer.name() + " -->" + "VN-2000 Noi bo KTT 105.5 mui 3 ")
            elif layer.crs().toProj4() == htd_105_75_nb :
                layer_list.append(layer.name() + " -->" + "VN-2000 Noi bo KTT 105.75 mui 3 ")
            elif layer.crs().toProj4() == htd_106_nb :
                layer_list.append(layer.name() + " -->" + "VN-2000 Noi bo KTT 106 mui 3 ")
            elif layer.crs().toProj4() == htd_106_25_nb :
                layer_list.append(layer.name() + " -->" + "VN-2000 Noi bo KTT 106.25 mui 3 ")
            elif layer.crs().toProj4() == htd_106_5_nb :
                layer_list.append(layer.name() + " -->" + "VN-2000 Noi bo KTT 106.5 mui 3 ")
            elif layer.crs().toProj4() == htd_107_nb :
                layer_list.append(layer.name() + " -->" + "VN-2000 Noi bo KTT 107 mui 3 ")
            elif layer.crs().toProj4() == htd_107_25_nb :
                layer_list.append(layer.name() + " -->" + "VN-2000 Noi bo KTT 107.25 mui 3 ")
            elif layer.crs().toProj4() == htd_107_5_nb :
                layer_list.append(layer.name() + " -->" + "VN-2000 Noi bo KTT 107.5 mui 3 ")
            elif layer.crs().toProj4() == htd_107_75_nb :
                layer_list.append(layer.name() + " -->" + "VN-2000 Noi bo KTT 107.75 mui 3 ")
            elif layer.crs().toProj4() == htd_108_nb :
                layer_list.append(layer.name() + " -->" + "VN-2000 Noi bo KTT 108 mui 3 ")
            elif layer.crs().toProj4() == htd_108_25_nb :
                layer_list.append(layer.name() + " -->" + "VN-2000 Noi bo KTT 108.25 mui 3 ")
            elif layer.crs().toProj4() == htd_108_5_nb :
                layer_list.append(layer.name() + " -->" + "VN-2000 Noi bo KTT 108.5 mui 3 ")
        # VN2000 Hoi nhap
            elif layer.crs().toProj4() == htd_103_hn :
                layer_list.append(layer.name() + " -->" + "VN-2000 Hoi nhap KTT 103 mui 3 ")
            elif layer.crs().toProj4() == htd_104_hn :
                layer_list.append(layer.name() + " -->" + "VN-2000 Hoi nhap KTT 104 mui 3 ")
            elif layer.crs().toProj4() == htd_104_5_hn :
                layer_list.append(layer.name() + " -->" + "VN-2000 Hoi nhap KTT 104.5 mui 3 ")
            elif layer.crs().toProj4() == htd_104_75_hn :
                layer_list.append(layer.name() + " -->" + "VN-2000 Hoi nhap KTT 104.75 mui 3 ")
            elif layer.crs().toProj4() == htd_105_hn :
                layer_list.append(layer.name() + " -->" + "VN-2000 Hoi nhap KTT 105 mui 3 ")
            elif layer.crs().toProj4() == htd_105_5_hn :
                layer_list.append(layer.name() + " -->" + "VN-2000 Hoi nhap KTT 105.5 mui 3 ")
            elif layer.crs().toProj4() == htd_105_75_hn :
                layer_list.append(layer.name() + " -->" + "VN-2000 Hoi nhap KTT 105.75 mui 3 ")
            elif layer.crs().toProj4() == htd_106_hn :
                layer_list.append(layer.name() + " -->" + "VN-2000 Hoi nhap KTT 106 mui 3 ")
            elif layer.crs().toProj4() == htd_106_25_hn :
                layer_list.append(layer.name() + " -->" + "VN-2000 Hoi nhap KTT 106.25 mui 3 ")
            elif layer.crs().toProj4() == htd_106_5_hn :
                layer_list.append(layer.name() + " -->" + "VN-2000 Hoi nhap KTT 106.5 mui 3 ")
            elif layer.crs().toProj4() == htd_107_hn :
                layer_list.append(layer.name() + " -->" + "VN-2000 Hoi nhap KTT 107 mui 3 ")
            elif layer.crs().toProj4() == htd_107_25_hn :
                layer_list.append(layer.name() + " -->" + "VN-2000 Hoi nhap KTT 107.25 mui 3 ")
            elif layer.crs().toProj4() == htd_107_5_hn :
                layer_list.append(layer.name() + " -->" + "VN-2000 Hoi nhap KTT 107.5 mui 3 ")
            elif layer.crs().toProj4() == htd_107_75_hn :
                layer_list.append(layer.name() + " -->" + "VN-2000 Hoi nhap KTT 107.75 mui 3 ")
            elif layer.crs().toProj4() == htd_108_hn :
                layer_list.append(layer.name() + " -->" + "VN-2000 Hoi nhap KTT 108 mui 3 ")
            elif layer.crs().toProj4() == htd_108_25_hn :
                layer_list.append(layer.name() + " -->" + "VN-2000 Hoi nhap KTT 108.25 mui 3 ")
            elif layer.crs().toProj4() == htd_108_5_hn :
                layer_list.append(layer.name() + " -->" + "VN-2000 Hoi nhap KTT 108.5 mui 3 ")

        # UTM 48,49, Latlong
            elif layer.crs().toProj4() == htd_utm_48 :
                layer_list.append(layer.name() + " -->" + "UTM Zone 48N - EPSG: 32648")
            elif layer.crs().toProj4() == htd_utm_49 :
                layer_list.append(layer.name() + " -->" + "UTM Zone 49N - EPSG: 32649")
            elif layer.crs().toProj4() == htd_latlong_4326 :
                layer_list.append(layer.name() + " -->" + "WGS 84 Lat/Long - EPSG: 4326")
            else:
                layer_list.append(layer.name() + " -->" +layer.crs().toProj4())
        # Add layer_list array to listWidget, clear layer if removed to layer in tools
        self.dlgtool3.listWidget_check.clear()
        self.dlgtool3.listWidget_check.addItems(layer_list)
        # show the dialog
        self.dlgtool3.show()
        # Run the dialog event loop
        result = self.dlgtool3.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
