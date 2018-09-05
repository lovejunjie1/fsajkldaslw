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

'''
def cleanBorderVert(polyName,vertArray):
    edgeLoop = False
    for i in vertArray:
        vert = '%s.vtx[%s]' % (polyName, str(i))

        edgeInfo = cmds.polyInfo(vert, vertexToEdge=1)
        #print edgeInfo

        edgeID = cleanInfos(edgeInfo[0])
        for eid in edgeID:
            #print eid
            edgeLoop = cmds.polySelect(polyName, edgeBorder=int(eid),ass=0,q=1)
            #print edgeLoop
            if edgeLoop:
                break
        if edgeLoop:
            break
    # searching border edge.when found the first one.enter the clean program.
    if edgeLoop:
        bIDs = []
        for el in edgeLoop:
            edge = '%s.e[%s]' % (polyName, str(el))

            vtx = cmds.polyInfo(edge, edgeToVertex=1)

            vtxID = cleanInfos(vtx[0])

            for v in vtxID:
                if not(v in bIDs):
                    bIDs.append(v)
        # from edge array,dump the unique vertex id to bIDs array

        tempArray = list(vertArray)
        for i in bIDs:
            intVal = int(i)
            if intVal in tempArray:
                #print 'check'
                tempArray.remove(intVal)

        theAns = cleanBorderVert(polyName, tempArray)
        return theAns
        # cause we found a border in edge array.so,we have iterate the program again.
    else:

        return vertArray
'''

theSel = cmds.ls(sl=1)



polyName = theSel[0]

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

#print 'finish'
#print vertArray



#cleanVertArray = cleanBorderVert(polyName,vertArray)

#print cleanVertArray
#selVertByIntArray(polyName,cleanVertArray)

#borderVertArray = list(set(vertArray).difference(set(cleanVertArray)))

#print borderVertArray
#selVertByIntArray(polyName,borderVertArray)

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





holeEdge = []
for i in gg:
    holeEdge += i

#selEdgeByIntArray(polyName,holeEdge)




def preCheck(divAttr,edgeArray):
    troubleCount = 0
    troubleList = []
    for ela in edgeArray:
        if len(ela) < divAttr:
            troubleCount += 1
            troubleList.append(ela)
    if not preCheckAns:
        cmds.warning('this polygon is not a perfact smoothed polygon.do you wanna continue?')

delLevel = 1
# this attr means smooth level 1 to reverse
divAttr = delLevel+1

edgeArray = getBaseStructEdges(polyName)
# every item in the array is unique.it's all fine.

selEdgeArray = []

preCheckAns = True
for ela in edgeArray:
    if len(ela) >= divAttr:

        divWorkArray = [ela[i:i+divAttr] for i in range(0,len(ela),divAttr)]

        # check array struct,is it 100% fit? if more or less.then removed them.
        for dwacheck in divWorkArray:
            if len(dwacheck) != divAttr:
                divWorkArray.remove(dwacheck)

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

            delVertInEdge+= targetArray

        #print delVertInEdge

        #selVertByIntArray(polyName,delVertInEdge)

        #now we need convert the vert to the edge who crossed base struct edges.

        #print holeEdge

        crossEdges = []
        for dvi in delVertInEdge:

            vert = '%s.vtx[%s]' % (polyName, str(dvi))

            edgeInfo = cmds.polyInfo(vert, vertexToEdge=1)

            edgeID = cleanInfos(edgeInfo[0])

            for eid in edgeID:
                if not(int(eid) in holeEdge):
                    crossEdges.append(int(eid))
                    break
                    # if i removed 'break'.then will get two edges.i don't have to do that


        #selEdgeByIntArray(polyName,crossEdges)
        selEdgeArray.append(crossEdges)

print selEdgeArray

for gg in selEdgeArray:
    for ce in gg:
        edgeLoop = cmds.polySelect(polyName, edgeLoop=int(ce), ass=0, q=1)
        selEdgeByIntArray(polyName,edgeLoop,add=1)























