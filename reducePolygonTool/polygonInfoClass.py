import maya.cmds as cmds


class polygonInfomation_Class():
    polyName = ''









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


    def getBaseStructEdgeInformation(self, polyName,vertInformationDict,delLevel=1):

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

    # ============= older version classes =================
    def __init__(self):
        self.polyName = ''

        self.keyVerts = []
        self.creaseVerts = []
        self.middleVerts = []


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

    def getStructVerts(self, is2=True, is4=True):

        if is2 or is4:

            polyCount = cmds.polyEvaluate(self.polyName, v=1)

            vertArray = []
            midVertArray = []
            creaseVertexArray = []

            for i in range(polyCount):

                vert = '%s.vtx[%s]' % (self.polyName, str(i))
                edgeInfo = cmds.polyInfo(vert, vertexToEdge=1)
                edgeID = self.cleanInfos(edgeInfo[0])

                # get vert who own the defined number of edges.
                IDlength = len(edgeID)

                isThisVertexImportent = False
                if is4:
                    if IDlength > 4:
                        vertArray.append(i)
                        isThisVertexImportent = True
                if is2:
                    if IDlength == 2:
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

            self.keyVerts = vertArray
            self.middleVerts = midVertArray
            self.creaseVerts = creaseVertexArray



    def getEdgesByVertex(self, vid):

        vert = '%s.vtx[%s]' % (self.polyName, str(vid))

        if cmds.objExists(vert):

            edgeInfo = cmds.polyInfo(vert, vertexToEdge=1)

            edgeID = self.cleanInfos(edgeInfo[0])

            relativeList = []
            for eid in edgeID:
                edgeLoop = cmds.polySelect(self.polyName, edgeLoop=int(eid), ass=0, q=1)

                intArray = []
                for el in edgeLoop:
                    intArray.append(int(el))

                if self.isEdgesListMirror(intArray):
                    spArray = self.splitLinesByMiddle([intArray])
                    for spa in spArray:
                        if int(eid) in spa:
                            relativeList.append(spa)
                else:
                    relativeList.append(intArray)

            return relativeList


    def getBaseStructEdgeInformation_ready(self, delLevel=1):

        cleanVertArray = list(self.keyVerts)

        edgeLoopArray = []
        # get the base struct edges.
        vertToStructEdgeDict = {} # return value

        for count, cva in enumerate(cleanVertArray):
            edges = self.getEdgesByVertex(cva)
            vertToStructEdgeDict.update({cva: edges})
        '''
            vert = '%s.vtx[%s]' % (self.polyName, str(cva))

            edgeInfo = cmds.polyInfo(vert, vertexToEdge=1)

            edgeID = self.cleanInfos(edgeInfo[0])

            relativeList = []
            for eid in edgeID:
                edgeLoop = cmds.polySelect(self.polyName, edgeLoop=int(eid), ass=0, q=1)
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
        '''
pic = polygonInfomation_Class()
pic.polyName = 'closeeyes1'
pic.getStructVerts()

gg = pic.getEdgesByVertex(709)
for g in gg:
    print g

print ''
ff = pic.getEdgesByVertex(512)
for f in ff:
    print f

'''
=============result===================
[3398, 2844, 1607, 1835, 1830, 2426, 2428, 2315, 2403, 4723, 1825, 641, 3084, 633, 439, 2078, 3135, 624, 625, 3903, 5123, 5044, 3902, 5251, 5417, 5328, 3985, 3604, 3984, 3703, 4032, 3803, 4090, 4372, 4180, 4253]
[1838, 2852, 1979, 1099, 2054, 1087, 1032, 432, 687, 1496, 1019, 1043, 3395, 1339, 1356, 466, 667, 470, 644]
[1559, 1561, 2468, 3377, 2483, 1565, 1844, 1847, 1955, 720, 4432, 4627, 4674, 4515, 4513]
[997, 974, 482, 722, 620, 2187, 1521, 1670, 1525]
[4922, 2275, 4992, 3423, 2744, 2746, 2748, 2751, 2753, 2758, 2761, 2771, 2787, 2272, 2139, 2148, 3304, 3306, 3234, 3212, 3211, 3162, 3156, 3167, 995, 998]

[1525, 1670, 1521, 2187, 620, 722, 482, 974, 997]
[643, 1070, 2510, 3386, 978, 1067, 1240, 1085, 1479, 752, 4449, 4645, 4683, 4571, 4544]
[1838, 2852, 1979, 1099, 2054, 1087, 1032, 432, 687, 1496, 1019, 1043, 3395, 1339, 1356, 466, 667, 470, 644]
[1517, 1461, 1396, 671, 662, 1726, 2152, 3314, 4792, 679]
[1768, 160, 836, 1235, 1571, 1518]




'''
