import finchClass
import time 
import datetime
import pythonUtils 
import finchConstants

import logging

logging.basicConfig(filename='finchRobot.log', level=logging.DEBUG)
 
# Get robot, and have it start moving0
# forward, the last parameter says to run in wheel
# adjustment mode to account for the different speeds of the wheels
myRobot = finchClass.MyRobot(0.0, 0.0, True)

ans = "l"

# ------------------------------------------------------------------------
def obsTest(testTime):
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
      logging.debug("Left obstacle state changed: {0} at: {1}".format(currLeftObstacle,myRobot.getElapsedTime()))
    if currRightObstacle != rightObstacle:
      logging.debug("Right obstacle state changed:{0} at: {1}".format(currRightObstacle,myRobot.getElapsedTime()))
  myRobot.stop()

# ------------------------------------------------------------------------
def obstacleAvoidMovement(direction=finchConstants.LEFT):
  movementsToMake = myRobot.getOutOfObstacle(direction)
  logging.debug("obstacleAvoidMovement, directionToMove: {0}".format(direction))
  index = 0
  for aMovement in movementsToMake:
    index += 1
    logging.debug("  movement: {0} is: {1}".format(index,convertTupleToString(aMovement)))


def spinLeft():
  myRobot.setWheels(-2.5,5.0,False)
  time.sleep(2)
  myRobot.stop()   
  time.sleep(.5)
  myRobot.setWheels(5.0,-2.5,False)
  time.sleep(2.5)
  myRobot.stop()   


def rotate(direction, degrees):
  if direction == finchConstants.LEFT:
    myRobot.leftTurn(degrees)      
  else:
    myRobot.rightTurn(degrees)

def convertTupleToString(tupleVar):
  return pythonUtils.convertTupleToString(tupleVar)

def roboStat():
  robotStat = myRobot.status()
 
  # Just here for debugging format of the return argument
  index = 0
  for aVar in robotStat:    
    logging.debug("robotStat[{0}] is type: {1}".format(index,str(type(aVar))))
    index += 1

  logging.info(str(time.time()) + " Elapsed:" + str(robotStat[finchClass.STAT_ELAPSED]) +
                                  " Wheels: " + convertTupleToString(robotStat[finchClass.STAT_WHEELS]) + 
                                  " Temp: " + str(robotStat[finchClass.STAT_TEMP]) +
                                  " lights: " + convertTupleToString(robotStat[finchClass.STAT_LIGHTS]) +
                                  " obstacles: " + convertTupleToString(robotStat[finchClass.STAT_OBSTACLE]) + 
                                  " accelerator: " + convertTupleToString(robotStat[finchClass.STAT_ACCEL]))

def goAFoot(wheelSpeed2Use=0.4):
  distancePerSecond = finchConstants.getDistancePerSecond(wheelSpeed2Use)
  # Reset the timer, we need to keep track of how long we're traveling
  time2Target = (12.0/distancePerSecond)

  logging.debug("goAFoot: distancePerSecond:{0:.2f} time2Target{1:.2f} wheelSpeed2Use:{2:.2f}".format(distancePerSecond,time2Target,wheelSpeed2Use))

  myRobot.resetTimer()
  myRobot.resetState()
  # Start moving forward at the requested speed, we'll continue moving
  # till we reach our destination or we can't move any longer
  myRobot.setWheels(wheelSpeed2Use,wheelSpeed2Use,True)
  while True:
    timeMoving   = myRobot.getElapsedTime()
    robotCanMove = myRobot.canMove()
    logging.debug("goAFoot: Looping, timeMoving:{0} robotCanMove:{1}".format(timeMoving,robotCanMove))
    if timeMoving >= time2Target or robotCanMove == False:
      break
  myRobot.stop()

def setColor(whichColor):
  if whichColor%3 == 0:
    myRobot.setLedColor(finchConstants.RED)
  elif whichColor%3 == 1:
    myRobot.setLedColor(finchConstants.GREEN)
  else:
    myRobot.setLedColor(finchConstants.BLUE)


# ------------------------------------------------------------------------
theColor = -1
lastDirection = finchConstants.RIGHT
while ans != 'q':
  ans = pythonUtils.input_char("o-obstacle, a-obstacleAvoid, s-stat, l-rotateLeft, r-rotateRight, p-spin, f-12Inches, c-color")
  if ans == "q":
    break

  if ans == "o":
    obsTest(5)
  elif ans == "a":
    if lastDirection == finchConstants.LEFT:
      lastDirection = finchConstants.RIGHT
    else:
      lastDirection = finchConstants.LEFT
    obstacleAvoidMovement(lastDirection)
  elif ans == "s":
    roboStat()
  elif ans is "j":
    myRobot.left()
  elif ans is "k":
    myRobot.right()
  elif ans is "i":         
    myRobot.faster()
  elif ans is "l":
    rotate(finchConstants.LEFT, 360)
    # myRobot.stop()
  elif ans is "r":
    rotate(finchConstants.RIGHT, 360)
  elif ans is "p":
    spinLeft()
  elif ans is "f":
    goAFoot()
  elif ans is "c":
    theColor += 1
    setColor(theColor)
  elif ans is "u":
    myRobot.run()

myRobot.shutDown()