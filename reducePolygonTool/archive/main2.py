import maya.cmds as cmds

def selVertByIntArray(polyName,inputArray,add=False):
    if not add:
        cmds.select(cl=1)
    for i in inputArray:
        vertString = '%s.vtx[%s]' % (polyName,str(i))
        cmds.select(vertString,add=1)

def selEdgeByIntArray(polyName,inputArray,add=False):
    if not add:
        cmds.select(cl=1)
    for i in inputArray:
        vertString = '%s.e[%s]' % (polyName,str(i))
        cmds.select(vertString,add=1)

def cleanInfos(vid):
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


def getAllVertsWhoHave5edges(polyName):
    polyCount = cmds.polyEvaluate(polyName, v=1)

    # sss = 'VERTEX   2660:  15050   5165   5167   5168 \n'
    vertArray = []

    for i in range(polyCount):

        vert = '%s.vtx[%s]' % (polyName, str(i))

        edgeInfo = cmds.polyInfo(vert, vertexToEdge=1)
        #print edgeInfo

        edgeID = cleanInfos(edgeInfo[0])

        IDlength = len(edgeID)

        #if IDlength == 3 or IDlength > 4:
        if IDlength > 4:

            vertArray.append(i)
    return vertArray


def getBaseStructEdges(polyName):

    cleanVertArray = getAllVertsWhoHave5edges(polyName)
    edgeLoopArray = []
    sortTemp = []
    for cva in cleanVertArray:

        vert = '%s.vtx[%s]' % (polyName, str(cva))

        edgeInfo = cmds.polyInfo(vert, vertexToEdge=1)

        edgeID = cleanInfos(edgeInfo[0])


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
    return edgeLoopArray



def preCheck(divAttr,edgeArray):
    # for check the data array lenth.
    # if the length of item in every subArrays are same.
    # it is a perfact data.
    # not finish yet.
    troubleCount = 0
    troubleList = []
    for ela in edgeArray:
        if len(ela) < divAttr:
            troubleCount += 1
            troubleList.append(ela)
    if troubleCount:
        cmds.warning(str(troubleCount) + ' troubles was found.this polygon is not a perfact smoothed polygon.do you wanna continue?')

def calculateBaseDeleteArray(polyName,delLevel=1):
    # delLevel attr means smooth level 1 to reverse
    divAttr = delLevel+1

    edgeArray = getBaseStructEdges(polyName)
    # every item in the array is unique.it's all fine.

    wholeEdges = []
    for i in edgeArray:
        wholeEdges += i

    selEdgeArray = []

    for ela in edgeArray:
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

                    vtxID = cleanInfos(vtx[0])

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

                edgeID = cleanInfos(edgeInfo[0])

                # rule 1.the line can not in the base protect array.
                # in the touch point.there're two edges in base protect array.
                # now i need collect all of rest items.
                cellArray = []
                for eid in edgeID:
                    if not(int(eid) in wholeEdges):
                        cellArray.append(int(eid))

                crossEdges.append(cellArray)

            #selEdgeByIntArray(polyName,crossEdges)
            selEdgeArray.append(crossEdges)


    delArrayTemp = []
    wholeDelArrayTemp = []
    for gg in selEdgeArray:
        for ce in gg:
            if ce:
                edgeLoop = cmds.polySelect(polyName, edgeLoop=int(ce[0]), ass=0, q=1)
                delArrayTemp.append(edgeLoop)
                for el in edgeLoop:
                    intEl = int(el)
                    if not(intEl in wholeDelArrayTemp):
                        wholeDelArrayTemp.append(intEl)

    return [delArrayTemp,wholeDelArrayTemp]

    #preWholeDelArray = ['%s.e[%s]' % (polyName,str(wda)) for wda in wholeDelArrayTemp]

#print wholeDelArrayTemp

# searching the crease edge in del array.
def filterCrease(polyName,wholeDelArrayTemp,isProtectCreaseLoop = True):
    arrayWithoutCrease = []
    noneCreaseArray = []
    creaseArray = []
    for pwda in wholeDelArrayTemp:
        fullString = '%s.e[%s]' % (polyName,str(pwda))
        cVal = cmds.polyCrease(fullString,q=1,value=1)
        if cVal[0] <= 0:
            noneCreaseArray.append(int(pwda))
        else:
            creaseArray.append(int(pwda))
    #

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


theSel = cmds.ls(sl=1)



polyName = theSel[0]

wholeDelArrayTemp = calculateBaseDeleteArray(polyName)

filterArray = filterCrease(polyName,wholeDelArrayTemp[1])

preWholeDelArray = ['%s.e[%s]' % (polyName, str(fa)) for fa in filterArray]

cmds.polyDelEdge(preWholeDelArray,cv=1)

print 'done'

















