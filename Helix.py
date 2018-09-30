import rhinoscriptsyntax as rs
import math
points = []
for i in range (-50,50):     

    x = math.sin(i)

    y = math.cos(i)

    z = i/10

    points.append(x)
    points.append(y)
    points.append(z)

rs.AddCurve(points)




