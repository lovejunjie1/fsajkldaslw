#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date     : 3/1/2018 10:15 AM
# @Author   : Godfrey Huang (jeanimator@gmail.com)
# @Link     : http://cgenter.com

import sys, os
from Qt import QtCore, QtGui, QtWidgets, IsPySide, IsPySide2


MayaParent = None

if IsPySide:
    import ui.mainWindow_ui as mainWindow_ui
    reload(mainWindow_ui)
    from shiboken import wrapInstance    
elif IsPySide2:
    import ui.mainWindow_pyside2ui as mainWindow_ui
    reload(mainWindow_ui)
    from shiboken2 import wrapInstance
try:
    import maya.OpenMayaUI as omui
    import maya.OpenMaya as om
    import pymel.core as pm
    import pymel.core.datatypes as dt
    import maya.cmds as cmds
    import maya.mel as mel

    def getMayaWindow():
        ptr = omui.MQtUtil.mainWindow()
        return wrapInstance(long(ptr), QtWidgets.QWidget)

    MayaParent = getMayaWindow()
except:
    pass


class MainWindow(QtWidgets.QMainWindow):
    '''
    holy maya file editor main window
    '''
    WINDOW_OBJECT_NAME = 'customToolWindow'    
    HOLY_ID = 0
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(MayaParent)
        self.parent = MayaParent
        self.ui = mainWindow_ui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setObjectName(self.WINDOW_OBJECT_NAME)
        self.setDocumentMode(False)
        self.setDockOptions(QtWidgets.QMainWindow.AllowTabbedDocks | QtWidgets.QMainWindow.AnimatedDocks)
        self.setUnifiedTitleAndToolBarOnMac(False)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose) 

        cssPath = os.path.join(os.path.dirname(os.path.realpath(__file__)),'style.css')
        with open(cssPath) as cssFile:
            styleData = cssFile.read()
        self.setStyleSheet(styleData)

        self.initData()
        self.createContent()        
        self.settings()
        self.connections()                        
        self.readSettings()
        self.refreshCallCount()
    
    def refreshCallCount(self):
        if self.HOLY_ID == 0:
            return

        try:
            import HolyCmdLog
            HolyCmdLog.saveusercmdlogtofile(self.HOLY_ID)
        except:pass

    def initData(self):
        self.dataSettings = QtCore.QSettings("customToolWindowSettings", "customToolWindowSettings")

    # ui function
    def createContent(self):
        pass

    def settings(self):
        pass

    def connections(self):
        pass

    def readSettings(self):
        self.dataSettings.beginGroup('customToolWindowSettings_mainWindow')
        windowGeometry = self.dataSettings.value('window_geometry')
        windowState = self.dataSettings.value('window_state')
        self.restoreGeometry(windowGeometry)
        self.restoreState(windowState)
        self.dataSettings.endGroup()

    def writeSettings(self):
        self.dataSettings.beginGroup('customToolWindowSettings_mainWindow')
        self.dataSettings.setValue('window_geometry', self.saveGeometry())
        self.dataSettings.setValue('window_state', self.saveState())
        self.dataSettings.endGroup()

    def closeEvent(self,event):
        self.writeSettings()

def main():
    '''
    holy maya file editor
    '''
    app = QtWidgets.QApplication.instance()
    if not app:
        app = QtWidgets.QApplication([])

    for widget in app.topLevelWidgets():
        if widget.objectName() == MainWindow.WINDOW_OBJECT_NAME:
            widget.close()
            widget.deleteLater()

    window = MainWindow(parent=MayaParent)
    window.show()

    window.raise_()
    try:
        sys.exit(app.exec_())
    except: pass

if __name__ == "__main__":
    main()