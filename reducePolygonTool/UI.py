#coding:utf-8
'''
2018-7-30 14:55:47
1.point on perface smoothed polyon to reduce face.what ever how many level.
  just need it's a perface smoothed polygon.that'all
2.It must have 5stars point.3 stars,2 stars and mor that 5 stars. there are not for this version.
3.Crease Tool is very useful.it could help you protect the edges which you won't delete.
4.also the loops of creased edges.it could be protected.just click the switch.
5.have fun.and be nice for TDs,we server for you guys with our hair.
'''
__author__ = 'fei.wang'
MayaParent = None

import sys
from Qt import QtWidgets as qw, QtGui, QtCore, IsPySide, IsPySide2
import threading

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

import functions_falloff
functions_falloff_class = functions_falloff.reduceFace_FalloffVersion_class()




class returnableThread(threading.Thread):

    def __init__(self,func,args=()):
        super(returnableThread,self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None

class reducePolygonTool_back_Class():

    def selVertByIntArray(self,polyName,inputArray,add=False):
        if not add:
            cmds.select(cl=1)
        for i in inputArray:
            vertString = '%s.vtx[%s]' % (polyName,str(i))
            cmds.select(vertString,add=1)

    def selEdgeByIntArray(self,polyName,inputArray,add=False):
        if not add:
            cmds.select(cl=1)
        for i in inputArray:
            vertString = '%s.e[%s]' % (polyName,str(i))
            cmds.select(vertString,add=1)

    def cleanInfos(self,vid):
        # vid = 'Head_01_Geo2.vtx[2660]'
        #
        # clean the none digital infos like:
        # sss = 'VERTEX   2660:  15050   5165   5167   5168 \n'

        gets = vid.split(' ')
        collect = []
        for g in gets:
            if g.isdigit():
                collect.append(g)
        return collect

    def getAllVertsWhoHave5edges(self,polyName,isMoreThan4 = True,is2 = True,is3 = False):
        polyCount = cmds.polyEvaluate(polyName, v=1)

        self.progress.setMaximum(polyCount)
        self.progress.setLabelText('analyzing...')
        self.progress.setValue(0)

        vertArray = []
        midEdgeArray = []
        creaseVertexArray = []
        if isMoreThan4 or is2 or is3:
            for i in range(polyCount):

                self.progress.setValue(i)

                vert = '%s.vtx[%s]' % (polyName, str(i))

                edgeInfo = cmds.polyInfo(vert, vertexToEdge=1)

                edgeID = self.cleanInfos(edgeInfo[0])

                # get vert who own the defined number of edges.
                IDlength = len(edgeID)

                isThisVertexImportent = False
                if isMoreThan4:
                    if IDlength > 4:
                        vertArray.append(i)
                        isThisVertexImportent = True
                if is2:
                    if IDlength == 2:
                        vertArray.append(i)
                        isThisVertexImportent = True
                if is3:
                    if IDlength == 3:
                        vertArray.append(i)
                        isThisVertexImportent = True

                # get middle edges.may be more than 1.as also are two.
                vertPos = cmds.xform(vert, q=1, ws=1, t=1)
                if round(vertPos[0], 6) == 0:
                    for eid in edgeID:
                        edg = '%s.e[%s]' % (polyName, str(eid))
                        edgePos = cmds.xform(edg, q=1, ws=1, t=1)
                        if round(edgePos[0], 6) == 0 and round(edgePos[3], 6) == 0:
                            midEdgeArray.append(int(eid))
                            break

                # get crease vertex.this vertex just for 2,3,5 and 5+ stars vertex.

                if isThisVertexImportent:
                    cVal = cmds.polyCrease(vert, q=1, vertexValue=1)
                    if cVal[0] > 0:
                        creaseVertexArray.append(int(i))
            #print 'crease vert:'
            #print creaseVertexArray
            return [vertArray, midEdgeArray, creaseVertexArray]
        else:
            print 'you need defined a type of vert to get.isMoreThan4 or is2 or is3?'
            return False


    def getBaseStructEdges(self, polyName):

        vertArrayTemp = self.getAllVertsWhoHave5edges(polyName)
        if vertArrayTemp:
            cleanVertArray = vertArrayTemp[0]
            midEdgeArray = vertArrayTemp[1]
            creaseVertexArray = vertArrayTemp[2]
            self.progress.setMaximum(len(cleanVertArray))
            self.progress.setLabelText('struct data...')
            self.progress.setValue(0)

            edgeLoopArray = []
            sortTemp = []
            # get the base struct edges on normal way.
            for count,cva in enumerate(cleanVertArray):

                self.progress.setValue(count)

                vert = '%s.vtx[%s]' % (polyName, str(cva))

                edgeInfo = cmds.polyInfo(vert, vertexToEdge=1)

                edgeID = self.cleanInfos(edgeInfo[0])

                for eid in edgeID:
                    edgeLoop = cmds.polySelect(polyName, edgeLoop=int(eid), ass=0, q=1)
                    intArray = []
                    for el in edgeLoop:
                        intArray.append(int(el))
                    sEdgeLoop = list(intArray)
                    sEdgeLoop.sort()

                    if not(sEdgeLoop in sortTemp):
                        edgeLoopArray.append(intArray)
                        sortTemp.append(sEdgeLoop)

            # if middle edges exists.add middle edges into array.
            strTemp = []
            if midEdgeArray:
                for mea in midEdgeArray:
                    edgeLoop = cmds.polySelect(polyName, edgeLoop=mea, ass=0, q=1)
                    strLoop = str(edgeLoop)
                    if strLoop not in strTemp:
                        strTemp.append(strLoop)
                        edgeLoopArray.append(edgeLoop)

            # before this line.for loop have a filter to split the multiple occurrence edges.
            # so we need add the edges who defined by crease vertex after filter.

            # add edges weight by crease verts.
            addWeightStructEdges = []
            for cva in creaseVertexArray:
                vert = '%s.vtx[%s]' % (polyName, str(cva))

                edgeInfo = cmds.polyInfo(vert, vertexToEdge=1)

                edgeID = self.cleanInfos(edgeInfo[0])

                for eid in edgeID:
                    edgeLoop = cmds.polySelect(polyName, edgeLoop=int(eid), ass=0, q=1)
                    intArray = []
                    for el in edgeLoop:
                        intArray.append(int(el))

                    addWeightStructEdges.append(intArray)


            return [edgeLoopArray, addWeightStructEdges]
        else:
            return False

    def calculateBaseDeleteArray(self,polyName,delLevel=1):
        # delLevel attr means smooth level 1 to reverse
        divAttr = delLevel+1

        edgeArrayTemp = self.getBaseStructEdges(polyName)
        if edgeArrayTemp:
            edgeArray = edgeArrayTemp[0]
            addWeightStructEdges = edgeArrayTemp[1]
        else:
            return False

        # every item in the array is unique.it's all fine.
        self.progress.setMaximum(len(edgeArray))
        self.progress.setLabelText('clean data..')
        self.progress.setValue(0)

        wholeEdges = []
        for i in edgeArray:
            wholeEdges += i

        # ================== main part =================================
        selEdgeArray = []

        for count,ela in enumerate(edgeArray):

            self.progress.setValue(count)

            if len(ela) >= divAttr:

                # make data form.when divAttr equel 1,we need two item to calculate.
                # divAttr = 2  ->  item length = 3
                # divAttr = 3  ->  item length = 4
                divWorkArray = [ela[i:i+divAttr] for i in range(0, len(ela), divAttr)]

                # check array struct,is it 100% fit? if more or less.then removed them.
                for dwacheck in divWorkArray:
                    if len(dwacheck) != divAttr:
                        divWorkArray.remove(dwacheck)

                # collect the point on curve,who need to delete under base rule.
                delVertInEdge = []

                for dwa in divWorkArray:

                    tempArray = []

                    targetArray = []

                    for i in dwa:

                        edge = '%s.e[%s]' % (polyName, str(i))

                        vtx = cmds.polyInfo(edge, edgeToVertex=1)

                        vtxID = self.cleanInfos(vtx[0])

                        for vid in vtxID:

                            if int(vid) in tempArray:

                                targetArray.append(int(vid))

                            else:

                                tempArray.append(int(vid))

                    delVertInEdge += targetArray

                # now we need convert the vert to the edge who crossed base struct edges.

                crossEdges = []
                for dvi in delVertInEdge:

                    vert = '%s.vtx[%s]' % (polyName, str(dvi))

                    edgeInfo = cmds.polyInfo(vert, vertexToEdge=1)

                    edgeID = self.cleanInfos(edgeInfo[0])

                    # rule 1.the line can not in the base protect array.
                    # in the touch point.there're two edges in base protect array.
                    # now i need collect all of rest items.
                    cellArray = []
                    for eid in edgeID:
                        if not(int(eid) in wholeEdges):
                            cellArray.append(int(eid))

                    crossEdges.append(cellArray)

                selEdgeArray.append(crossEdges)
        # ================== main part end =================================
        # ================== add cease vert weight part =================================
        # calculate the edges who need add weight.
        # program as same as the main function of this def.
        # just use a another array and loop again.
        # addWeightStructEdges

        addWeightEdgeArray = []

        self.progress.setValue(0)
        for count,ela in enumerate(addWeightStructEdges):

            self.progress.setValue(count)

            if len(ela) >= divAttr:

                # make data form.when divAttr equel 1,we need two item to calculate.
                # divAttr = 2  ->  item length = 3
                # divAttr = 3  ->  item length = 4
                divWorkArray = [ela[i:i+divAttr] for i in range(0, len(ela), divAttr)]

                # check array struct,is it 100% fit? if more or less.then removed them.
                for dwacheck in divWorkArray:
                    if len(dwacheck) != divAttr:
                        divWorkArray.remove(dwacheck)

                # collect the point on curve,who need to delete under base rule.
                delVertInEdge = []

                for dwa in divWorkArray:
                    tempArray = []
                    targetArray = []
                    for i in dwa:
                        edge = '%s.e[%s]' % (polyName, str(i))
                        vtx = cmds.polyInfo(edge, edgeToVertex=1)
                        vtxID = self.cleanInfos(vtx[0])
                        for vid in vtxID:
                            if int(vid) in tempArray:
                                targetArray.append(int(vid))
                            else:
                                tempArray.append(int(vid))

                    delVertInEdge += targetArray

                # now we need convert the vert to the edge who crossed base struct edges.

                crossEdges = []
                for dvi in delVertInEdge:
                    vert = '%s.vtx[%s]' % (polyName, str(dvi))
                    edgeInfo = cmds.polyInfo(vert, vertexToEdge=1)
                    edgeID = self.cleanInfos(edgeInfo[0])

                    # rule 1.the line can not in the base protect array.
                    # in the touch point.there're two edges in base protect array.
                    # now i need collect all of rest items.
                    cellArray = []
                    for eid in edgeID:
                        if not(int(eid) in wholeEdges):
                            cellArray.append(int(eid))

                    crossEdges.append(cellArray)

                addWeightEdgeArray.append(crossEdges)

        # ================== add cease vert weight part end =================================
        countWeightTemp = addWeightEdgeArray + selEdgeArray
        self.progress.setMaximum(len(countWeightTemp))
        self.progress.setLabelText('clean data....')
        self.progress.setValue(0)
        wholeDelArrayTemp = []

        countDict = {}
        # edge weights dict. very important.
        for count, gg in enumerate(countWeightTemp):
            self.progress.setValue(count)
            for ce in gg:
                if ce:
                    edgeLoop = cmds.polySelect(polyName, edgeLoop=int(ce[0]), ass=0, q=1)

                    edgeLoop.sort()

                    strEdge = str(edgeLoop)

                    if strEdge not in countDict.keys():

                        countDict.update({strEdge:5})
                    else:
                        countDict[strEdge] += 1
                    '''
                    isFound = False
                    for awe in addWeightEdgeArray:
                        if ce in awe:
                            isFound = True

                    if isFound:
                        countDict.update({strEdge:7})
                    '''
        # ==========================================
        vertToKeyDict = {}
        vertToWeightDict = {}

        edgeArray # defined at the fist of def

        teamVertsByEdgeArray = []
        for ea in edgeArray:
            tempArray = []
            for i in ea:
                edge = '%s.e[%s]' % (polyName, str(i))
                vtx = cmds.polyInfo(edge, edgeToVertex=1)
                vtxID = self.cleanInfos(vtx[0])
                for vid in vtxID:
                    if int(vid) not in tempArray:
                        tempArray.append(int(vid))
            teamVertsByEdgeArray.append(tempArray)



        crossEdges = []
        for tvbea in teamVertsByEdgeArray:
            for tvb in tvbea:
                vert = '%s.vtx[%s]' % (polyName, str(tvb))
                edgeInfo = cmds.polyInfo(vert, vertexToEdge=1)
                edgeID = self.cleanInfos(edgeInfo[0])

                # rule 1.the line can not in the base protect array.
                # in the touch point.there're two edges in base protect array.
                # now i need collect all of rest items.
                cellArray = []
                for eid in edgeID:
                    if not (int(eid) in wholeEdges):
                        edgeLoop = cmds.polySelect(polyName, edgeLoop=int(eid), ass=0, q=1)
                        cellArray.append(edgeLoop)
                        break
                if cellArray:
                    crossEdges.append(cellArray)
        #print '^^^^^'
        #for ce in crossEdges:
        #    print ce
        #print len(crossEdges)
        #print '^^^^^'

        # ==========================================


        # remove edges.just keep weight <= 5.
        # as high weight as confirm the edge have to be deleted.
        collectArray = []
        for key,val in countDict.items():
            if val > 5:
                keytemp = key.split(',')
                collectList = []
                for kt in keytemp:
                    digitTemp = ''
                    for k in kt:
                        if k.isdigit():
                            digitTemp += k
                    digitVal = int(digitTemp)
                    collectList.append(digitVal)
                collectArray.append(collectList)

        for cc in collectArray:
            for c in cc:
                wholeDelArrayTemp.append(c)



        return [collectArray, wholeDelArrayTemp]

    def filterCrease(self, polyName, wholeDelArrayTemp, isProtectCreaseLoop=True):

        arrayWithoutCrease = []

        noneCreaseArray = []

        creaseArray = []

        self.progress.setMaximum(len(wholeDelArrayTemp))
        self.progress.setLabelText('filter Crease...')
        self.progress.setValue(0)

        for count, pwda in enumerate(wholeDelArrayTemp):
            self.progress.setValue(count)
            fullString = '%s.e[%s]' % (polyName, str(pwda))
            cVal = cmds.polyCrease(fullString, q=1, value=1)
            if cVal[0] <= 0:
                noneCreaseArray.append(int(pwda))
            else:
                creaseArray.append(int(pwda))

        creaseProtectArray = []

        if isProtectCreaseLoop:
            for i in creaseArray:
                edgeLoop = cmds.polySelect(polyName, edgeLoop=int(i), ass=0, q=1)
                for el in edgeLoop:
                    creaseProtectArray.append(int(el))

            for i in noneCreaseArray:
                if i not in creaseProtectArray:
                    arrayWithoutCrease.append(i)
        else:
            arrayWithoutCrease = list(noneCreaseArray)

        return arrayWithoutCrease

    def main(self, protectloop=True, reducelevel=1):

        theSel = cmds.ls(sl=1)

        polyName = theSel[0]
        if '.' in polyName:
            polyName = polyName.split('.')[0]
        # if user in the edge mode selected.filter the detail tags.just keep model name.

        self.progress = qw.QProgressDialog()
        self.progress.show()

        wholeDelArrayTemp = self.calculateBaseDeleteArray(polyName, delLevel=reducelevel)

        filterArray = self.filterCrease(polyName, wholeDelArrayTemp[1], isProtectCreaseLoop=protectloop)

        self.progress.setMaximum(5)
        self.progress.setLabelText('struct final data...')
        self.progress.setValue(3)

        preWholeDelArray = ['%s.e[%s]' % (polyName, str(fa)) for fa in filterArray]

        self.progress.setLabelText('delete edges...')
        self.progress.setValue(4)
        cmds.polyDelEdge(preWholeDelArray,cv=1)

        self.progress.setValue(5)

        self.progress.close()

        print 'done'



class reduceSmoothFacesClass(qw.QMainWindow):
    uniqueInstance = None
    versionCode = 'ver' + ' 0.1.0'
    WINDOW_OBJECT_NAME = 'reduceFace'
    HOLY_ID = 0

    def __init__(self, parent=None):
        # ----- formular -----
        super(reduceSmoothFacesClass, self).__init__(MayaParent)

        self.resize(400, 150)
        self.parent = MayaParent
        self.setObjectName(self.WINDOW_OBJECT_NAME)
        self.setDocumentMode(False)
        self.initData()
        self.readSettings()
        self.refreshCallCount()
        # ----- formular end -----

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

        theTab = qw.QTabWidget()
        mv = qw.QVBoxLayout()
        mainWidget.setLayout(mv)
        mv.addWidget(theTab)

        grp1 = qw.QGroupBox()
        vlay = qw.QVBoxLayout()
        grp1.setLayout(vlay)
        vlay.addStretch()

        hlay0 = qw.QHBoxLayout()
        stepSlider = qw.QSlider()
        stepSlider.setOrientation(QtCore.Qt.Horizontal)
        stepSlider.setFixedSize(150, 30)
        #stepSlider.setStyleSheet(sliderStyle)
        stepSlider.setMinimum(1)
        stepSlider.setMaximum(5)
        stepSlider.setSingleStep(1)
        #stepSlider.setTickInterval(1)
        stepSlider.setTickPosition(qw.QSlider.TicksAbove)

        self.displayLevel = qw.QLabel('1')
        self.displayLevel.setStyleSheet(Mstyle.QLabel(fontSize='24px'))
        self.displayLevel.setFixedSize(30,30)
        hlay0.addStretch()
        hlay0.addWidget(self.displayLevel)
        hlay0.addWidget(stepSlider)
        hlay0.addStretch()
        vlay.addLayout(hlay0)



        hlay1 = qw.QHBoxLayout()
        runButton = qw.QPushButton()
        runButton.setText('reduce')
        runButton.setFixedSize(180, 30)
        runButton.setStyleSheet(Mstyle.QPushButton())
        hlay1.addWidget(runButton)
        vlay.addLayout(hlay1)

        hlay2 = qw.QHBoxLayout()
        self.checkBox = qw.QCheckBox()
        self.checkBox.setFixedWidth(180)
        self.checkBox.setText('protect crease loop')
        self.checkBox.setStyleSheet(Mstyle.QCheckBox())
        hlay2.addWidget(self.checkBox)
        vlay.addLayout(hlay2)

        vlay.addStretch()

        theTab.addTab(grp1, 'typeA')

        grp2 = qw.QGroupBox()
        vlay2 = qw.QVBoxLayout()
        grp2.setLayout(vlay2)
        vlay2.addStretch()

        hlay20 = qw.QHBoxLayout()
        stepSlider2 = qw.QSlider()
        stepSlider2.setOrientation(QtCore.Qt.Horizontal)
        stepSlider2.setFixedSize(150, 30)
        #stepSlider2.setStyleSheet(sliderStyle)
        stepSlider2.setMinimum(1)
        stepSlider2.setMaximum(5)
        stepSlider2.setSingleStep(1)
        #stepSlider2.setTickInterval(1)
        stepSlider2.setTickPosition(qw.QSlider.TicksAbove)

        self.displayLevel2 = qw.QLabel('1')
        self.displayLevel2.setStyleSheet(Mstyle.QLabel(fontSize='24px'))
        self.displayLevel2.setFixedSize(30,30)
        hlay20.addStretch()
        hlay20.addWidget(self.displayLevel2)
        hlay20.addWidget(stepSlider2)
        hlay20.addStretch()
        vlay2.addLayout(hlay20)

        hlay25 = qw.QHBoxLayout()
        thresholdLab = qw.QLabel('threshold : ')
        thresholdLab.setFixedWidth(80)
        self.spinBox = qw.QSpinBox()
        self.spinBox.setRange(-1000, 1000)
        self.spinBox.setValue(100)
        self.spinBox.setFixedWidth(70)

        hlay25.addStretch()
        hlay25.addWidget(thresholdLab)
        hlay25.addWidget(self.spinBox)
        hlay25.addStretch()
        vlay2.addLayout(hlay25)

        hlay21 = qw.QHBoxLayout()
        runButton2 = qw.QPushButton()
        runButton2.setText('reduce')
        runButton2.setFixedSize(180, 30)
        runButton2.setStyleSheet(Mstyle.QPushButton())
        hlay21.addWidget(runButton2)
        vlay2.addLayout(hlay21)

        hlay2 = qw.QHBoxLayout()
        self.checkBox2 = qw.QCheckBox()
        self.checkBox2.setChecked(True)
        self.checkBox2.setFixedWidth(180)
        self.checkBox2.setText('use fall off module')
        self.checkBox2.setStyleSheet(Mstyle.QCheckBox())
        hlay2.addWidget(self.checkBox2)
        vlay2.addLayout(hlay2)



        vlay2.addStretch()


        theTab.addTab(grp2, 'typeB')



        # init mainWidget statesbar
        self.statusBar().showMessage('reduce 1 level smooth.press button to use,enjoy it')

        runButton.clicked.connect(self.main)
        runButton2.clicked.connect(self.main_type2)
        stepSlider.sliderMoved.connect(self.slidermoveFn)

    def slidermoveFn(self,Val):
        tipDict = {'1': 'reduce 1 level smooth.press button to use,enjoy it',
                   '2': 'reduce 2 level smooth.',
                   '3': 'reduce 3 level smooth.',
                   '4': 'reduce 4 level smooth.is it too much?',
                   '5': 'reduce 5 level smooth.it is realy too much.',
                   '6': 'reduce 6 level smooth.really?',
                   '7': 'reduce 7 level smooth.seriously?',
                   '8': 'reduce 8 level smooth.zi ji ren bie kai qiang!',
                   '9': 'reduce 9 level smooth.da guo huo xue bi!',
                   '10': 'reduce 10 level smooth.da guo huo bing kuo luo!'}

        self.displayLevel.setText(str(Val))

        self.statusBar().showMessage(tipDict[str(Val)])

    def main(self):
        self.statusBar().showMessage('let us rock!')
        reduceVal = int(self.displayLevel.text())

        rpt_bc = reducePolygonTool_back_Class()
        rpt_bc.main(reducelevel=reduceVal, protectloop=self.checkBox.isChecked())

        self.statusBar().showMessage('done!')


    def main_type2(self):
        theSel = cmds.ls(sl=1)

        polyName = theSel[0]
        if '.' in polyName:
            polyName = polyName.split('.')[0]

        returnVal = functions_falloff_class.main(polyName,clamp=self.spinBox.value(),isfallOffModules=self.checkBox2.isChecked(),delLevel = 1)

        #for i in returnVal:
        #    functions_falloff_class.selEdgeByIntArray(i, add=1)

        preWholeDelArray = []
        for fa in returnVal:
            for f in fa:
                preWholeDelArray.append('%s.e[%s]' % (polyName, str(f)))


        cmds.polyDelEdge(preWholeDelArray,cv=1)

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


def main():
    '''
    holy polygon reduce faces editor
    '''
    app = qw.QApplication.instance()
    if not app:
        app = qw.QApplication([])

    for widget in app.topLevelWidgets():
        if widget.objectName() == reduceSmoothFacesClass.WINDOW_OBJECT_NAME:
            widget.close()
            widget.deleteLater()

    window = reduceSmoothFacesClass(parent=MayaParent)
    window.show()

    window.raise_()
    try:
        sys.exit(app.exec_())
    except: pass

if __name__ == '__main__':
    main()