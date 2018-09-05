import maya.cmds as cmds
import math
import maya.OpenMaya as om
from Qt import QtWidgets as qw, QtGui, QtCore, IsPySide, IsPySide2


def copySelVertexList():
    clipboard = qw.QApplication.clipboard()

    sel = cmds.ls(sl=1, fl=1)

    tempB = []
    for s in sel:
        subs = s.split('.')
        if len(subs) == 2:
            if subs[1][:3] == 'vtx':
                tempA = str(subs[1])
                tempB.append(tempA)

    clipboard.setText(str(tempB))


def pasteSelVertexList():
    sels = cmds.ls(sl=1)
    if sels:
        polyName = sels[0]
        if '.' in polyName:
            spmainsel = polyName.split('.')
            polyName = spmainsel[0]

        clipboard = qw.QApplication.clipboard()

        data = clipboard.mimeData()
        selList = []
        if data.hasText():
            dText = data.text()
            doubleCheck = (dText[:6] == '[\'vtx[')
            if doubleCheck:
                selList = eval(dText)

        #print selList
        if selList:
            combieList = []
            for sl in selList:
                tempC = '%s.%s' % (polyName, sl)
                combieList.append(tempC)

            cmds.select(combieList)

'''

copySelVertexList()

pasteSelVertexList()

resetSelVertxToBaseShape('browDown2',oDict)

'''



