import rhinoscriptsyntax as rs
import math

newCurve = rs.GetObject('Select Curve')
rs.RebuildCurve(newCurve, 3, point_count=400)
#rate = 0.01   #Adjust rate
throat = rs.RealBox("Enter Initial Diameter", 1, 'Initial Diameter', minimum = None, maximum = None)  #Adjust initial throat size
initThroat = 0.999
throat = throat/2                                                                                                                       
horn = rs.RealBox("Enter Final Diameter", 10, 'Final Diameter', minimum = None, maximum = None)
curvePoints = rs.CurveEditPoints(newCurve)
#curvePoints = rs.CurveContourPoints(newCurve, rs.CurveStartPoint(newCurve), rs.CurveEndPoint(newCurve))

numPoints = len(curvePoints)
rate = (math.log((horn/2)+initThroat-(throat)))/(numPoints-1)


#cloud = rs.AddPointCloud(curvePoints)
x = 0
offPoints = []
offPoints2 = []
circleProfiles = []

for c in curvePoints:
    param = rs.CurveClosestPoint(newCurve,c)
    tangent = rs.CurveTangent(newCurve,param)
    tempLine = rs.AddLine([0,0,0],tangent)
    rs.MoveObject(tempLine,c)
    dirLine = rs.RotateObject(tempLine,c,90,None,True )
    offCurve = rs.OffsetCurve(tempLine,rs.CurveEndPoint(dirLine),(math.e**(rate * x))- initThroat+throat)
    offPoints.append(rs.CurveStartPoint(offCurve))
    rs.DeleteObject(offCurve)
    rs.DeleteObject(dirLine)
    
    
    dirLine = rs.RotateObject(tempLine,c,-90,None,True )
    offCurve = rs.OffsetCurve(tempLine,rs.CurveEndPoint(dirLine),(math.e**(rate * x))- initThroat+throat)
    offPoints2.append(rs.CurveStartPoint(offCurve))


    plane = rs.PlaneFromPoints(rs.CurveStartPoint(tempLine), rs.CurveStartPoint(offCurve), rs.VectorAdd(rs.CurveStartPoint(tempLine),[0,0,1]))
    radius = rs.Distance(rs.CurveStartPoint(tempLine), rs.CurveStartPoint(offCurve))
    circle = rs.AddCircle(plane,radius)
    rs.DeleteObject(offCurve)
    rs.DeleteObject(dirLine)
    rs.DeleteObject(tempLine)
    circleProfiles.append(circle)
    x = x+1
    
 

polyLines = []

for curve in circleProfiles:
    rad = rs.CurveRadius(curve, rs.CurveStartPoint(curve))
    cLength = math.sqrt(((rad*math.cos((math.pi)/4))-rad)**2+(rad*math.cos((math.pi)/4))**2)
    points = rs.CurveEditPoints(curve)
    
    polyLine = rs.AddPolyline(points)
    polyLines.append(polyLine)
    
    


points1 = []
points2 = []
points3 = []
points4 = []
points5 = []
points6 = []
points7 = []
points8 = []

x = 0
for polyLine in polyLines:
    points = rs.CurvePoints(polyLine)
    points1.append(points[0])
    points2.append(points[1])
    points3.append(points[2])
    points4.append(points[3])
    points5.append(points[4])
    points6.append(points[5])
    points7.append(points[6])
    points8.append(points[7])
    
#rs.AddLoftSrf(polyLines,None, None, loft_type = 2, simplify_method = 0, value=0, closed=False)
line1 = rs.AddCurve(points1)
line2 = rs.AddCurve(points2)
line3 = rs.AddCurve(points3)
line4 = rs.AddCurve(points4)
line5 = rs.AddCurve(points5)
line6 = rs.AddCurve(points6)
line7 = rs.AddCurve(points7)
line8 = rs.AddCurve(points8)

rs.RebuildCurve(line1,degree=3,point_count=250)
rs.RebuildCurve(line2,degree=3,point_count=250)
rs.RebuildCurve(line3,degree=3,point_count=250)
rs.RebuildCurve(line4,degree=3,point_count=250)
rs.RebuildCurve(line5,degree=3,point_count=250)
rs.RebuildCurve(line6,degree=3,point_count=250)
rs.RebuildCurve(line7,degree=3,point_count=250)
rs.RebuildCurve(line8,degree=3,point_count=250)

rs.AddLoftSrf([line1, line2],None, None, loft_type = 2, simplify_method = 0, value=0, closed=False)
rs.AddLoftSrf([line2, line3],None, None, loft_type = 2, simplify_method = 0, value=0, closed=False)
rs.AddLoftSrf([line3, line4],None, None, loft_type = 2, simplify_method = 0, value=0, closed=False)
rs.AddLoftSrf([line4, line5],None, None, loft_type = 2, simplify_method = 0, value=0, closed=False)
rs.AddLoftSrf([line5, line6],None, None, loft_type = 2, simplify_method = 0, value=0, closed=False)
rs.AddLoftSrf([line6, line7],None, None, loft_type = 2, simplify_method = 0, value=0, closed=False)
rs.AddLoftSrf([line7, line8],None, None, loft_type = 2, simplify_method = 0, value=0, closed=False)
rs.AddLoftSrf([line8, line1],None, None, loft_type = 2, simplify_method = 0, value=0, closed=False)


rs.DeleteObjects(circleProfiles)
rs.DeleteObjects(polyLines)
rs.DeleteObject(newCurve)