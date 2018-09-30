import rhinoscriptsyntax as rs
import math

solid = rs.GetObjects("Select solid to miter", rs.filter.polysurface, True, True, objects=None, minimum_count=1, maximum_count=-1)
solid2 = rs.GetObjects("Select second solid to miter (if none, press enter)", rs.filter.polysurface, True, True, objects=None, minimum_count=1, maximum_count=-1)
outerFace = rs.GetObject("Select outer surface", rs.filter.surface, False, True, None, True)
miterFace = rs.GetObject("Select second outer surface", rs.filter.surface, False, True, None, True)
 
outerFacePoints = rs.SurfacePoints(outerFace)
miterFacePoints = rs.SurfacePoints(miterFace)

intersectPoints = []

for outerFacePoint in outerFacePoints:
    for miterFacePoint in miterFacePoints:
        if miterFacePoint == outerFacePoint:
            intersectPoints.append(miterFacePoint)

param = rs.SurfaceClosestPoint(outerFace, intersectPoints[0])
normal = rs.SurfaceNormal(outerFace, param)
outerEndPoint = intersectPoints[0] + normal
outerVector = normal

param = rs.SurfaceClosestPoint(miterFace, intersectPoints[0])
normal = rs.SurfaceNormal(miterFace, param)
miterEndPoint = intersectPoints[0] + normal
miterVector = normal

line = rs.AddLine(outerEndPoint, miterEndPoint)
rs.HideObject(line)
midPoint = rs.CurveMidPoint(line)

normalVector = rs.VectorCrossProduct(outerVector, miterVector)

cutPlane = rs.AddCutPlane(solid, intersectPoints[0], midPoint, normal = normalVector)
rs.HideObject(cutPlane)

splitSolids = rs.SplitBrep(solid, cutPlane, True)

rs.CapPlanarHoles(splitSolids[0])
rs.CapPlanarHoles(splitSolids[1])

if  rs.SurfaceArea(splitSolids[0]) > rs.SurfaceArea(splitSolids[1]):
    rs.DeleteObject(splitSolids[1])
else:
    rs.DeleteObject(splitSolids[0]) 

if not solid2:
    x = 0
else: 
    splitSolids = rs.SplitBrep(solid2, cutPlane, True)

    rs.CapPlanarHoles(splitSolids[0])
    rs.CapPlanarHoles(splitSolids[1])
    
    if  rs.SurfaceArea(splitSolids[0]) > rs.SurfaceArea(splitSolids[1]):
        rs.DeleteObject(splitSolids[1])
    else:
        rs.DeleteObject(splitSolids[0]) 

rs.DeleteObject(cutPlane)

rs.DeleteObject(line)