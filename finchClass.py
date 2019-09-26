from finch import Finch 
import time 
import finchConstants
import botUtils
import logging

logging.basicConfig(filename='finchRobot.log', level=logging.DEBUG)

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
    self.leftWheel  = left
    self.rightWheel = right
    self.myBot = Finch()

    # Keep track of the direction you should try on obstacles
    self.obstacleDirectionToTry = finchConstants.LEFT
    self.lastScrapedSide = " "
    # Keep track of when the last time you moved forward, we use that
    # to identify sensors
    self.lastTimeIMovedForward = -1
    self.obstacleState = { 
      "left" : False,
      "leftStateTime" : 0.0,
      "leftElapsedTime" : 0.0,
      "right" : False,
      "rightStateTime" : 0.0,
      "rightElapsedTime" : 0.0
    }

     # If true then wheel speed will be adjusted by the constants
    self.inWheelAdjustmentMode = inAdjustmentMode
    self.lasttime = time.time()
    self.update(self.inWheelAdjustmentMode)

 
  # Reset the state of the sensors
  def resetState(self):
    self.obstacleState["left"] = False
    self.obstacleState["leftStateTime"] = 0.0
    self.obstacleState["leftElapsedTime"] = 0.0
    self.obstacleState["right"] = False
    self.obstacleState["rightStateTime"] = 0.0
    self.obstacleState["rightElapsedTime"] = 0.0

  # This is common routine to update the dictionary 'state' items associated
  # with the sensors... we need this because we need the state to persist for
  # a given amount of time before we think of it as 'real' (the bot sensors are flakey)
  # NOTE: The state will only be updated when wheels are moving, or you pass in the 
  # forceUpdate indicator
  def updateMyState(self, forceUpdate=False):
    if self.leftWheel != 0.0 or self.rightWheel != 0.0 or forceUpdate:
      stateTime = time.time()
      leftObst, rightObst  = self.myBot.obstacle()
      
      if self.obstacleState["left"] != leftObst or self.obstacleState["leftStateTime"] == 0.0:
        self.obstacleState["left"] = leftObst
        self.obstacleState["leftStateTime"] = stateTime
        self.obstacleState["leftElapsedTime"] = 0.0
      else:
        self.obstacleState["leftElapsedTime"] = round(stateTime - self.obstacleState["leftStateTime"],4)

      if self.obstacleState["right"] != rightObst or self.obstacleState["rightStateTime"] == 0.0:
        self.obstacleState["right"] = rightObst
        self.obstacleState["rightStateTime"] = stateTime
        self.obstacleState["rightElapsedTime"] = 0.0
      else:
        self.obstacleState["rightElapsedTime"] = round(stateTime - self.obstacleState["rightStateTime"],4)
  
  # Helper to return indicator if an obstacle exists, we did this because we need the obstacle to
  # persist for an amount of time (thresholdInSecs) before we say it's on
  def hasObstacle(self,whichOne,thresholdInSecs=0.2):
    logging.debug("finchClass-hasObstacle, obstacleState:{0}".format(str(self.obstacleState)))

    leftObst = False
    if self.obstacleState["leftElapsedTime"] > thresholdInSecs:
      leftObst = self.obstacleState["left"]
    rightObst = False
    if self.obstacleState["rightElapsedTime"] > thresholdInSecs:
      rightObst = self.obstacleState["right"]

    logging.debug("finchClass-hasObstacle, leftObst:{0} rightObst{1}".format(leftObst,rightObst))

    if whichOne == finchConstants.LEFT:
      return leftObst
    elif whichOne == finchConstants.RIGHT:
      return rightObst
    elif leftObst == True or rightObst == True:
      return True
    else:
      return False

  def wheelHelper(self, whichWheel, logModeOnly=False):
    # For logging we don't want to show the polarity adjustment... could be
    # confusing to people analyzing wheel motion :)
    if logModeOnly == False:
      rtPol = finchConstants.RIGHTPOLARITY
      ltPol = finchConstants.LEFTPOLARITY
    else:
      rtPol = 1.0
      ltPol = 1.0

    if whichWheel == "R":
      if self.inWheelAdjustmentMode:
        return (self.rightWheel+finchConstants.RIGHTWHEELADJUSTMENT)*rtPol
      else:
        return self.rightWheel*rtPol
    else:
      if self.inWheelAdjustmentMode:
        return (self.leftWheel+finchConstants.LEFTWHEELADJUSTMENT)*ltPol
      else:
        return self.leftWheel*ltPol

  # Set the wheel speed (to move, unless both are zero)
  def update(self, useAdjustment):
    self.inWheelAdjustmentMode = useAdjustment
    logging.debug("finchClass-update, left: {0:.2f} right: {1:.2f}".format(self.wheelHelper("L"), self.wheelHelper("R")))

    if (self.leftWheel != 0.0 or self.rightWheel != 0.0):
      # Setting wheel speed, reset the sensors
      self.resetState()
      self.myBot.wheels(self.wheelHelper("L"), self.wheelHelper("R"))
    else:
      self.myBot.wheels(0.0,0.0)
  
  # Stop moving
  def stop(self):
    self.leftWheel = 0.0
    self.rightWheel = 0.0
    self.update(False)

  # Turn left, we do this by either increasing the speed of the right wheel
  # or decreasing the left wheel speed if we're already at max speed
  def left(self):
    if self.rightWheel >= finchConstants.RIGHTMAXSPEED:
      self.leftWheel -= finchConstants.SPEEDINCREMENT
    else:
      self.rightWheel += finchConstants.SPEEDINCREMENT
    self.update(self.inWheelAdjustmentMode)

  # Turn left for the desired degrees
  def leftTurn(self,degrees2Turn):
    self.turnTime = degrees2Turn/360.0
    self.leftWheel = finchConstants.LEFTROTATIONSPEED*-1
    self.rightWheel = finchConstants.LEFTROTATIONSPEED
    self.update(False)
    time.sleep(finchConstants.LEFTROTATIONTIME*self.turnTime)
    self.leftWheel = 0
    self.rightWheel = 0
    self.update(False)
    
  # Turn right, basically increase the speed of the left wheel
  # or decreasing right wheel if left wheel already at max speed
  def right(self):
    if self.leftWheel >= finchConstants.LEFTMAXSPEED:
      self.rightWheel -= finchConstants.SPEEDINCREMENT
    else:
      self.leftWheel += finchConstants.SPEEDINCREMENT
    self.update(self.inWheelAdjustmentMode)

  # Turn right the specified number of degrees
  def rightTurn(self, degrees2Turn):
    self.turnTime = degrees2Turn/360.0
    self.leftWheel  = finchConstants.RIGHTROTATIONSPEED
    self.rightWheel = finchConstants.RIGHTROTATIONSPEED*-1
    self.update(False)
    time.sleep(finchConstants.RIGHTROTATIONTIME*self.turnTime)
    self.leftWheel = 0
    self.rightWheel = 0
    self.update(False)
    
  # Get the elapsed time
  def getElapsedTime(self):
    return round(time.time() - self.lasttime,4)

  # Reset the elapsed timer
  def resetTimer(self):
    self.lasttime = time.time()

  # Run... set wheels to max speed
  def run(self):
    self.leftWheel = finchConstants.LEFTMAXSPEED
    self.rightWheel = finchConstants.RIGHTMAXSPEED
    self.update(self.inWheelAdjustmentMode)

  # Go faster, we determine the speed increment and increase both wheels by that amount
  def faster(self):
    increment = min(finchConstants.SPEEDINCREMENT, finchConstants.LEFTMAXSPEED-self.leftWheel, finchConstants.RIGHTMAXSPEED-self.rightWheel)
    self.leftWheel += increment
    self.rightWheel += increment
    self.update(self.inWheelAdjustmentMode)

  # Set wheels to be at certain speed
  def setWheels(self, lftWheel, rtWheel, adJustMode):
    self.leftWheel = lftWheel
    self.rightWheel = rtWheel
    self.inWheelAdjustmentMode = adJustMode
    self.update(self.inWheelAdjustmentMode)

  # Shutdown the robot
  def shutDown(self):
    self.myBot.close()
  
  # Return True if robot can move, false if there is some type of
  # obstacle
  def canMove(self):
    # Add logic for other sensors
    self.updateMyState()
    return (self.hasObstacle("BOTH") == False)

  # Routine when robot feels a scrap (obstacle on one side of it), pass in the side
  def getOutOfScrape(self, sideOfScrape):
    # Motion is rotate SCRAPEANGLE (if left +, right -)
    # Backup SCRAPEBACKUPDISTANCE
    # Rotate back to original angle
    if sideOfScrape == finchConstants.LEFT:
      return botUtils.calculateScrapeMovement(finchConstants.SCRAPEANGLE, finchConstants.SCRAPEBACKUPDISTANCE)
    else:
      return botUtils.calculateScrapeMovement(-finchConstants.SCRAPEANGLE, finchConstants.SCRAPEBACKUPDISTANCE)

  # Get out of obstacle is similar to the get out of scrap but we use a 45 degree angle and the distance to
  # move puts us back 1/2 of the robot's width away
  def getOutOfObstacle(self, directionToMove):
    # We want to try a position to the left or right that is 1/2 our width away
    # Calculate the distance we need to backup first, it's 1/2 width divided by sin(45)
    distanceToBackup = (finchConstants.TOTALWIDTH / 2) / botUtils.degreesSin(45)
    if directionToMove == finchConstants.LEFT:
      # Want angle of -45 to turn right then backup
      return botUtils.calculateScrapeMovement(-45.0, distanceToBackup)
    else:
      return botUtils.calculateScrapeMovement(45, distanceToBackup)
      
  # Return the direction to try when you hit an obstacle, put logic in here
  def getObstacleDirectionToTry(self):
    return self.obstacleDirectionToTry

  def flipObstacleDirectionToTry(self):
    if self.obstacleDirectionToTry == finchConstants.LEFT:
      self.obstacleDirectionToTry = finchConstants.RIGHT 
    else:
      self.obstacleDirectionToTry = finchConstants.LEFT

  # Return the side that was last scraped, put more in here
  def getLastScrapeSide(self):
    return self.lastScrapedSide

  def isObstacle(self, robotPosition, robotRegionOfTravel):
    # Return True if you hit an obstacle (both sensors are true), if you
    # only have one sensor then count that as a scrape and return false
    # leftObst, rightObst  = self.myBot.obstacle()
    leftObst  = self.hasObstacle(finchConstants.LEFT)
    rightObst = self.hasObstacle(finchConstants.RIGHT)
    if leftObst == True and rightObst == True:
      return True
    elif leftObst == True or rightObst == True:
      # The robot sensor don't always report true even
      # when there's an obstacle right in front of it.  
      # If the robot is close to the edge of it's region
      # of travel then report this as a scrape otherwise
      # report it as an obstacle
      if self.isRobotCloseToEdge(robotPosition, robotRegionOfTravel) == True:
        if leftObst == True:
          self.lastScrapedSide = finchConstants.LEFT
        else:
          self.lastScrapedSide = finchConstants.RIGHT
        return False
      else:
        return True
    return False

  # Determines if robot is oriented along the x or y axis (within 10 degree of it)
  def robotOrientedAlongAxis(self,robotPosition):
    orientedTowardAxis = " "
    if ( robotPosition[botUtils.POS_OF_ANGLE] < 10 | robotPosition[botUtils.POS_OF_ANGLE] > 350 ):
      orientedTowardAxis = "X+"
    elif ( robotPosition[botUtils.POS_OF_ANGLE] > 170 and robotPosition[botUtils.POS_OF_ANGLE] < 190 ):
      orientedTowardAxis = "X-"
    elif ( robotPosition[botUtils.POS_OF_ANGLE] > 80 and robotPosition[botUtils.POS_OF_ANGLE] < 100 ):
      orientedTowardAxis = "Y+"
    elif ( robotPosition[botUtils.POS_OF_ANGLE] > 260 and robotPosition[botUtils.POS_OF_ANGLE] < 280 ):
      orientedTowardAxis = "Y-"
    return orientedTowardAxis

  # Determine if robot is close to a particular regions edge
  def getRobotClosestEdges(self, robotPosition, regionOfTravel, threshold=finchConstants.HALFMYWIDTH):
    # Calculate the distance from coordinates
    closeEdges = []
    distanceToLeftX = robotPosition[botUtils.POS_OF_X] - regionOfTravel[0]
    distanceToRightX = regionOfTravel[2] - robotPosition[botUtils.POS_OF_X] 
    distanceFromBottomY = robotPosition[botUtils.POS_OF_Y] - regionOfTravel[1]
    distanceFromTopY = regionOfTravel[3] - robotPosition[botUtils.POS_OF_Y]
    if (distanceToLeftX <= threshold):
      closeEdges.append("LX")
    elif (distanceToRightX <= threshold):
      closeEdges.append("UX")

    if (distanceFromBottomY <= threshold):
      closeEdges.append("LY")
    elif (distanceFromTopY <= threshold):
      closeEdges.append("UY")
    return closeEdges

  def getFinchReference(self):
    return self.myBot
 
  # Revisit this, there's definitely better way to do this... look in to matrix trasnformations
  def checkAndSetObstacleDirectionToTry(self, robotPosition, regionOfTravel, threshold=finchConstants.HALFMYWIDTH):
    # Get closest edges
    myCloseEdges = self.getRobotClosestEdges(robotPosition, regionOfTravel, threshold)
    newDirection = " "
    if len(myCloseEdges) > 0:
      # We are close to an edge, get the robot orientation to figure out the edges that
      # are used to set new direction... when in x direction we look at y values, when
      # pointing in y direction we look at x values
      robotOrientation = self.robotOrientedAlongAxis(robotPosition)
      if robotOrientation == "X+":
        if "UY" in myCloseEdges:
          newDirection = finchConstants.RIGHT
        elif "LY" in myCloseEdges:
          newDirection = finchConstants.LEFT
      elif robotOrientation == "X-":
        if "UY" in myCloseEdges:
          newDirection = finchConstants.LEFT
        elif "LY" in myCloseEdges:
          newDirection = finchConstants.RIGHT
      elif robotOrientation == "Y+":
        if "UX" in myCloseEdges:
          newDirection = finchConstants.LEFT
        elif "LX" in myCloseEdges:
          newDirection = finchConstants.RIGHT
      elif robotOrientation == "Y-":
        if "UX" in myCloseEdges:
          newDirection = finchConstants.RIGHT
        elif "LX" in myCloseEdges:
          newDirection = finchConstants.LEFT

      if newDirection != self.obstacleDirectionToTry:
        self.flipObstacleDirectionToTry()
      

  # Helper just returns true or false stating that we're close to edge.
  def isRobotCloseToEdge(self, robotPosition, regionOfTravel, threshold=finchConstants.HALFMYWIDTH):
    edgesCloseTo = self.getRobotClosestEdges(robotPosition, regionOfTravel, threshold)
    if len(edgesCloseTo) > 0:
      return True
    else:
      return False

  # Set the finches nose color :)
  def setLedColor(self, theColor):
    if theColor == finchConstants.RED:
      self.myBot.led(255,0,0)
    elif theColor == finchConstants.GREEN:
      self.myBot.led(0,255,0)
    elif theColor == finchConstants.BLUE:
      self.myBot.led(0,0,255)

    
  # Return status of all robot attributes
  def status(self):
    # This returns elapsed time since clock was set and a tuple with the attributes, the wheels, obstacle and lights
    # are tuples (so it's a tuple of tuples (except for temp))
    leftObst, rightObst  = self.myBot.obstacle()
    
    print("leftObst: {0} rightObst: {1}".format(leftObst,rightObst))
    currStat = (self.getElapsedTime(),
                (self.wheelHelper("L",True), self.wheelHelper("R",True)),  
                self.myBot.temperature(),
                (self.myBot.light()),
                (leftObst, rightObst),
                (self.myBot.acceleration()))
    
    return currStat
    # comment below was up above
    #            (self.leftWheel+finchConstants.LEFTWHEELADJUSTMENT, self.rightWheel+finchConstants.RIGHTWHEELADJUSTMENT), \