import maya.cmds as cmds

class reduceFace_FalloffVersion_class():
    polyName = ''

    def cleanInfos(self, vid):
        # vid = 'Head_01_Geo2.vtx[2660]'
        #
        # clean the none digital infos like:
        # sss = 'VERTEX   2660:  15050   5165   5167   5168 \n'

        gets = vid.split(' ')
        collect = []
        for g in gets:
            if g.isdigit():
                collect.append(int(g))
        return collect

    def isEdgesListMirror(self, inputEdgeArray):
        edgeNameEnd = '%s.e[%s]' % (self.polyName, str(inputEdgeArray[-1]))
        edgeEndPos = cmds.xform(edgeNameEnd, ws=1, q=1, t=1)
        edgeEndPos = [round(i, 6) for i in edgeEndPos]

        edgeNameStart = '%s.e[%s]' % (self.polyName, str(inputEdgeArray[0]))
        edgeStartPos = cmds.xform(edgeNameStart, ws=1, q=1, t=1)
        edgeStartPos = [round(i, 6) for i in edgeStartPos]

        edgeStartPos[0] *= -1
        edgeStartPos[3] *= -1

        return (edgeStartPos == edgeEndPos)


    def splitLinesByMiddle(self, inputEdgeloopArray):
        returnArray = []

        tempA = []
        for i in inputEdgeloopArray:
            if (len(i) % 2) == 0:
                tempA.append(i)
            else:
                returnArray.append(i)
        tempB = []
        for ta in tempA:
            if self.isEdgesListMirror(ta):
                tempB.append(ta)
            else:
                returnArray.append(ta)

        for tb in tempB:
            midVal = len(tb) / 2
            returnArray.append(tb[:midVal])
            returnArray.append(tb[midVal:])

        return returnArray

    def selVertByIntArray(self, inputArray,add=False):
        if not add:
            cmds.select(cl=1)
        for i in inputArray:
            vertString = '%s.vtx[%s]' % (self.polyName,str(i))
            cmds.select(vertString,add=1)


    def selEdgeByIntArray(self, inputArray,add=False):
        if not add:
            cmds.select(cl=1)
        for i in inputArray:
            vertString = '%s.e[%s]' % (self.polyName,str(i))
            cmds.select(vertString, add=1)

    def getMiddleEdgeByMiddleVerts(self, middVerts):
        middleEdgeArray = []
        for mea in middVerts:
            edgeLoop = cmds.polySelect(self.polyName, edgeLoop=mea, ass=0, q=1)
            edgeName = '%s.e[%s]' % (self.polyName, str(int(edgeLoop[0])))
            edgePos = cmds.xform(edgeName,ws=1,q=1,t=1)
            if round(edgePos[0],5) == 0:
                edgeName = '%s.e[%s]' % (self.polyName, str(int(edgeLoop[-1])))
                edgePos = cmds.xform(edgeName,ws=1,q=1,t=1)
                if round(edgePos[0],5) == 0:
                    intArray = [int(i) for i in edgeLoop]

                    if intArray not in middleEdgeArray:
                        middleEdgeArray.append(intArray)
        return middleEdgeArray


    def edgeToVertex_List(self, edgeNumber):
        te = '%s.e[%s]' % (self.polyName, str(edgeNumber))
        vertInfo = cmds.polyInfo(te, edgeToVertex=1)
        vertID = self.cleanInfos(vertInfo[0])
        return vertID

    def edgeListToVertList(self, tEdge):
        lastTemp = self.edgeToVertex_List(tEdge[0])
        vertArrayTemp = []
        for i in range(1, len(tEdge)):
            nowArray = self.edgeToVertex_List(tEdge[i])
            intersection = list(set(lastTemp).intersection(set(nowArray)))
            vertArrayTemp.append(intersection[0])
            lastTemp = list(nowArray)

        startTemp = self.edgeToVertex_List(tEdge[0])
        for st in startTemp:
            if st not in vertArrayTemp:
                vertArrayTemp = [st] + vertArrayTemp
        endTemp = self.edgeToVertex_List(tEdge[-1])
        for ed in endTemp:
            if ed not in vertArrayTemp:
                vertArrayTemp = vertArrayTemp + [ed]

        return vertArrayTemp


    def getVertInformation(self, polyName,isMoreThan4=True, is2=True, is3=False):
        polyCount = cmds.polyEvaluate(polyName, v=1)

        vertArray = []
        midVertArray = []
        creaseVertexArray = []
        if isMoreThan4 or is2 or is3:
            for i in range(polyCount):
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
                    midVertArray.append(i)

                # get crease vertex.this vertex just for 2,3,5 and 5+ stars vertex.
                if isThisVertexImportent:
                    cVal = cmds.polyCrease(vert, q=1, vertexValue=1)
                    if cVal[0] > 0:
                        creaseVertexArray.append(int(i))
            return {'keyVerts': vertArray, 'middleVerts': midVertArray, 'creaseVerts': creaseVertexArray}
        else:
            print 'you need defined a type of vert to get.isMoreThan4 or is2 or is3?'
            return False


    def getBaseStructEdgeInformation(self, polyName,vertInformationDict):

        cleanVertArray = vertInformationDict['keyVerts']

        edgeLoopArray = []
        # get the base struct edges.
        vertToStructEdgeDict = {} # return value
        simpleStructEdgeArray = []
        for count, cva in enumerate(cleanVertArray):

            vert = '%s.vtx[%s]' % (polyName, str(cva))

            edgeInfo = cmds.polyInfo(vert, vertexToEdge=1)

            edgeID = self.cleanInfos(edgeInfo[0])

            relativeList = []
            for eid in edgeID:
                edgeLoop = cmds.polySelect(polyName, edgeLoop=int(eid), ass=0, q=1)
                if len(edgeLoop) > (delLevel+1): # filter the items which length not enough.
                    intArray = []
                    for el in edgeLoop:
                        intArray.append(int(el))
                    if intArray:
                        if intArray not in edgeLoopArray:
                            edgeLoopArray.append(intArray)

                        # collect information {vert:[edge1,edge2,...edge5]}}
                        if self.isEdgesListMirror(intArray):
                            spArray = self.splitLinesByMiddle([intArray])
                            for spa in spArray:
                                if int(eid) in spa:
                                    relativeList.append(spa)
                        else:
                            relativeList.append(intArray)
            vertToStructEdgeDict.update({str(cva): relativeList})

        # restore edges start from key vert.


        edgeLoopArrayWithoutMiddle = list(edgeLoopArray)
        spEdgeLoopArray = self.splitLinesByMiddle(edgeLoopArray)
        spEdgeLoopArray += (self.getMiddleEdgeByMiddleVerts(vertInformationDict['middleVerts']))
        edgeLoopArrayWithoutMiddle += (self.getMiddleEdgeByMiddleVerts(vertInformationDict['middleVerts']))

        # create struct weight
        structWeightDict = {} # return value
        for spela in spEdgeLoopArray:
            structWeightDict.update({str(spela): 1})

        # add edge weight(crease vertex)
        creaseVertArray = vertInformationDict['creaseVerts']
        if creaseVertArray:
            for cva in creaseVertArray:
                edgeArray = vertToStructEdgeDict[str(cva)]
                for ea in edgeArray:
                    structWeightDict[str(ea)] += 1

        structEdgeToVertsDict = {} # return value.very important
        for spela in spEdgeLoopArray:
            vertTempA = self.edgeListToVertList(spela)
            intArray = []
            for vta in vertTempA:
                intArray.append(int(vta))
            structEdgeToVertsDict.update({str(spela): intArray})

        structEdges = []
        for spela in spEdgeLoopArray:
            #print spela
            for sa in spela:
                structEdges.append(int(sa))

        return {'keyVertToStructEdgeDict': vertToStructEdgeDict,
                'structEdgeWeightDict': structWeightDict,
                'structEdgeToVertsDict': structEdgeToVertsDict,
                'structEdgeFlat': structEdges,
                'edgeLoopArrayWithoutMiddle': edgeLoopArrayWithoutMiddle,
                'structEdgeList': spEdgeLoopArray}


    def getCrossByStructEdge(self, evDict, sigEdge):
        if str(sigEdge) in evDict.keys():

            sigEdgeVerts = evDict[str(sigEdge)]

            sigEdgeCrossDict = {}
            for sev in sigEdgeVerts[1:-1]:
                vert = '%s.vtx[%s]' % (self.polyName, str(sev))

                edgeInfo = cmds.polyInfo(vert, vertexToEdge=1)

                edgeID = self.cleanInfos(edgeInfo[0])

                for eid in edgeID:

                    if eid not in sigEdge:
                        edgeLoop = cmds.polySelect(self.polyName, edgeLoop=int(eid), ass=0, q=1)
                        intArray = []
                        for el in edgeLoop:
                            intArray.append(int(el))
                        sigEdgeCrossDict.update({sev: intArray})
                        break
            return sigEdgeCrossDict
        else:
            print 'input edge is not in evDict.you need calculate evDict,include the edge you inputted.'


    def getStructVertToCrossEdgeDict(self, evDict, SEedges, fullStructs):
        tempFullStructs = list(fullStructs)
        for fs in tempFullStructs:
            fs.sort()

        structVertToCrossEdgeDict = {}
        structVertWeightDict = {}
        for see in SEedges:

            theDict = self.getCrossByStructEdge(evDict, see)

            if theDict:
                for key, val in theDict.items():
                    copyval = list(val)
                    copyval.sort()
                    if copyval not in tempFullStructs:

                        structVertToCrossEdgeDict.update({key: val})

                    else:
                        structVertToCrossEdgeDict.update({key: False})

                    structVertWeightDict.update({key: 0})

        return {'structVertToCrossEdgeDict': structVertToCrossEdgeDict,
                'structVertWeightDict': structVertWeightDict}


    def getFalloffDict(self, polyName, falloffkdTemp):
        falloffkd = dict(falloffkdTemp)

        falloffkdSSR = {}

        for key, val in falloffkd.items():
            if val:
                tempA = val
                tempList = []
                for ta in tempA:

                    edge = '%s.e[%s]' % (polyName, str(ta[0]))
                    edgeInfo = cmds.polyInfo(edge, edgeToVertex=1)
                    edgeID = self.cleanInfos(edgeInfo[0])
                    if int(key) in edgeID:
                        tempList.append(ta)
                    else:
                        edge2 = '%s.e[%s]' % (polyName, str(ta[-1]))
                        edgeInfo2 = cmds.polyInfo(edge2, edgeToVertex=1)
                        edgeID2 = self.cleanInfos(edgeInfo2[0])
                        if int(key) in edgeID2:
                            ta.reverse()
                        tempList.append(ta)
                falloffkdSSR.update({key: tempList})

        returnDict = {}

        for key, val in falloffkdSSR.items():
            vTemp = []
            for v in val:
                vlist = self.edgeListToVertList(v)

                valList = []
                for i in range(len(vlist)):
                    tempv = round(float(i) / float(len(vlist)), 6)
                    valList.append(1.0 - tempv)
                #print vlist
                #print valList
                #print '==='
                vTemp.append(valList)
            returnDict.update({key:vTemp})
        return {'ssr': falloffkdSSR, 'weight': returnDict}

    def mainRule(self, inputDict,SVweightIn,delLevel = 1,weightVal = 10):
        spLen = delLevel +1
        SVweightInTemp = dict(SVweightIn)
        svk = SVweightInTemp.keys()
        for key, val in inputDict.items():
            spTemp = []
            for i in range(0, len(val)-1, spLen):
                nextVal = i + spLen
                if nextVal > len(val)-1:
                    nextVal = len(val)-1
                spTemp.append(val[i:nextVal])

            for st in spTemp:
                if st and len(st)>1:
                    if st[0] in svk:
                        SVweightInTemp[st[0]] -= weightVal
                    for sb in st[1:]:
                        if sb in svk:
                            SVweightInTemp[sb] += weightVal
        return SVweightInTemp

    def falloffRule(self, falloffCombieData,weightIn,weightVal = 100):

        #falloffCombieData = dict(falloffDict)
        ssrDict = falloffCombieData['ssr']
        FWDict = falloffCombieData['weight']

        falloffOverDict = {}

        for k in ssrDict.keys():

            for tc,ssr in enumerate(ssrDict[k]):
                for count,s in enumerate(ssr):

                    if s in weightIn.keys():
                        valTemp = weightIn[s]
                        val =  FWDict[k][tc][count] + (weightVal * valTemp)
                        falloffOverDict.update({s: val})
                    else:
                        print False
        return falloffOverDict



    def main(self, polyName, clamp = 0, delLevel = 1, isfallOffModules = True):
        self.polyName = polyName
        vertArrayDictTemp = self.getVertInformation(polyName)
        edgeInfoDictTemp = self.getBaseStructEdgeInformation(polyName,vertArrayDictTemp)

        falloffkd = dict(edgeInfoDictTemp['keyVertToStructEdgeDict'])
        falloffDict = self.getFalloffDict(polyName, falloffkd)

        evDict = edgeInfoDictTemp['structEdgeToVertsDict']
        SEedges = edgeInfoDictTemp['structEdgeList']

        fullStructs = edgeInfoDictTemp['edgeLoopArrayWithoutMiddle']

        transATemp = self.getStructVertToCrossEdgeDict(evDict, SEedges, fullStructs)

        SVtoCEDict = transATemp['structVertToCrossEdgeDict'] # all edges who could be delete.
        SVweight = transATemp['structVertWeightDict']


        okDict = {}
        noDict = {}
        for key, val in evDict.items():
            fastCheck = (len(val) - 1) % (delLevel + 1)
            if fastCheck == 0:
                okDict.update({key: val})
            else:
                noDict.update({key: val})

        resultDict = {}
        call1Dict = self.mainRule(noDict, SVweight, weightVal=10)
        call2Dict = self.mainRule(okDict, call1Dict, weightVal=100)

        if isfallOffModules:
            resultDict = self.falloffRule(falloffDict, call2Dict)
        else:
            resultDict = call2Dict

        tempGG = []
        delVert = []

        splitLine = int(clamp)

        for key, val in resultDict.items():
            #print 'key: %s , val : %s \n' % (str(key),str(val))
            if val == splitLine:
                tempGG.append(key)
            if val > splitLine:
                delVert.append(key)

        delEdge = []
        for dv in delVert:
            edge = SVtoCEDict[dv]
            if edge:
                delEdge.append(edge)

        return delEdge



'''
jjy = reduceFace_FalloffVersion_class()
delLevel = 1
polyName = 'closeeyes1'
rltssss = jjy.main(polyName,clamp=100,isfallOffModules = True,delLevel = 1)

for i in rltssss:
    selEdgeByIntArray(i,add=1)


'''




