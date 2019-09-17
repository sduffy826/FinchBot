#import sys
#sys.path.append('../../../FinchPython120')

from finch import Finch 
import time 
from getkey import getkey, keys

class MyRobot:

  def __init__(self, left, right):
    self.leftWheel = left
    self.rightWheel = right
    self.finch = Finch()
 
  def update(self):
    self.finch.wheels(self.leftWheel, self.rightWheel)

  def stop(self):
    self.leftWheel = 0.0
    self.rightWheel = 0.0
    self.update()

  def left(self):
    if self.rightWheel >= 1.0:
      self.leftWheel -= 0.1
    else:
      self.rightWheel += 0.1
    self.update()

  def right(self):
    if self.leftWheel >= 1.0:
      self.rightWheel -= 0.1
    else:
      self.leftWheel += 0.1
    self.update()

  def run(self):
    self.leftWheel = 1.0
    self.rightWheel = 1.0
    self.update()

  def faster(self):
    increment = min(0.1, 1-self.leftWheel, 1-self.rightWheel)
    self.leftWheel += increment
    self.rightWheel += increment
    self.update()

  def shutDown(self):
    self.finch.close()
  
  def status(self):
    # This returns a tuple with the attributes, the wheels, obstacle and lights
    # are tuples (so it's a tuple of tuples (except for temp))
    currStat = ((self.leftWheel, self.rightWheel), self.finch.temperature(), \
                (self.finch.light()), (self.finch.obstacle()), \
                (self.finch.acceleration()))
    return currStat

def input_char(message):
  print(message)
  return getkey()


myRobot = MyRobot(0.0, 0.0)

ans = "l"
while ans <> "q":
  
  ans = input_char("j-left, k-right, i-increase, l-stop, u-topspeed, spacebar-topspeed")
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

myRobot.shutDown()

time.sleep(1)
