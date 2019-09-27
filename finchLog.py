import finchClass
import time 
import datetime
import pythonUtils 

from getkey import getkey, keys

def getLogFile():
  some_datetime_obj = datetime.datetime.now()  # Store current datetime
  datetime_str = some_datetime_obj.isoformat()  # Convert to ISO 8601 string
  return "LogFile." + datetime_str

def input_char(message):
  print(message)
  return getkey()

currentLogFile = getLogFile()
fileHandle     = open(currentLogFile,"at") # Append and text file

outputStr = "Time,Elapsed,L-Wheel,R-Wheel,Temp,L-Light,R-Light,L-Obst,R-Obst,x-Acc,y-Acc,z-Acc,Tap,Shake\n"
fileHandle.write(outputStr)

# Get robot, and have it start moving0
# forward, the last parameter says to run in wheel
# adjustment mode to account for the different speeds of the wheels
myRobot = finchClass.MyRobot(0.7, 0.7, True)
#myFinch = myRobot.myRobot()

ans = "l"
while ans != 'q':
  
  ans = input_char("j-left, k-right, i-increase, l-stop, u-topspeed, spacebar-topspeed")

  print("Response", ans)
  theTime = time.time()
  robotStat = myRobot.status()
  
  outputStr = str(theTime) + "," + \
              str(robotStat[finchClass.STAT_ELAPSED]) + "," + \
              str(robotStat[finchClass.STAT_WHEELS]).strip('()') + "," + \
              str(robotStat[finchClass.STAT_TEMP]) + "," + \
              str(robotStat[finchClass.STAT_LIGHTS]).strip('()') + "," + \
              str(robotStat[finchClass.STAT_OBSTACLE]).strip('()') + "," + \
              str(robotStat[finchClass.STAT_ACCEL]).strip('()')
  fileHandle.write(outputStr)
  fileHandle.write('\n')
       
  print(time.time(), "Elapsed:", robotStat[finchClass.STAT_ELAPSED],
                     "Wheels: ", str(robotStat[finchClass.STAT_WHEELS]), 
                     "Temp: ", robotStat[finchClass.STAT_TEMP], 
                     "lights: ", str(robotStat[finchClass.STAT_LIGHTS]), 
                     "obstacles: ", str(robotStat[finchClass.STAT_OBSTACLE]), 
                     "accelerator:", str(robotStat[finchClass.STAT_ACCEL]))
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

totalElapsedTime = myRobot.getElapsedTime()
myRobot.shutDown()

theLength = "L"
while pythonUtils.isFloat(theLength) == False:
  theLength = input("Enter distance travelled in inches: ")

offCenter = "L"
while pythonUtils.isFloat(offCenter) == False:
  offCenter = input("Distance from center: ")

outputStr = "EOF,TotalLength," + str(theLength) + ",ElapsedTime," + str(totalElapsedTime) + ",OffsetFromAxis," + str(offCenter)
fileHandle.write(outputStr)
fileHandle.close()

time.sleep(0.5)
