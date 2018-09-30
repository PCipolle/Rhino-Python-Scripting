import rhinoscriptsyntax as rs
import math

yFactor = rs.RealBox("Enter a number for bottom curve", title="Scale Factor 1")
yFactor2 = rs.RealBox("Enter a number for top curve", title="Scale Factor 2")

points = []

for i in range (-50,50):     

    x = i

    y = yFactor*math.cos(i)

    z = 0

    points.append(x)
    points.append(y)
    points.append(z)

cosCurve = rs.AddCurve(points)

points2 = []
for i in range (-50,50):     

    x = i

    y = yFactor2*math.cos(i)

    z = 50

    points2.append(x)
    points2.append(y)
    points2.append(z)

cosCurve2 = rs.AddCurve(points2)

ids = [cosCurve, cosCurve2]
rs.AddLoftSrf(ids)






