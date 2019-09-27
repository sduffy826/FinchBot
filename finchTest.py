import finchClass
import finchConstants
import botUtils
import time 
import datetime
import pythonUtils
import logging 
import sys

from collections import deque

LOGMOVEMENT = False
STEPTHRU = True

currDateTime = datetime.datetime.now().isoformat()
logFile = "finchTest" + currDateTime + ".log"
#logging.basicConfig(filename=logFile, level=logging.INFO)

#logging.basicConfig(stream=sys.stdout, filename=logFile, level=logging.INFO)
logging.basicConfig(filename='fooo.loo', filemode='mw', level=logging.DEBUG)

def outRec(theString):
  logging.debug(theString)
  print(theString)

# ------------------------------------------------------------------------------------------
def wheelSpeedTest():
  startSpeed = 0.0
  while startSpeed <= 1.0:
    outRec("Speed: {0:.2f} Distance/Sec {1:.2f}".format(startSpeed,finchConstants.getDistancePerSecond(startSpeed)))
    startSpeed += 0.1

# ==========================================================================================
request = " "
outRec("\n\nfinchTest.py started at {0}, logfile: {1}".format(currDateTime,logFile))
logging.info("foo")
while request != "q":
  print("1-Show wheel speed")
  request = pythonUtils.input_char("hit key 'q' to quit")
  
  if request == "1":
    wheelSpeedTest()




