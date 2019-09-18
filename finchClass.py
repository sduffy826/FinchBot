from finch import Finch 
import time 

class MyRobot:
  # Constructor, the polarity is here cause some robots may have the
  # polarity wrong (i.e. right wheel is going in wrong direction)
  # The 'adjust' variables are to adjust for different speeds in the wheels
  # it tries to make them in sync.
  def __init__(self, left, right, lPolarity=1.0, rPolarity=-1.0, lAdjust=0.024, rAdjust=0.0):
    self.leftWheel = left
    self.leftPolarity = lPolarity
    self.leftAdjust = lAdjust

    self.rightWheel = right
    self.rightPolarity = rPolarity
    self.rightAdjust = rAdjust

    self.finch = Finch()

    self.rightMax = 1.0 - lAdjust
    self.leftMax = 1.0 - rAdjust
    self.update()
 
  def update(self):
    if (self.leftWheel != 0.0 or self.rightWheel != 0.0):
      self.finch.wheels((self.leftWheel+self.leftAdjust)*self.leftPolarity, \
                        (self.rightWheel+self.rightAdjust)*self.rightPolarity)
    else:
      self.finch.wheels(0.0,0.0)

  def stop(self):
    self.leftWheel = 0.0
    self.rightWheel = 0.0
    self.update()

  def left(self):
    if self.rightWheel >= self.rightMax:
      self.leftWheel -= 0.1
    else:
      self.rightWheel += 0.1
    self.update()

  def right(self):
    if self.leftWheel >= self.leftMax:
      self.rightWheel -= 0.1
    else:
      self.leftWheel += 0.1
    self.update()

  def run(self):
    self.leftWheel = self.leftMax
    self.rightWheel = self.rightMax
    self.update()

  def faster(self):
    increment = min(0.1, self.leftMax-self.leftWheel, self.rightMax-self.rightWheel)
    self.leftWheel += increment
    self.rightWheel += increment
    self.update()

  def shutDown(self):
    self.finch.close()
  
  def status(self):
    # This returns a tuple with the attributes, the wheels, obstacle and lights
    # are tuples (so it's a tuple of tuples (except for temp))
    currStat = ((self.leftWheel+self.leftAdjust, self.rightWheel+self.rightAdjust), \
                self.finch.temperature(), \
                (self.finch.light()), (self.finch.obstacle()), \
                (self.finch.acceleration()))
    return currStat