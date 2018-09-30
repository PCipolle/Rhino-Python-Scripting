
import rhinoscriptsyntax as rs
import math

solid = rs.GetObjects("Select solid to bullnose", rs.filter.polysurface, True, True, objects=None, minimum_count=1, maximum_count=-1)

face = rs.GetObject("Select surface to bullnose", rs.filter.surface, False, True, None, True)

points = rs.SurfacePoints(face)

if rs.Distance(points[0], points[1]) < rs.Distance(points[1], points[2]):
    distance = rs.Distance(points[0], points[1])
    line = rs.AddLine(points[0], points[1])
    line2 = rs.AddLine(points[2], points[3])
    mid1 = rs.CurveMidPoint(line)
    mid2 = rs.CurveMidPoint(line2)
    path = rs.AddLine(mid1, mid2)
else:
    distance = rs.Distance(points[1], points[2])
    line = rs.AddLine(points[1], points[2])
    line2 = rs.AddLine(points[3], points[0])
    mid1 = rs.CurveMidPoint(line)
    mid2 = rs.CurveMidPoint(line2)
    path = rs.AddLine(mid1, mid2)
    
points = rs.CurveEditPoints(line)
radius = distance/2

rs.DeleteObject(line2)

param = rs.SurfaceClosestPoint(face, points[0])
normal = rs.SurfaceNormal(face, param)
normalVect = distance*rs.VectorReverse(normal)
endPoint = points[0] + normalVect

line2 = rs.AddLine(points[0], endPoint)

param = rs.SurfaceClosestPoint(face, points[1])
normal = rs.SurfaceNormal(face, param)
normalVect = distance*rs.VectorReverse(normal)
endPoint = points[1] + normalVect

line3 = rs.AddLine(points[1], endPoint)


curve1 = rs.AddFilletCurve(line, line2, radius)
curve2 = rs.AddFilletCurve(line, line3, radius)

curve = rs.JoinCurves([curve1,curve2], True)

profile = rs.ExtrudeCurve(curve, path)

splitSolids = rs.SplitBrep(solid, profile)

area1 = rs.SurfaceArea(splitSolids[0])
area2 = rs.SurfaceArea(splitSolids[1])
area3 = rs.SurfaceArea(splitSolids[2])


rs.DeleteObject(solid)

i = 0
swap = True

while swap == True:
    swap = False
    for i in range(0,1):
        if rs.SurfaceArea(splitSolids[i]) > rs.SurfaceArea(splitSolids[i+1]):
            tmp = splitSolids[i+1]
            splitSolids[i+1] = splitSolids[i]
            splitSolids[i] = tmp
            swap = True

rs.JoinSurfaces([splitSolids[2],profile], True)
rs.DeleteObject(splitSolids[0])
rs.DeleteObject(splitSolids[1])

rs.DeleteObject(line)
rs.DeleteObject(line2)
rs.DeleteObject(line3)
rs.DeleteObject(curve)
rs.DeleteObject(path)