from finch import Finch 
import time 
import finchConstants

class MyRobot:
  
  # Constructor, the polarity is here cause some robots may have the
  # polarity wrong (i.e. right wheel is going in wrong direction)
  # The 'adjust' variables are to adjust for different speeds in the wheels
  # it tries to make them in sync.
  def __init__(self, left, right):
    self.debugIt = True

    self.leftWheel  = left
    self.rightWheel = right
  
    self.finch = Finch()

    # If true then wheel speed will be adjusted by the constants
    self.updateMode = False
    self.update(self.updateMode)
 
  def wheelHelper(self, whichWheel):
    if whichWheel=="R":
      if self.updateMode:
        return (self.rightWheel+finchConstants.RIGHTWHEELADJUSTMENT)*finchConstants.RIGHTPOLARITY
      else:
        return self.rightWheel*finchConstants.RIGHTPOLARITY
    else:
      if self.updateMode:
        return (self.leftWheel+finchConstants.LEFTWHEELADJUSTMENT)*finchConstants.LEFTPOLARITY
      else:
        return self.leftWheel*finchConstants.LEFTPOLARITY

  def update(self, useAdjustment):
    self.updateMode = useAdjustment
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
    self.update(self.updateMode)

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
    self.update(self.updateMode)

  def rightTurn(self, degrees2Turn):
    self.turnTime = degrees2Turn/360.0
    self.leftWheel  = finchConstants.RIGHTROTATIONSPEED
    self.rightWheel = finchConstants.RIGHTROTATIONSPEED*-1
    self.update(False)
    time.sleep(finchConstants.RIGHTROTATIONTIME*self.turnTime)
    self.leftWheel = 0
    self.rightWheel = 0
    self.update(False)
    
  def run(self):
    self.leftWheel = finchConstants.LEFTMAXSPEED
    self.rightWheel = finchConstants.RIGHTMAXSPEED
    self.update(self.updateMode)

  def faster(self):
    increment = min(finchConstants.SPEEDINCREMENT, finchConstants.LEFTMAXSPEED-self.leftWheel, finchConstants.RIGHTMAXSPEED-self.rightWheel)
    self.leftWheel += increment
    self.rightWheel += increment
    self.update(self.updateMode)

  def shutDown(self):
    self.finch.close()
  
  def status(self):
    # This returns a tuple with the attributes, the wheels, obstacle and lights
    # are tuples (so it's a tuple of tuples (except for temp))
    currStat = ((self.leftWheel+finchConstants.LEFTWHEELADJUSTMENT, self.rightWheel+finchConstants.RIGHTWHEELADJUSTMENT), \
                self.finch.temperature(), \
                (self.finch.light()), (self.finch.obstacle()), \
                (self.finch.acceleration()))
    return currStat