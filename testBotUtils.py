import botUtils
import time 

listOfAnglesToTest = []
listOfAnglesToTest.append((90,75))
listOfAnglesToTest.append((10,350))
listOfAnglesToTest.append((180,359))

for theAngles in listOfAnglesToTest:
  startAngle = theAngles[0]
  endAngle = theAngles[1]
  angleChange = botUtils.getMinDegrees(startAngle,endAngle)
  checkEndAngle = botUtils.getNewOrientation(startAngle,angleChange)
  print("From: {0} to: {1} turn {2} you'll arrive at: {3}".format(startAngle,endAngle,angleChange,checkEndAngle))