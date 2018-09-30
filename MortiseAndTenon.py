import rhinoscriptsyntax as rs
import math

def Main():
    

    rectangle = rs.GetObject("Select rectangle to create mortise and tenon from", rs.filter.curve, True, True)
 
    
    
    if rs.IsCurveClosed(rectangle):
        x = 0
    else:
        print "Failed....Curve must be closed and rectangular"
        return
        
    if rs.IsCurvePlanar(rectangle):
        x = 0
    else:
        print "Failed....Curve must be planar"
        return
        
    lines = rs.ExplodeCurves(rectangle)
    count = 0
    
    for line in lines:
        count = count + 1
    
    if count != 4:
        print "Failed....To many line segments, redraw rectangle"
        return
        
    if rs.IsLine(lines[0]):
        x = 0
    else:
        print "Failed....Curve must be rectangular"
        return
        
    if rs.IsLine(lines[1]):
        x = 0
    else:
        print "Failed....Curve must be rectangular"
        return
        
    if rs.IsLine(lines[2]):
        x = 0
    else:
        print "Failed....Curve must be rectangular"
        return
        
    if rs.IsLine(lines[3]):
        x = 0
    else:
        print "Failed....Curve must be rectangular"
        return
        
    face = rs.GetObject("Select tenon surface", rs.filter.surface, False, True, None, True)
    
    length = rs.GetReal("Enter tenon length", number=None)
    if length and length != 0:
        x = 0
    else:
        print "Failed....No length was entered"
        return
        
    depth = rs.GetReal("Enter mortise depth", number=length+0.05)
    if depth and depth != 0:
        x = 0
    else:
        print "Failed....No depth was entered"
        return
        
    fit = rs.GetReal("Enter mortise fit", number=0.01)
    
    line1 = rs.AddLine(rs.CurveStartPoint(lines[0]),rs.CurveEndPoint(lines[0]))
    line2 = rs.AddLine(rs.CurveStartPoint(lines[1]),rs.CurveEndPoint(lines[1]))
    line3 = rs.AddLine(rs.CurveStartPoint(lines[2]),rs.CurveEndPoint(lines[2]))
    line4 = rs.AddLine(rs.CurveStartPoint(lines[3]),rs.CurveEndPoint(lines[3]))
    
    rs.DeleteObjects(lines)
    lines = line1, line2, line3, line4
    
    if rs.CurveLength(lines[0]) > rs.CurveLength(lines[1]):
        smallside = rs.CurveLength(lines[1])
        longside1 = lines[0]
        longside2 = lines[2]
    else:
        smallside = rs.CurveLength(lines[0])
        longside1 = lines[1]
        longside2 = lines[3]
        
        
    filletRadius = smallside/2
    
    fillet1 = rs.CurveFilletPoints (lines[0], lines[1])
    fillet2 = rs.CurveFilletPoints (lines[1], lines[2])
    fillet3 = rs.CurveFilletPoints (lines[2], lines[3])
    fillet4 = rs.CurveFilletPoints (lines[3], lines[0])
    
    arc1 = rs.AddFilletCurve(lines[0],lines[1], radius = filletRadius) 
    arc2 = rs.AddFilletCurve(lines[1],lines[2], radius = filletRadius) 
    arc3 = rs.AddFilletCurve(lines[2],lines[3], radius = filletRadius) 
    arc4 = rs.AddFilletCurve(lines[3],lines[0], radius = filletRadius)
    arcs = arc1, arc2, arc3, arc4
    
    arcs = rs.JoinCurves(arcs)
    
    arcEnd1 = rs.CurveEndPoint(arcs[0])
    arcStart1 = rs.CurveStartPoint(arcs[0])
    arcEnd2 = rs.CurveEndPoint(arcs[1])
    arcStart2 = rs.CurveStartPoint(arcs[1])
    
    if rs.Distance(arcEnd1, arcEnd2) > rs.Distance(arcEnd1,arcStart2):
        temp = arcEnd2
        arcEnd2 = arcStart2
        arcStart2 = temp
        
    line1 = rs.AddLine(arcEnd1, arcEnd2)
    line2 = rs.AddLine(arcStart1, arcStart2)
        
    curves = line1, arcs[0], arcs[1], line2
    tenonOut = rs.JoinCurves(curves)
    tenonSurf = rs.AddPlanarSrf(tenonOut)
    point = rs.SurfacePoints(face)
    
    param = rs.SurfaceClosestPoint(face, point[0])
    normal = rs.SurfaceNormal(face, param)
    normal = normal * length
    vect = rs.AddLine( arcEnd1, arcEnd1 + normal )
    
    tenon = rs.ExtrudeSurface(tenonSurf, vect, cap=True)
    
    rs.DeleteObjects(curves)
    arcs = arc1, arc2, arc3, arc4
    rs.DeleteObjects(arcs)
    rs.DeleteObject(rectangle)
    
    
    rs.ExtendCurveLength(longside1, 0, 0, fit)
    rs.ExtendCurveLength(longside1, 0, 1, fit)
    rs.ExtendCurveLength(longside2, 0, 0, fit)
    rs.ExtendCurveLength(longside2, 0, 1, fit)
    
    if rs.Distance(rs.CurveEndPoint(longside1), rs.CurveEndPoint(longside2)) < rs.Distance(rs.CurveStartPoint(longside1), rs.CurveEndPoint(longside2)):
        line1Start = rs.CurveEndPoint(longside1)
        line1End = rs.CurveEndPoint(longside2)
        line2Start = rs.CurveStartPoint(longside1)
        line2End = rs.CurveStartPoint(longside2)
    else:
        line1Start = rs.CurveStartPoint(longside1)
        line1End = rs.CurveEndPoint(longside2)
        line2Start = rs.CurveEndPoint(longside1)
        line2End = rs.CurveStartPoint(longside2) 
        
    shortside1 = rs.AddLine(line1Start, line1End)
    shortside2 = rs.AddLine(line2Start, line2End)
    
    arc1 = rs.AddFilletCurve(longside1, shortside1, radius = filletRadius)
    arc2 = rs.AddFilletCurve(shortside1, longside2, radius = filletRadius)
    arc3 = rs.AddFilletCurve(longside2, shortside2, radius = filletRadius)
    arc4 = rs.AddFilletCurve(shortside2, longside1, radius = filletRadius)
    arcs = arc1, arc2, arc3, arc4
    
    arcs = rs.JoinCurves(arcs)
    
    arcEnd1 = rs.CurveEndPoint(arcs[0])
    arcStart1 = rs.CurveStartPoint(arcs[0])
    arcEnd2 = rs.CurveEndPoint(arcs[1])
    arcStart2 = rs.CurveStartPoint(arcs[1])
    
    if rs.Distance(arcEnd1, arcEnd2) > rs.Distance(arcEnd1,arcStart2):
        temp = arcEnd2
        arcEnd2 = arcStart2
        arcStart2 = temp
        
    line1 = rs.AddLine(arcEnd1, arcEnd2)
    line2 = rs.AddLine(arcStart1, arcStart2)
    
    curves = line1, arcs[0], arcs[1], line2
    mortiseOut = rs.JoinCurves(curves)
    mortiseSurf = rs.AddPlanarSrf(mortiseOut)
    
    param = rs.SurfaceClosestPoint(face, point[0])
    normal = rs.SurfaceNormal(face, param)
    normal = normal * depth
    vect = rs.AddLine( arcEnd1, arcEnd1 + normal )
    
    mortise = rs.ExtrudeSurface(mortiseSurf, vect, cap=True)   
    
    rs.DeleteObject(shortside1)
    rs.DeleteObject(shortside2)
    rs.DeleteObject(mortiseOut)
    rs.DeleteObject(mortiseSurf)
    rs.DeleteObjects(curves)
    rs.DeleteObjects(lines)
    arcs = arc1, arc2, arc3, arc4
    rs.DeleteObjects(arcs)
    rs.DeleteObject(rectangle)
    rs.DeleteObject(tenonOut)
    rs.DeleteObject(tenonSurf)

    return

Main()


