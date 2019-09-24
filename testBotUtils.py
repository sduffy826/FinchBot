import botUtils
import time 

# Test logif for turning angles.
def testTurningAngles():
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
  
  testAngleAndDistance2GetThere()  

# Test calculating the angle between two points, and distance between them
def testAngleAndDistance2GetThere():
  testList = []
  #testList.append((4,2,90))
  testList.append((0,0,0))

  targetList = []
  targetList.append((72,6))
  #targetList.append((3,1))
  #targetList.append((0,0))
  #targetList.append((-2,-1))
  #targetList.append((-4,-2))
  #targetList.append((2,-2))    

  for strt in testList:
    for aTarget in targetList:
      x = aTarget[0]
      y = aTarget[1]
      theAngle = botUtils.calculateAngleToTarget(strt,x,y)
      distance = botUtils.calculateDistanceBetweenPoints(strt,aTarget)
      print("From: {0} to: ({1},{2}) is: {3} angle, distance: {4}".format(str(strt),x,y,theAngle,distance))

#testAngleAndDistance2GetThere()
testTurningAngles()