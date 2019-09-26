import finchClass
import time 
import datetime
import pythonUtils 
import finchConstants

# Get robot, and have it start moving0
# forward, the last parameter says to run in wheel
# adjustment mode to account for the different speeds of the wheels
myRobot = finchClass.MyRobot(0.4, 0.4, True)

testTime = 15.0
ans = "l"

# ------------------------------------------------------------------------
def obsTest():
  myRobot.stop()
  myRobot.resetTimer()
  myRobot.setWheels(0.4,0.4,True)
  leftObstacle = myRobot.hasObstacle(finchConstants.LEFT)
  rightObstacle = myRobot.hasObstacle(finchConstants.RIGHT)
  while myRobot.getElapsedTime() < testTime:
    myRobot.updateMyState()
    currLeftObstacle = myRobot.hasObstacle(finchConstants.LEFT)
    currRightObstacle = myRobot.hasObstacle(finchConstants.RIGHT)
    if currLeftObstacle != leftObstacle:
      print("Left obstacle state changed:{0} at{1}".format(currLeftObstacle,myRobot.getElapsedTime()))
    if currRightObstacle != rightObstacle:
      print("Right obstacle state changed:{0} at{1}".format(currRightObstacle,myRobot.getElapsedTime()))

def roboStat():
  robotStat = myRobot.status()
  print(time.time(), "Elapsed:", robotStat[finchClass.STAT_ELAPSED],
                      "Wheels: ", str(robotStat[finchClass.STAT_WHEELS]), 
                      "Temp: ", robotStat[finchClass.STAT_TEMP], 
                      "lights: ", str(robotStat[finchClass.STAT_LIGHTS]), 
                      "obstacles: ", str(robotStat[finchClass.STAT_OBSTACLE]), 
                      "accelerator:", str(robotStat[finchClass.STAT_ACCEL]))


# ------------------------------------------------------------------------
while ans != 'q':
  ans = pythonUtils.input_char("o-obstacle, s-stat")
  if ans == "q":
    break

  if ans == "o":
    obsTest()
  elif ans == "s":
    roboStat()
  elif ans is "j":
    myRobot.left()
  elif ans is "k":
    myRobot.right()
  elif ans is "i":         
    myRobot.faster()
  elif ans is "l":
    myRobot.stop()
  elif ans is "u":
    myRobot.run()

myRobot.shutDown()