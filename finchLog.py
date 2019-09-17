#import sys
#sys.path.append('../../../FinchPython120')
import finchClass
import time 
import datetime

from getkey import getkey, keys

def getLogFile():
  some_datetime_obj = datetime.datetime.now()  # Store current datetime
  datetime_str = some_datetime_obj.isoformat()  # Convert to ISO 8601 string
  return "LogFile." + datetime_str


def input_char(message):
  print(message)
  return getkey()

myRobot = finchClass.MyRobot(0.0, 0.0)

currentLogFile = getLogFile()
fileHandle     = open(currentLogFile,"at") # Append and text file
  
ans = "l"
while ans != 'q':
  
  ans = input_char("j-left, k-right, i-increase, l-stop, u-topspeed, spacebar-topspeed")

  print("Response", ans)
  theTime = time.time()
  robotStat = myRobot.status()

  # Output data
  outputStr = (theTime, robotStat)
  fileHandle.write(str(outputStr))
  fileHandle.write('\n')
       
  print(time.time(), "Wheels: ", str(robotStat[0]), 
                     "Temp: ", robotStat[1], 
                     "lights: ", str(robotStat[2]), 
                     "obstacles: ", str(robotStat[3]), 
                     "accelerator:", str(robotStat[4]))

  if ans is "j":
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

theLength = input("Enter distance travelled in inches")
offCenter = input("Enter distance from center")
outputStr = ("EOF",theLength,offCenter)
fileHandle.write(str(outputStr))
fileHandle.close()

time.sleep(0.5)