class splitBSback_Class():



    def resetSelVertxToBaseShape(self,bsName,baseDict,bsDict,setPercent = 100):
        sel = cmds.ls(sl=1, fl=1)

        for s in sel:
            subs = s.split('.')
            if len(subs) == 2:
                if subs[1][:3] == 'vtx':
                    tempA = int(subs[1][4:-1])
                    posA = baseDict[tempA]
                    posB = bsDict[tempA]
                    per = setPercent * 0.01

                    pos = [((posA[0] - posB[0]) * per) + posB[0], ((posA[1] - posB[1]) * per) + posB[1], ((posA[2] - posB[2]) * per) + posB[2]]

                    bFullName = '%s.vtx[%s]' % (bsName, str(tempA))

                    cmds.xform(bFullName, os=1, t=pos)





    def meshPointDict(self,polyName,isRound = False):
        vertCount = cmds.polyEvaluate(polyName,v=1)

        origDict = {}
        for i in range(vertCount):
            vtxName = '%s.vtx[%s]' % (polyName, str(i))
            ogValTemp = cmds.xform(vtxName, os=1, q=1, t=1)
            ogVal = []
            if isRound:
                for og in ogValTemp:
                    tempA = round(og,isRound)
                    ogVal.append(tempA)
            else:
                ogVal = ogValTemp
            tempDict = {i: ogVal}
            origDict.update(tempDict)
        return origDict



    def markWorkArea(self,showMesh,oDict,bDict,defaulfColor = (0.0, 0.5, 0.4),roundVal = 5):
        cmds.polyColorPerVertex(showMesh, rgb=(0.0,0.0,0.0), colorDisplayOption=False)
        workAreaDict = {}
        for i in range(len(oDict.keys())):
            oVal = oDict[i]
            orVal = []
            for ov in oVal:
                ov = round(ov, roundVal)
                orVal.append(ov)

            bVal = bDict[i]
            brVal = []
            for bv in bVal:
                bv = round(bv, roundVal)
                brVal.append(bv)

            if orVal != brVal:

                tempA = {i: {'o': oVal, 'b': bVal}}

                workAreaDict.update(tempA)

                vtxName = '%s.vtx[%s]' % (showMesh, str(i))

                cmds.polyColorPerVertex(vtxName, rgb=defaulfColor, colorDisplayOption=True)

        return workAreaDict

    def lockAttr(self,attrName, isHide=0, lockArray=[0, 1, 1, 1, 1, 1, 1, 1, 1, 1]):
        tempArray = ['.tx', '.ty', '.tz',
                     '.rx', '.ry', '.rz',
                     '.sx', '.sy', '.sz',
                     '.v']

        for i in range(9):
            fullAttr = attrName + tempArray[i]
            try:
                cmds.setAttr(fullAttr, lock=lockArray[i])
                if isHide:
                    cmds.setAttr(fullAttr, hide=lockArray[i])
            except:
                print fullAttr + ' can not be changed.'

    def uniqueName(self,strName):
        count = 0
        needLoop = True
        nowName = strName
        while needLoop:
            count += 1
            if cmds.objExists(nowName):
                nowName = strName + str(count)
            else:
                needLoop = False
        return nowName

    def createSingleReferenctLine(self,meshName):
        boundSize = cmds.getAttr(meshName + '.boundingBoxSize')
        boundMin = cmds.getAttr(meshName + '.boundingBoxMin')

        planeMidName = self.uniqueName('referencePlane_Mid')
        planeMid = cmds.polyPlane(w=boundSize[0][2]*1.1, h=boundSize[0][1]*1.1, sx=1, sy=1, ax=(1, 0, 0), cuv=2, ch=1, n=planeMidName)

        planeMidGrp = cmds.group(planeMid[0], n=planeMidName + '_grp')
        self.lockAttr(planeMid[0])

        planeLeftName = self.uniqueName('referencePlane_Left')
        planeLeft = cmds.polyPlane(w=boundSize[0][2]*1.1, h=boundSize[0][1]*1.1, sx=1, sy=1, ax=(1, 0, 0), cuv=2, ch=1, n=planeLeftName)
        planeLeftGrp = cmds.group(planeLeft[0], n=planeLeftName + '_grp')
        self.lockAttr(planeLeft[0])

        planeRightName = self.uniqueName('referencePlane_Right')
        planeRight = cmds.polyPlane(w=boundSize[0][2]*1.1, h=boundSize[0][1]*1.1, sx=1, sy=1, ax=(1, 0, 0), cuv=2, ch=1, n=planeRightName)
        planeRightGrp = cmds.group(planeRight[0], n=planeRightName + '_grp')
        self.lockAttr(planeRight[0])

        cmds.xform(planeMidGrp, ws=1, t=[boundMin[0][0] + boundSize[0][0]*0.5,
                                         boundMin[0][1] + boundSize[0][1]*0.5,
                                         boundMin[0][2] + boundSize[0][2]*0.5])

        cmds.xform(planeLeftGrp, ws=1, t=[boundMin[0][0] + boundSize[0][0]*0.75,
                                         boundMin[0][1] + boundSize[0][1]*0.5,
                                         boundMin[0][2] + boundSize[0][2]*0.5])

        cmds.xform(planeRightGrp, ws=1, t=[boundMin[0][0] + boundSize[0][0]*0.25,
                                         boundMin[0][1] + boundSize[0][1]*0.5,
                                         boundMin[0][2] + boundSize[0][2]*0.5])
        cmds.setAttr(planeRightGrp + '.sx', -1)

        cmds.parent([planeRightGrp, planeLeftGrp], planeMid[0])

        cmds.parentConstraint(meshName, planeMidGrp, mo=1, n=self.uniqueName('referencePlane_parentConstraint'))
        cmds.scaleConstraint(meshName, planeMidGrp, mo=1, n=self.uniqueName('referencePlane_scaleConstraint'))
        return {'m': planeMid[0], 'l': planeLeft[0], 'r': planeRight[0]}

    def getRange(self, bsName, minP, maxP):

        minValTemp = cmds.xform(minP, ws=1, q=1, t=1)
        minVal = minValTemp[0]
        # print maxVal

        maxValTemp = cmds.xform(maxP, ws=1, q=1, t=1)
        maxVal = maxValTemp[0]
        # print midVal

        baseValTemp = cmds.xform(bsName, ws=1, q=1, t=1)
        baseVal = baseValTemp[0]

        minVal -= baseVal
        maxVal -= baseVal

        rangeVal = maxVal - minVal

        return {'max': maxVal, 'min': minVal, 'range': rangeVal}





    def createSplitPlane(self, meshName, fullNumberOfLine =4):

        boundSize = cmds.getAttr(meshName + '.boundingBoxSize')
        boundMin = cmds.getAttr(meshName + '.boundingBoxMin')

        unit = 1.0/float(fullNumberOfLine-1)
        planeGrpArray = []
        for i in range(fullNumberOfLine):
            planeMidName = self.uniqueName('referencePlane_ref')
            planeMid = cmds.polyPlane(w=boundSize[0][2] * 1.1, h=boundSize[0][1] * 1.1, sx=1, sy=1, ax=(1, 0, 0), cuv=2, ch=1,
                                      n=planeMidName)

            planeMidGrp = cmds.group(planeMid[0], n=planeMidName + '_grp')
            planeMidSdk = cmds.group(planeMidGrp, n=planeMidName + '_sdk')
            planeMidZero = cmds.group(planeMidSdk, n=planeMidName + '_zero')
            self.lockAttr(planeMid[0])
            planeGrpArray.append(planeMidZero)

            cmds.xform(planeMidZero, ws=1, t=[boundMin[0][0] + boundSize[0][0] * unit * i,
                                             boundMin[0][1] + boundSize[0][1]*0.5,
                                             boundMin[0][2] + boundSize[0][2]*0.5])

        refPlaneGrp = cmds.group(planeGrpArray,n=self.uniqueName('referencePlane_grp'))
        refPlaneSdk = cmds.group(refPlaneGrp,n=self.uniqueName('referencePlane_sdk'))
        refPlaneZero = cmds.group(refPlaneSdk,n=self.uniqueName('referencePlane_zero'))

        st = planeGrpArray[0][:-5]
        ed = planeGrpArray[-1][:-5]
        mid = planeGrpArray[1:-1]

        for count,i in enumerate(mid):
            val = count+1
            cons = cmds.parentConstraint([st,ed], i, mo=1, n=self.uniqueName('referencePlane_parentConstraint'))
            cmds.setAttr('%s.%sW0' % (cons[0],st),1.0 - (val*unit))
            cmds.setAttr('%s.%sW1' % (cons[0],ed),(val*unit))

        cmds.parentConstraint(meshName, refPlaneZero, mo=1, n=self.uniqueName('referencePlane_parentConstraint'))
        cmds.scaleConstraint(meshName, refPlaneZero, mo=1, n=self.uniqueName('referencePlane_scaleConstraint'))

        return planeGrpArray




    def getColorArray(self, totalLen):

        import random
        random.randrange(0.0, 1.0)
        colorArray = []
        for i in range(totalLen):

            ranR = round(random.random(), 4)
            ranG = round(random.random(), 4)
            ranB = round(random.random(), 4)
            colorArray.append((ranR,ranG,ranB))

        return colorArray

    def getAreaDict(self,meshName, spPlanes, workDict):

        reSpPlanes = []
        reSpPlanesMatrix = []
        reSpPlanesMatrixInv = []
        for sp in spPlanes:
            pl = sp[:-5]

            theMatMin = cmds.xform(pl, q=1, ws=1, m=1)

            matrix_planeMin = om.MMatrix()
            util_planeMin = om.MScriptUtil()
            util_planeMin.createMatrixFromList(theMatMin, matrix_planeMin)

            reSpPlanes.append(pl)
            reSpPlanesMatrix.append(matrix_planeMin)
            reSpPlanesMatrixInv.append(matrix_planeMin.inverse())

        returnAreaDict = {}
        outterCount = 0
        returnWeightDict = {}
        for i in range(1, len(reSpPlanes)):

            areaDict = {}
            weightDict = {}
            for key, val in workDict.items():

                matrix_vtx = self.getVertMatrix(meshName, key)
                #print matrix_vtx
                relativeMat = matrix_vtx * reSpPlanesMatrixInv[i - 1]

                transRmat = om.MTransformationMatrix(relativeMat)

                transPosMin = transRmat.translation(om.MSpace.kWorld)

                if transPosMin.x > 0:
                    relativeMat = matrix_vtx * reSpPlanesMatrixInv[i]

                    transRmat = om.MTransformationMatrix(relativeMat)

                    transPosMax = transRmat.translation(om.MSpace.kWorld)

                    if transPosMax.x <= 0:
                        areaDict.update({key: val})
                        totalC = abs(transPosMin.x) + abs(transPosMax.x)
                        minVal = abs(transPosMin.x) / float(totalC)
                        # maxVal = abs(transPosMax.y)/float(totalC)
                        weightDict.update({key: minVal})
            returnAreaDict.update({outterCount: areaDict})
            returnWeightDict.update({outterCount: weightDict})
            outterCount += 1

        return {'area': returnAreaDict, 'weight': returnWeightDict}

    def changeAreaColor(self, meshName,areaArray,colorArray):

        areaIDtoColor = {}
        count = 0
        for aa in areaArray.keys():
            for i in areaArray[aa].keys():
                vtxName = '%s.vtx[%s]' % (meshName, str(i))
                cmds.polyColorPerVertex(vtxName, rgb=colorArray[count], colorDisplayOption=True)

            areaIDtoColor.update({aa: colorArray[count]})
            count += 1



    def bezierCurve_fn(self, inputVal, rangeX=0.3, rangeY=0.0):
        if 0 <= inputVal <= 1.0 and 0 <= rangeX <= 1.0 and 0.0 <= rangeY <= 0.5:
            pointArray = [[0.0, 0.0], [rangeX, rangeY], [0.5, 0.5], [1.0 - rangeX, 1.0 - rangeY], [1.0, 1.0]]
            t = 0

            if inputVal < 0.5:
                p0 = pointArray[0]
                p1 = pointArray[1]
                p2 = pointArray[2]
                t = inputVal * 2.0
            else:
                t = (inputVal - 0.5) * 2.0
                p0 = pointArray[2]
                p1 = pointArray[3]
                p2 = pointArray[4]

            p0attr = math.pow(1.0 - t, 2)
            p1attr = 2.0 * t * (1.0 - t)
            p2attr = math.pow(t, 2)
            p0mul = [p0[0] * p0attr, p0[1] * p0attr]
            p1mul = [p1[0] * p1attr, p1[1] * p1attr]
            p2mul = [p2[0] * p2attr, p2[1] * p2attr]
            result = [p0mul[0] + p1mul[0] + p2mul[0], p0mul[1] + p1mul[1] + p2mul[1]]
            #print result
            return result
        else:
            print 'inputVal range is [0,1]\nrangeX range is [0,1]\nrangeY range is [0,0.5]\n'
            '''
            for i in range(100):
                pos = bezierCurve_fn(i * 0.01, rangeX=0.3, rangeY=0.2)
                gg = cmds.spaceLocator()[0]
                cmds.setAttr(gg + '.tx', pos[0] * 10)
                cmds.setAttr(gg + '.tz', pos[1] * 10)
            '''

    def getWeightDict(self, areaDictTempA, indexArray, keyY_min=0.0, keyY_max=0.0, disableMax=False, disableMin=False):
        areaArray = areaDictTempA['area']
        weightDict = areaDictTempA['weight']

        # indexArray = [0,1]
        minArray = areaArray[indexArray[0]]
        maxArray = areaArray[indexArray[1]]

        minWeight = weightDict[indexArray[0]]
        maxWeight = weightDict[indexArray[1]]

        weightDictOut = {}

        # print minArray.keys()
        #print 'printing MIN weights =================================='
        for i in minArray.keys():
            #print i
            weightVal = 1.0
            if disableMin:
                weightVal = 0.0
            else:
                weightVal = self.bezierCurve_fn(1.0 - minWeight[i], rangeY=keyY_min)[1]

            #print weightVal
            weightDictOut.update({i: weightVal})

        #print 'printing MAX weights =================================='
        for i in maxArray.keys():
            #print i
            weightVal = 1.0
            if disableMax:
                weightVal = 0.0
            else:
                weightVal = self.bezierCurve_fn((maxWeight[i]), rangeY=keyY_max)[1]

            weightDictOut.update({i: weightVal})
            #print weightVal
        return weightDictOut


    def workDictToMoveDict(self, workDict):
        moveDict = {}
        for key, val in workDict.items():
            tempA = []
            for i in range(3):
                tv = val['b'][i] - val['o'][i]
                tempA.append(tv)

            moveDict.update({key: tempA})

        return moveDict


    def makeBigRangeDict(self, bsName,minP,midP,maxP):
        returnDict = {
            'max': 0,
            'min': 0,
            'mid': 0,
            'maxRange': 0,
            'minRange': 0
        }
        tempMin = self.getRange(bsName, minP, midP)
        returnDict['min'] = tempMin['min']
        returnDict['mid'] = tempMin['max']
        returnDict['minRange'] = tempMin['range']
        tempMax = self.getRange(bsName, midP, maxP)
        returnDict['max'] = tempMax['max']
        returnDict['maxRange'] = tempMax['range']
        return returnDict


    def executeVertexMoving(self, execDict, meshName):
        #print '=====dict ====='
        #print execDict
        #print execDict.items()

        for key, val in execDict.items():
            #print str(meshName) + str(key)
            #print val
            cmds.xform(str(meshName) + str(key), os=1, t=val)
        return True

    def makeExecuteDict(self, wDict, workDict,isInverse = True):
        mDict = self.workDictToMoveDict(workDict)
        # print mDict
        excuteDict = {}

        for key in mDict.keys():
            val = mDict[key]
            vtxName = '.vtx[%s]' % (str(key))

            baseArray = workDict[key]['o']

            moveArray = []

            for v, b in zip(val, baseArray):
                tempV = []
                if key in wDict.keys():
                    wt = wDict[key]
                    if isInverse:
                        wt = 1.0 - wDict[key]
                    tempV = (v * wt) + b
                else:
                    tempV = b

                moveArray.append(tempV)

            excuteDict.update({vtxName: moveArray})
        return excuteDict


    def refreshExcuteDict(self,meshName,spPlanes,workDict,curDict = {0: 0.3,1: 0.3,2: 0.3},isCombieBorder = True):

        areaDictTemp = self.getAreaDict(meshName, spPlanes, workDict)

        finalDictArray = []

        for i in range(1,len(spPlanes)-1):
            if i == 1:
                newDict = self.getWeightDict(areaDictTemp, [i-1, i], keyY_min = curDict[i-1],keyY_max = curDict[i],
                                             disableMin=True)
            elif i == (len(spPlanes)-2):
                newDict = self.getWeightDict(areaDictTemp, [i - 1, i], keyY_min=curDict[i - 1], keyY_max=curDict[i],
                                             disableMax=True)
            else:
                newDict = self.getWeightDict(areaDictTemp, [i - 1, i], keyY_min=curDict[i - 1], keyY_max=curDict[i])

            mDict = self.makeExecuteDict(newDict, workDict)

            finalDictArray.append(mDict)


        return finalDictArray




    def getVertMatrix(self,*args):
        if args:
            theVtx = ''
            if len(args) == 1:
                theVtx = args[0]
            elif len(args) == 2:
                theVtx = '%s.vtx[%s]' % (str(args[0]), str(args[1]))


            theMatB = cmds.xform(theVtx, q=1, ws=1, m=1)
            thePos = cmds.xform(theVtx, q=1, ws=1, t=1)
            theMatB[-4] = thePos[0]
            theMatB[-3] = thePos[1]
            theMatB[-2] = thePos[2]

            matrix_vtx = om.MMatrix()
            util_vtx = om.MScriptUtil()
            util_vtx.createMatrixFromList(theMatB, matrix_vtx)

            return matrix_vtx

    def objToSkin(self, sel):
        shps = cmds.listRelatives(sel, s=1)

        sCluster = ''
        for sh in shps:
            cnts = cmds.listConnections(sh)
            toBreak = False
            if cnts:
                for cn in cnts:
                    if cmds.objectType(cn) == 'skinCluster':
                        sCluster = cn
                        toBreak = True
                        break
            if toBreak:
                break
        return sCluster


    def getSkinMapDict(self, sel, area='all'):
        theSkin = self.objToSkin(sel)
        jointDict = False
        if theSkin:
            jointDict = {}

            loopArray = []

            if area == 'all':
                pass
            elif isinstance(area, dict):
                loopArray = area.keys()

            for i in loopArray:
                vtxName = '%s.vtx[%s]' % (sel, str(i))
                valTemp = cmds.skinPercent(theSkin, vtxName, q=1, v=1, r=True)
                nameTemp = cmds.skinPercent(theSkin, vtxName, query=True, transform=None)
                innerDict = {}
                for v, n in zip(valTemp, nameTemp):
                    innerDict.update({n: v})
                jointDict.update({i: innerDict})

        return jointDict


    def convertSkinMapToJointMap(self, skinMap, filterVal=0.000000001):
        jntDict = {}
        for vtx, dc in skinMap.items():
            for key, val in dc.items():
                if val != 0 and val > filterVal:
                    if key not in jntDict.keys():
                        jntDict.update({key: {vtx: val}})
                    else:
                        tempDict = {vtx: val}
                        jntDict[key].update(tempDict)

        return jntDict



#==============================



'''

theClass = splitBSback_Class()

meshName = 'browDown'
bDict = theClass.meshPointDict(meshName)

polyName = 'Head_01_Geo1'
oDict = theClass.meshPointDict(polyName)

workDict = theClass.markWorkArea(meshName, oDict, bDict)

print workDict

spPlanes = theClass.createSplitPlane(meshName)
print spPlanes
############
areaDictTemp = getAreaDict(meshName, spPlanes, workDict)
areaArray = areaDictTemp['area']
weightDict = areaDictTemp['weight']
print areaArray.keys()
print weightDict.items()


colorArray = theClass.getColorArray(len(areaArray.keys()))
colorDict = theClass.changeAreaColor(meshName, areaArray, colorArray)

# <-----------
print

newDict = getWeightDict(theClass,areaDictTemp,[0,1],disableMin=True)

print newDict

print newDict[3050]


mDict = makeExecuteDict(theClass,newDict,workDict)

theClass.executeVertexMoving(mDict,'browDown2')


'''

