import rhinoscriptsyntax as rs
import math

theta = []
points = []
a = rs.RealBox('Enter Initial Radius', 1, 'Radius', minimum = None, maximum = None)
b = rs.RealBox('Enter Growth Rate', 0.2, 'Rate', minimum = None, maximum = None)
maxSteps = rs.RealBox('Enter Number of Points', 10, 'Points', minimum = None, maximum = None)
step = 0
while step < maxSteps:
    theta.append(step)
    step = step +0.1


for t in theta:
    
    r = a*(math.e**(b*t))
    x = r*math.cos(t)
    y = r*math.sin(t)
    point = [x,y,0]
    points.append(point)

#rs.AddPointCloud(points)
rs.AddCurve(points)