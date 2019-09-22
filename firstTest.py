#import sys
#sys.path.append('../../../FinchPython120')

from finch import Finch 
import finchClass
import time 
from getkey import getkey, keys

def input_char(message):
  print(message)
  return getkey()

myRobot = finchClass.MyRobot(0.0, 0.0)

ans = "l"
while ans != 'q':
  
  ans = input_char("j-left, k-right, i-increase, l-stop, u-topspeed, spacebar-topspeed, a-left90, s-right90")
  #time.sleep(1)
  print("Response", ans)
  theTime = time.time()
  robotStat = myRobot.status()

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
  elif ans is "a":
    myRobot.leftTurn(90)
  elif ans is "s":
    myRobot.rightTurn(90)

myRobot.shutDown()

time.sleep(1)
