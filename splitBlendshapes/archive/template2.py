import maya.cmds as cmds
import math
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
                #print str(orVal) + ' != ' + str(brVal)
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

    def getAreaDict(self, meshName,spPlanes,workDict):
        reSpPlanes = []
        for sp in spPlanes:
            #print sp

            pl = sp[:-5]
            reSpPlanes.append(pl)

        rangeArray = []
        for i in range(1, len(reSpPlanes)):

            minP = reSpPlanes[i-1]
            maxP = reSpPlanes[i]

            rangeTemp = self.getRange(meshName, minP, maxP)

            rangeArray.append(rangeTemp)

        # print workDict

        returnAreaDict = {}
        for count, ra in enumerate(rangeArray):
            areaDict = {}
            for key, val in workDict.items():
                if ra['min'] <= val['b'][0] <= ra['max']:
                    areaDict.update({key: val})
            returnAreaDict.update({count: areaDict})
        return returnAreaDict



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


    def getWeightDict(self, workDict, rangeDict, keyY_min=0.0, keyY_max=0.0, disableMax=False, disableMin=False):
        maxVal = rangeDict['max']
        minVal = rangeDict['min']
        midVal = rangeDict['mid']
        maxRange = rangeDict['maxRange']
        minRange = rangeDict['minRange']

        weightDict = {}
        for key, val in workDict.items():
            bval = val['b'][0]
            weightVal = 1.0
            if midVal <= bval < maxVal:
                if disableMax:
                    weightVal = 0.0
                else:
                    absVal = bval - midVal
                    xVal = float(absVal) / float(maxRange)
                    # weightVal = scale * (math.sin(xVal + offset))
                    # xVal = (float(absVal) / float(maxRange)) * scaleX
                    weightVal = self.bezierCurve_fn(xVal, rangeY=keyY_max)[1]
                    # weightVal += maintainCenter

            elif midVal > bval > minVal:
                if disableMin:
                    weightVal = 0.0
                else:
                    absVal = midVal - bval
                    xVal = float(absVal) / float(minRange)
                    weightVal = self.bezierCurve_fn(xVal, rangeY=keyY_min)[1]

            if weightVal > 1.0:
                print 'over'
                weightVal = 1.0

            if weightVal < 0.0:
                print 'below'
                weightVal = 0.0
            weightDict.update({key: weightVal})
        return weightDict


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
            cmds.xform(meshName + key, os=1, t=val)
        return True

    def makeExecuteDict(self, wDict, workDict):
        mDict = self.workDictToMoveDict(workDict)
        excuteDict = {}
        for key, val in mDict.items():
            vtxName = '.vtx[%s]' % (str(key))
            baseArray = workDict[key]['o']
            moveArray = []
            for v, b in zip(val, baseArray):
                tempV = (v * (1.0 - wDict[key])) + b
                moveArray.append(tempV)
            excuteDict.update({vtxName: moveArray})
        return excuteDict


    def refreshExcuteDict(self,meshName,spPlanes,workDict,curDict = {0: 0.3,1: 0.3,2: 0.3},isCombieBorder = True):

        reSpPlanes = []
        for sp in spPlanes:
            pl = sp[:-5]
            reSpPlanes.append(pl)

        finalDictArray = []
        if isCombieBorder:

            bigRangeArray = []
            for i in range(1, len(reSpPlanes)-1):

                mbrd = self.makeBigRangeDict(meshName, reSpPlanes[i-1], reSpPlanes[i], reSpPlanes[i+1])
                bigRangeArray.append(mbrd)

            for count, bra in enumerate(bigRangeArray):

                res = []
                if count == 0:
                    res = self.getWeightDict(workDict, bra, keyY_min=curDict[count], keyY_max=curDict[count+1], disableMax=False, disableMin=True)
                elif count == (len(bigRangeArray)-1):
                    res = self.getWeightDict(workDict, bra, keyY_min=curDict[count], keyY_max=curDict[count+1], disableMax=True, disableMin=False)
                else:
                    res = self.getWeightDict(workDict, bra, keyY_min=curDict[count], keyY_max=curDict[count+1], disableMax=False, disableMin=False)

                exTemp = self.makeExecuteDict(res,workDict)
                finalDictArray.append(exTemp)
        else:
            print 'enter not combie border\n'
            print reSpPlanes
            print 'HHHHHHHHHHHHHHHHH'
            bigRangeArray = []
            for ff in range(len(reSpPlanes)):
                print '$$$$$   ' + str(ff)
                print '$$$$$   ' + str(len(reSpPlanes))
                prePlane = ''
                afterPlane = ''
                if ff==0:
                    prePlane = reSpPlanes[ff]
                else:
                    prePlane = reSpPlanes[ff-1]

                if ff == (len(reSpPlanes)-1):
                    afterPlane = reSpPlanes[ff]
                else:
                    print 'fuck i:' + str(ff)
                    afterPlane = reSpPlanes[ff+1]

                print 'pre:' + str(prePlane)
                print 'mid:' + str(reSpPlanes[ff])
                print 'aft:' + str(afterPlane)

                mbrd = self.makeBigRangeDict(meshName, prePlane, reSpPlanes[ff], afterPlane)
                bigRangeArray.append(mbrd)

            for count, bra in enumerate(bigRangeArray):


                res = self.getWeightDict(workDict, bra, keyY_min=curDict[count], keyY_max=curDict[count + 1],
                                         disableMax=False, disableMin=False)

                exTemp = self.makeExecuteDict(res, workDict)
                finalDictArray.append(exTemp)


        return finalDictArray
'''

theClass = splitBSback_Class()

bsName = 'browDown'
bDict = theClass.meshPointDict(bsName)

polyName = 'Head_01_Geo1'
oDict = theClass.meshPointDict(polyName)

workDict = theClass.markWorkArea(bsName, oDict, bDict)

print workDict

refLineDict = createSingleReferenctLine(bsName)

# =====================

print refLineDict
rangeDict = {'r': u'referencePlane_Right1', 
             'm': u'referencePlane_Mid1', 
             'l': u'referencePlane_Left1'}


rangeDict = getRange(refLineDict)

wDict = getWeightDict(workDict,rangeDict,keyY=0.0,disableMin=True)

mDict = workDictToMoveDict(workDict)

for key, val in mDict.items():
    vtxName = '%s.vtx[%s]' % (bsName,str(key))
    baseArray = workDict[key]['o']
    moveArray = []
    for v,b in zip(val, baseArray):

        tempV = (v * (1.0 - wDict[key])) + b
        moveArray.append(tempV)

    cmds.xform(vtxName, os=1, t=moveArray)

'''
#if __name__ == '__main__':


#def createSingleReferenctLine(meshName):


'''

colorArray = getColorArray(len(areaArray.keys()))

# change color


theClass = splitBSback_Class()

meshName = 'browDown6'
bDict = theClass.meshPointDict(meshName)

polyName = 'Head_01_Geo1'
oDict = theClass.meshPointDict(polyName)

workDict = theClass.markWorkArea(meshName, oDict, bDict)

spPlanes = createSplitPlane(meshName)
############
areaArray = getAreaDict(meshName, spPlanes, workDict)

if not colorArray:
    colorArray = getColorArray(len(areaArray.keys()))
colorDict = changeAreaColor(meshName, areaArray, colorArray)

finalDictArray = refreshExcuteDict(spPlanes,workDict,curDict = {0: 0.3,1: 0.3,2: 0.3})

executeStep(finalDictArray[0],'browDown7')

'''





