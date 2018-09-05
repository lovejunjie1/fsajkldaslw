import sys
rpt_path = r'D:\codes\dev\splitBlendshapes'
if not rpt_path in sys.path:
    sys.path.append(rpt_path)

from Qt import QtWidgets as qw, QtGui, QtCore, IsPySide, IsPySide2

if IsPySide:
    from shiboken import wrapInstance
elif IsPySide2:
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
        return wrapInstance(long(ptr), qw.QWidget)

    MayaParent = getMayaWindow()
except:
    pass

import redBlackStyleSheet as MstyleTemp
Mstyle = MstyleTemp.RedBlackStyleSheet()

import template3
tpClass = template3.splitBSback_Class()

class splitBlendshapeUIClass(qw.QMainWindow):
    uniqueInstance = None
    versionCode = 'ver' + ' 0.1.0'
    WINDOW_OBJECT_NAME = 'splitBlendshape'
    HOLY_ID = 0

    def __init__(self, parent=None):
        # ----- formular -----
        super(splitBlendshapeUIClass, self).__init__(MayaParent)

        self.resize(400, 150)
        self.parent = MayaParent
        self.setObjectName(self.WINDOW_OBJECT_NAME)
        self.setDocumentMode(False)
        self.initData()
        self.readSettings()
        self.refreshCallCount()
        # ----- formular end -----
        self.ogMod = ''
        self.bsMod = ''

        self.ogDict = {}
        self.bsDict = {}
        self.workDict = {}

        self.colorArray = []
        self.finalDictArray = []
        self.spPlanes = []
        # ----- custom Attr ------
        self.create_ui()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    def create_ui(self):
        self.setParent(MayaParent)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle(self.WINDOW_OBJECT_NAME)

        self.setDockOptions(qw.QMainWindow.AllowTabbedDocks | qw.QMainWindow.AnimatedDocks)
        self.setUnifiedTitleAndToolBarOnMac(False)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        mainWidget = qw.QWidget()
        self.setCentralWidget(mainWidget)
        #mainWidget.setFixedHeight(130)
        mainWidget.setAttribute(QtCore.Qt.WA_StyledBackground)
        #mainWidget.setStyleSheet(Mstyle.QWidget())


        vlay = qw.QVBoxLayout()
        mainWidget.setLayout(vlay)



        groupbox1 = qw.QGroupBox()
        vlayout1 = qw.QVBoxLayout(groupbox1)
        vlayout1.setAlignment(QtCore.Qt.AlignCenter)

        hlay0 = qw.QHBoxLayout()

        self.spinC = qw.QSpinBox()
        self.spinC.setRange(0, 100)
        self.spinC.setEnabled(False)
        self.spinC.setValue(0)
        self.spinC.setFixedWidth(60)
        self.spinC.setSuffix('%')
        hlay0.addWidget(self.spinC)

        selA = qw.QPushButton('set')
        selA.setEnabled(False)
        selA.setFixedSize(50,20)
        selA.setToolTip('orig')
        selA.setStyleSheet(Mstyle.QPushButton(kw='b'))
        hlay0.addWidget(selA)

        self.lineEA = qw.QLineEdit()
        self.lineEA.setEnabled(False)
        self.lineEA.setStyleSheet(Mstyle.QLineEdit(kw='c'))
        self.lineEA.setText('click << to pick Orignal mesh')
        hlay0.addWidget(self.lineEA)

        addBtnA = qw.QPushButton('<<')
        addBtnA.setFixedSize(50,20)
        addBtnA.setToolTip('orignal')
        addBtnA.setStyleSheet(Mstyle.QPushButton(kw='on'))
        hlay0.addWidget(addBtnA)
        vlayout1.addLayout(hlay0)

        hlay1 = qw.QHBoxLayout()

        self.spinD = qw.QSpinBox()
        self.spinD.setRange(0, 100)
        self.spinD.setValue(100)
        self.spinD.setFixedWidth(60)
        self.spinD.setSuffix('%')
        hlay1.addWidget(self.spinD)

        selB = qw.QPushButton('set')
        selB.setFixedSize(50, 20)
        selB.setToolTip('bs')
        selB.setStyleSheet(Mstyle.QPushButton(kw='b'))
        hlay1.addWidget(selB)

        self.lineEB = qw.QLineEdit()
        self.lineEB.setStyleSheet(Mstyle.QLineEdit(kw='c'))
        self.lineEB.setEnabled(False)
        self.lineEB.setText('click << to pick Blenshape mesh')
        hlay1.addWidget(self.lineEB)

        addBtnB = qw.QPushButton('<<')
        addBtnB.setFixedSize(50, 20)
        addBtnB.setToolTip('blendshape')
        addBtnB.setStyleSheet(Mstyle.QPushButton(kw='on'))
        hlay1.addWidget(addBtnB)
        vlayout1.addLayout(hlay1)

        tipLab1 = qw.QLabel('')
        tipLab1.setText('Tips: set button >> set selection vertex position like orignal or blendshape mesh')
        vlayout1.addWidget(tipLab1)

        vlay.addWidget(groupbox1)
        # ==========================
        self.typeTab = qw.QTabWidget()
        self.typeTab.setStyleSheet(Mstyle.QTabWidget())
        self.typeTab.setTabPosition(qw.QTabWidget.West)

        groupbox3 = qw.QGroupBox()
        groupbox3 .setStyleSheet(Mstyle.QGroupBox())
        vlayout3 = qw.QVBoxLayout(groupbox3)
        vlayout3.setAlignment(QtCore.Qt.AlignCenter)

        createMidPlaneBtn = qw.QPushButton('create middle fast plane')
        createMidPlaneBtn.setStyleSheet(Mstyle.QPushButton(kw='on'))
        vlayout3.addWidget(createMidPlaneBtn)

        selMidPlaneBtn = qw.QPushButton('select and update')
        selMidPlaneBtn.setStyleSheet(Mstyle.QPushButton(kw='b'))
        #vlayout3.addWidget(selMidPlaneBtn)

        spinHB = qw.QHBoxLayout()
        titleLabSpinB = qw.QLabel('curvility (0-50):')

        self.spinB = qw.QSpinBox()
        self.spinB.setRange(0, 50)
        self.spinB.setValue(30)

        spinHB.addWidget(titleLabSpinB)
        spinHB.addWidget(self.spinB)
        #self.spinB.setPrefix ('curvility: ')
        vlayout3.addLayout(spinHB)

        self.typeTab.addTab(groupbox3, 'type1')

        # ============================
        groupbox2 = qw.QGroupBox()
        groupbox2 .setStyleSheet(Mstyle.QGroupBox())
        vlayout2 = qw.QVBoxLayout(groupbox2)
        vlayout2.setAlignment(QtCore.Qt.AlignCenter)

        hlay10 = qw.QHBoxLayout()
        spinApreLabel = qw.QLabel()
        spinApreLabel.setText('split to ')
        spinApreLabel.setFixedWidth(40)
        hlay10.addWidget(spinApreLabel)

        self.spinA = qw.QSpinBox()
        self.spinA.setRange(2, 20)
        self.spinA.setValue(2)
        self.spinA.setFixedWidth(90)
        self.spinA.setSuffix('parts')

        createPlaneBtn = qw.QPushButton('create plane')

        createPlaneBtn.setStyleSheet(Mstyle.QPushButton(kw='on'))

        hlay10.addWidget(self.spinA)
        hlay10.addWidget(createPlaneBtn)
        vlayout2.addLayout(hlay10)

        self.planeTable = qw.QTableWidget()
        self.planeTable.setColumnCount(2)
        self.planeTable.setHorizontalHeaderLabels(['curvility', 'name'])
        self.planeTable.setRowCount(0)
        self.planeTable.horizontalHeader().setStretchLastSection(True)
        self.planeTable.setSelectionMode(qw.QAbstractItemView.ExtendedSelection)
        self.planeTable.setColumnWidth(0, 50)
        vlayout2.addWidget(self.planeTable)


        hBox196 = qw.QHBoxLayout()
        self.checkCombie = qw.QCheckBox()
        self.checkCombie.setText('isCombieBorder')
        self.checkCombie.setChecked(True)
        self.checkCombie.setFixedWidth(120)
        hBox196.addWidget(self.checkCombie)
        
        updatePlaneBtn = qw.QPushButton('update plane position')
        updatePlaneBtn.setStyleSheet(Mstyle.QPushButton(kw='b'))
        #hBox196.addWidget(updatePlaneBtn)
        #hBox196.addStretch(1)
        #vlayout2.addLayout(hBox196)

        vlayout2.addStretch()

        self.typeTab.addTab(groupbox2, 'type2')

        # =======================================

        groupbox4 = qw.QGroupBox()
        groupbox4 .setStyleSheet(Mstyle.QGroupBox())
        vlayout4 = qw.QVBoxLayout(groupbox4)
        vlayout4.setAlignment(QtCore.Qt.AlignCenter)

        noLab = qw.QLabel()
        noLab.setText('comming soon')
        vlayout4.addWidget(noLab)

        self.typeTab.addTab(groupbox4, 'type3')


        vlay.addWidget(self.typeTab)

        previewBtn = qw.QPushButton('preview')
        previewBtn.setStyleSheet(Mstyle.QPushButton(kw='b'))
        vlay.addWidget(previewBtn)

        vlay.addStretch()


        '''
        stepSlider.sliderMoved.connect(self.slidermoveFn)
        '''
        addBtnA.clicked.connect(self.pickBtnFn)
        addBtnB.clicked.connect(self.pickBtnFn)
        createMidPlaneBtn.clicked.connect(self.fastBtnFn)
        #selMidPlaneBtn.clicked.connect(self.refreshAreaFn)

        createPlaneBtn.clicked.connect(self.createPlaneBtnFn)

        previewBtn.clicked.connect(self.previewBtnFn)

        self.checkCombie.toggled.connect(self.checkCombieFn)

        self.spinB.valueChanged.connect(self.refreshAreaFn)

        selA.clicked.connect(self.resetPointFn)
        selB.clicked.connect(self.resetPointFn)

    def resetPointFn(self):
        cmds.undoInfo(openChunk=True)

        sender = self.sender()
        if sender.toolTip() == 'bs':
            if self.bsMod and self.bsDict:
                if self.ogDict:
                    tpClass.resetSelVertxToBaseShape(self.bsMod,self.ogDict,self.bsDict,setPercent=self.spinD.value())
                else:
                    print 'orig model not picked.'
            else:
                print 'blendshape model not picked.'
        elif sender.toolTip() == 'orig':
            if self.bsDict:
                if self.ogMod and self.ogDict:
                    tpClass.resetSelVertxToBaseShape(self.ogMod,self.bsDict,self.ogDict,setPercent=self.spinC.value())
                else:
                    print 'orig model not picked.'
            else:
                print 'blendshape model not picked.'

        cmds.undoInfo(closeChunk=True)

    def checkCombieFn(self, state):
        print state
        self.refreshFinalDictFn()
    def createPlaneBtnFn(self):
        self.clearExistsPlane()
        lineNum = self.spinA.value() +2
        if not self.colorArray or len(self.colorArray) != lineNum:
            self.colorArray = tpClass.getColorArray(lineNum-1)
        self.spPlanes = tpClass.createSplitPlane(self.bsMod, fullNumberOfLine=lineNum)

        self.areaArray = tpClass.getAreaDict(self.bsMod, self.spPlanes, self.workDict)
        colorDict = tpClass.changeAreaColor(self.bsMod, self.areaArray, self.colorArray)

        self.planeTable.clear()
        self.planeTable.setRowCount(len(self.colorArray))

        for count,key in enumerate(self.colorArray):
            curItm = qw.QSpinBox()
            curItm.setRange(0, 50)
            curItm.setValue(30)
            curItm.valueChanged.connect(self.refreshAreaFn)

            nameItm = qw.QTableWidgetItem()
            nameItm.setBackground(QtGui.QColor(key[0]*255, key[1]*255, key[2]*255))
            nameItm.setText(str([key[0]*255, key[1]*255, key[2]*255]))

            self.planeTable.setCellWidget(count,0,curItm)
            self.planeTable.setItem(count,1,nameItm)


        self.refreshFinalDictFn()

    def clearExistsPlane(self):
        if self.spPlanes:
            if cmds.objExists(self.spPlanes[0]):
                nn = cmds.ls(self.spPlanes[0], long=1)
                gg = nn[0].split('|')[1]
                cmds.delete(gg)

    def fastBtnFn(self):

        lineNum = 4
        if not self.colorArray:
            self.colorArray = tpClass.colorArray = tpClass.getColorArray(lineNum-1)
        self.spPlanes = tpClass.createSplitPlane(self.bsMod, fullNumberOfLine=lineNum)

        self.areaArray = tpClass.getAreaDict(self.bsMod, self.spPlanes, self.workDict)
        colorDict = tpClass.changeAreaColor(self.bsMod, self.areaArray, self.colorArray)
        self.refreshFinalDictFn()

    def refreshAreaFn(self):

        self.areaArray = tpClass.getAreaDict(self.bsMod, self.spPlanes, self.workDict)
        colorDict = tpClass.changeAreaColor(self.bsMod, self.areaArray, self.colorArray)
        self.refreshFinalDictFn()

    def refreshFinalDictFn(self):

        if self.spPlanes and self.workDict:
            cDict = {}
            combieCheck = self.checkCombie.isChecked()
            if self.typeTab.currentIndex() == 0:
                cDict = {0: 0.3, 1: float(self.spinB.value()*0.01), 2: 0.3}
                combieCheck = True
            elif self.typeTab.currentIndex() == 1:
                rows = self.planeTable.rowCount()
                for rw in range(rows):
                    valItm = self.planeTable.cellWidget(rw,0)
                    val = float(valItm.value()) * 0.01
                    cDict.update({rw:val})

            self.finalDictArray = tpClass.refreshExcuteDict(self.bsMod, self.spPlanes, self.workDict, curDict=cDict,
                                                            isCombieBorder=combieCheck)


    def previewBtnFn(self):
        cmds.undoInfo(openChunk=True)
        self.refreshAreaFn()

        if self.finalDictArray:
            lenth = len(self.finalDictArray)
            existsArray = []
            for i in range(lenth):
                checkName = self.bsMod + '_splitMesh' + str(i)
                if not cmds.objExists(checkName):
                    dMesh = cmds.duplicate(self.bsMod, n=checkName, rr=1)[0]
                else:
                    dMesh = checkName

                colorDict = tpClass.changeAreaColor(dMesh, self.areaArray, self.colorArray)
                boundSize = cmds.getAttr(dMesh + '.boundingBoxSize')[0]
                dTrans = cmds.xform(self.bsMod, q=1, ws=1, t=1)

                dY = dTrans[1] + (boundSize[1]*1.1)
                dX = dTrans[0] + (boundSize[0]*(i*0.1)) + (boundSize[0]*i)
                fullX = dTrans[0] + (boundSize[0]*(lenth*0.1)) + (boundSize[0]*lenth)
                dX = dX - (fullX * 0.5)

                cmds.xform(dMesh, ws=1, t=[dX, dY, dTrans[2]])

                existsArray.append(checkName)



            for i in range(lenth):
                theDict = self.finalDictArray[i]
                tpClass.executeVertexMoving(theDict, existsArray[i])

            delCheckArray = cmds.ls(self.bsMod + '_splitMesh*', type = 'transform')
            for dca in delCheckArray:
                if dca not in existsArray:
                    cmds.delete(dca)
        cmds.undoInfo(closeChunk=True)

    def pickBtnFn(self):
        sel = cmds.ls(sl=1)
        sender = self.sender()
        if sel:
            if sender.toolTip() == 'blendshape':
                self.lineEB.setText(sel[0])
                self.bsMod = sel[0]
                self.bsDict = tpClass.meshPointDict(self.bsMod)

            elif sender.toolTip() == 'orignal':
                self.lineEA.setText(sel[0])
                self.ogMod = sel[0]
                self.ogDict = tpClass.meshPointDict(self.ogMod)

            if self.ogDict and self.bsDict:
                self.workDict = tpClass.markWorkArea(self.bsMod, self.ogDict, self.bsDict)

        else:
            if sender.toolTip() == 'blendshape':
                self.lineEB.setText('click << to pick Blenshape mesh')
                self.bsMod = ''
                self.bsDict = {}
            elif sender.toolTip() == 'orignal':
                self.lineEA.setText('click << to pick Orignal mesh')
                self.ogMod = ''
                self.ogDict = {}

    def slidermoveFn(self,Val):


        self.statusBar().showMessage('what')

    def main(self):
        self.statusBar().showMessage('let us rock!')

        self.statusBar().showMessage('done!')


    def initData(self):
        self.dataSettings = QtCore.QSettings("customToolWindowSettings", "customToolWindowSettings")

    def refreshCallCount(self):
        if self.HOLY_ID == 0:
            return

        try:
            import HolyCmdLog
            HolyCmdLog.saveusercmdlogtofile(self.HOLY_ID)
        except:pass

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
        self.clearExistsPlane()

def main():
    '''
    holy polygon reduce faces editor
    '''
    app = qw.QApplication.instance()
    if not app:
        app = qw.QApplication([])

    for widget in app.topLevelWidgets():
        if widget.objectName() == splitBlendshapeUIClass.WINDOW_OBJECT_NAME:
            widget.close()
            widget.deleteLater()

    window = splitBlendshapeUIClass(parent=MayaParent)
    window.show()

    window.raise_()
    try:
        sys.exit(app.exec_())
    except: pass

if __name__ == '__main__':
    main()
    #window = splitBlendshapeUIClass(parent=MayaParent)
    #window.show()