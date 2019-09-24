from finch import Finch 
import time 
import finchConstants

STAT_ELAPSED = 0
STAT_WHEELS = 1
STAT_TEMP = 2
STAT_LIGHTS = 3
STAT_OBSTACLE = 4
STAT_ACCEL = 5

class MyRobot:
  
  # Constructor, the polarity is here cause some robots may have the
  # polarity wrong (i.e. right wheel is going in wrong direction)
  # The 'adjust' variables are to adjust for different speeds in the wheels
  # it tries to make them in sync.
  def __init__(self, left, right, inAdjustmentMode=False):
    self.debugIt = True

    self.leftWheel  = left
    self.rightWheel = right
  
    self.finch = Finch()

    # If true then wheel speed will be adjusted by the constants
    self.inWheelAdjustmentMode = inAdjustmentMode
    self.lasttime = time.time()
    self.update(self.inWheelAdjustmentMode)
 
  def wheelHelper(self, whichWheel, logModeOnly=False):
    # For logging we don't want to show the polarity adjustment... could be
    # confusing to people analyzing wheel motion :)
    if logModeOnly==False:
      rtPol = finchConstants.RIGHTPOLARITY
      ltPol = finchConstants.LEFTPOLARITY
    else:
      rtPol = 1.0
      ltPol = 1.0
    if whichWheel=="R":
      if self.inWheelAdjustmentMode:
        return (self.rightWheel+finchConstants.RIGHTWHEELADJUSTMENT)*rtPol
      else:
        return self.rightWheel*rtPol
    else:
      if self.inWheelAdjustmentMode:
        return (self.leftWheel+finchConstants.LEFTWHEELADJUSTMENT)*ltPol
      else:
        return self.leftWheel*ltPol

  def update(self, useAdjustment):
    self.inWheelAdjustmentMode = useAdjustment
    if self.debugIt==True:
      print("left: {0:.2f} right: {1:.2f}".format(self.wheelHelper("L"), self.wheelHelper("R") ))

    if (self.leftWheel != 0.0 or self.rightWheel != 0.0):
      self.finch.wheels(self.wheelHelper("L"), self.wheelHelper("R"))
    else:
      self.finch.wheels(0.0,0.0)

  def stop(self):
    self.leftWheel = 0.0
    self.rightWheel = 0.0
    self.update(False)

  def left(self):
    if self.rightWheel >= finchConstants.RIGHTMAXSPEED:
      self.leftWheel -= finchConstants.SPEEDINCREMENT
    else:
      self.rightWheel += finchConstants.SPEEDINCREMENT
    self.update(self.inWheelAdjustmentMode)

  def leftTurn(self,degrees2Turn):
    self.turnTime = degrees2Turn/360.0
    self.leftWheel = finchConstants.LEFTROTATIONSPEED*-1
    self.rightWheel = finchConstants.LEFTROTATIONSPEED
    self.update(False)
    time.sleep(finchConstants.LEFTROTATIONTIME*self.turnTime)
    self.leftWheel = 0
    self.rightWheel = 0
    self.update(False)
    
  def right(self):
    if self.leftWheel >= finchConstants.LEFTMAXSPEED:
      self.rightWheel -= finchConstants.SPEEDINCREMENT
    else:
      self.leftWheel += finchConstants.SPEEDINCREMENT
    self.update(self.inWheelAdjustmentMode)

  def rightTurn(self, degrees2Turn):
    self.turnTime = degrees2Turn/360.0
    self.leftWheel  = finchConstants.RIGHTROTATIONSPEED
    self.rightWheel = finchConstants.RIGHTROTATIONSPEED*-1
    self.update(False)
    time.sleep(finchConstants.RIGHTROTATIONTIME*self.turnTime)
    self.leftWheel = 0
    self.rightWheel = 0
    self.update(False)
    
  def getElapsedTime(self):
    return round(time.time() - self.lasttime,4)

  def resetTimer(self):
    self.lasttime = time.time()

  def run(self):
    self.leftWheel = finchConstants.LEFTMAXSPEED
    self.rightWheel = finchConstants.RIGHTMAXSPEED
    self.update(self.inWheelAdjustmentMode)

  def faster(self):
    increment = min(finchConstants.SPEEDINCREMENT, finchConstants.LEFTMAXSPEED-self.leftWheel, finchConstants.RIGHTMAXSPEED-self.rightWheel)
    self.leftWheel += increment
    self.rightWheel += increment
    self.update(self.inWheelAdjustmentMode)

  def shutDown(self):
    self.finch.close()
  
  def status(self):
    # This returns elapsed time since clock was set and a tuple with the attributes, the wheels, obstacle and lights
    # are tuples (so it's a tuple of tuples (except for temp))
    currStat = (self.getElapsedTime(),
                (self.wheelHelper("L",True), self.wheelHelper("R",True)),  
                self.finch.temperature(),
                (self.finch.light()), (self.finch.obstacle()),
                (self.finch.acceleration()))
    
    return currStat
    # comment below was up above
    #            (self.leftWheel+finchConstants.LEFTWHEELADJUSTMENT, self.rightWheel+finchConstants.RIGHTWHEELADJUSTMENT), \