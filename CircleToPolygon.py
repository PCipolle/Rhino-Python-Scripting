import rhinoscriptsyntax as rs
import math

newCurves = rs.GetObjects('select curves')
x = 0
polyLines = []

for curve in newCurves:
    rad = rs.CurveRadius(curve, rs.CurveStartPoint(curve))
    cLength = math.sqrt(((rad*math.cos((math.pi)/4))-rad)**2+(rad*math.cos((math.pi)/4))**2)
    points = rs.CurveEditPoints(curve)
    
    polyLine = rs.AddPolyline(points)
    polyLines.append(polyLine)
    
    
rs.DeleteObjects(newCurves)
rs.AddLoftSrf(polyLines,None, None, loft_type = 2, simplify_method = 0, value=0, closed=False)

