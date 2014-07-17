# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QuickOSMDialog
                                 A QGIS plugin
 OSM's Overpass API frontend
                             -------------------
        begin                : 2014-06-11
        copyright            : (C) 2014 by 3Liz
        email                : info@3liz.com
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

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from osm_file import Ui_ui_osm_file
from os.path import dirname,abspath,join,isfile
from QuickOSM.CoreQuickOSM.ExceptionQuickOSM import FileDoesntExistException

class OsmFileWidget(QWidget, Ui_ui_osm_file):
    def __init__(self, parent=None):
        QWidget.__init__(self)
        self.setupUi(self)
        
        defaultOsmConf = join(dirname(abspath(__file__)),"CoreQuickOSM","Parser","osmconf.ini")
        self.lineEdit_osmConf.setText(defaultOsmConf)
        self.pushButton_openOsmFile.setEnabled(False)
        
        #Connect
        self.pushButton_browseOsmFile.clicked.connect(self.setOsmFilePath)
        self.pushButton_browseOsmConf.clicked.connect(self.setOsmConfPath)
        self.lineEdit_osmConf.textEdited.connect(self.disableRunButton)
        self.lineEdit_osmFile.textEdited.connect(self.disableRunButton)
        self.pushButton_openOsmFile.clicked.connect(self.openFile)
        
    def setOsmFilePath(self):
        '''
        Fill the osm file
        '''
        osmFile = QFileDialog.getOpenFileName(parent=None, caption=QApplication.translate("QuickOSM", 'Select *.osm or *.pbf'),filter="OSM file (*.osm *.pbf)")
        self.lineEdit_osmFile.setText(osmFile)
        self.disableRunButton()
            
    def setOsmConfPath(self):
        '''
        Fill the osmConf file
        '''
        osmConf = QFileDialog.getOpenFileName(parent=None, caption=QApplication.translate("QuickOSM", 'Select osm conf'), filter="OsmConf file (*.ini)")
        self.lineEdit_osmConf.setText(osmConf)
        self.disableRunButton()
            
    def disableRunButton(self):
        if self.lineEdit_osmConf.text() and self.lineEdit_osmFile.text():
            self.pushButton_openOsmFile.setEnabled(True)
        else:
            self.pushButton_openOsmFile.setEnabled(False)
        
    def openFile(self):
        #Get fields
        osmFile = self.lineEdit_osmFile.text()
        osmConf = self.lineEdit_osmConf.text()
        
        if not isfile(osmFile):
            raise FileDoesntExistException(suffix="*.osm or *.pbf")
        
        if not isfile(osmConf):
            raise FileDoesntExistException(suffix="*.ini")

class OsmFileDockWidget(QDockWidget):
    def __init__(self, parent=None):
        QDockWidget.__init__(self)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setWidget(OsmFileWidget())
        self.setWindowTitle(QApplication.translate("ui_osm_file", "OSM File"))