import finchClass
import finchConstants
import botUtils
import time 
import datetime
import pythonUtils
import logging 
import sys

from collections import deque

# Get logger, for console want info messages. for file we want debug info
testLogger = pythonUtils.getCustomLogger("finchTest",logging.INFO,logging.DEBUG,True)

LOGMOVEMENT = False
STEPTHRU = True

currDateTime = datetime.datetime.now().isoformat()

# --------------------------------------------------
myRobot = finchClass.MyRobot(0.0, 0.0, True)

# ------------------------------------------------------------------------------------------
def wheelSpeedTest():
  startSpeed = 0.0
  while startSpeed <= 1.0:
    testLogger.info("Speed: {0:.2f} Distance/Sec {1:.2f}".format(startSpeed,finchConstants.getDistancePerSecond(startSpeed)))
    startSpeed += 0.1

# ----------------
def callEdgeCheck(robotPosition, regionOfTravel, threshold=finchClass.THRESHOLDTOSIDE):
  print("foo")
  theClosestEdges = myRobot.getRobotClosestEdges(robotPosition, regionOfTravel, threshold)
  testLogger.info("Closest edge test, pos: {0}, reg: {1}, edges:{2}".format(str(robotPosition),str(regionOfTravel),str(theClosestEdges)))

def edgeTest():
  robotPosition = (0.0,17.0,0.0)
  robotRegion = (0.0, -6.0, 96, 18)
  callEdgeCheck(robotPosition,robotRegion)
  myRobot.checkAndSetObstacleDirectionToTry(robotPosition, robotRegion)


# ==========================================================================================
request = " "
testLogger.info("\n\nfinchTest.py started at {0}".format(currDateTime))

while request != "q":
  print("1-ShowWheelSpeed, 2-EdgeTest")
  request = pythonUtils.input_char("hit key 'q' to quit")
  
  if request == "1":
    wheelSpeedTest()
  elif request == "2":
    edgeTest()
