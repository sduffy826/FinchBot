from finch import Finch 
import time 
import finchConstants
import botUtils
import pythonUtils
import logging

# get logger for finchClass, if you want a new one then have the parent program initialize
# the logger with the last parm of True
finchClassLogger = pythonUtils.getCustomLogger("finchClass",logging.INFO,logging.DEBUG, False)

STAT_ELAPSED = 0
STAT_WHEELS = 1
STAT_TEMP = 2
STAT_LIGHTS = 3
STAT_OBSTACLE = 4
STAT_ACCEL = 5

# Specify the constants for how long an obstacle must persist before it's reported as On
OBSTACLE_PERSIST_TIME_REQUIRED = 0.1

OBSTACLE_READING_DELAY = 0.01

# Set amount for thresholdtoside; if we're within that and hit an
# obstacle then it's a scrap
THRESHOLDTOSIDE = finchConstants.HALFMYWIDTH + 1

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

    # Use vars below for logging when 
    self.lastPersistedLeftObstacleState = False
    self.lastPersistedRightObstacleState = False

    # Obstacle reading goes haywire... we'll count up readings within
    # an interval and use the overall score to report
    self.lastObstacleReading = 0.0
    self.lastObstacleReadingLeftScores  = [0,0,0,0,0]
    self.lastObstacleReadingRightScores = [0,0,0,0,0]
    self.scorePosition = 0
    self.obstacleNumberOfScores = len(self.lastObstacleReadingLeftScores)

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

    self.lastPersistedLeftObstacleState = False
    self.lastPersistedRightObstacleState = False
    self.lastObstacleReading = 0.0
    self.lastObstacleReadingLeftScores  = [0,0,0,0,0]
    self.lastObstacleReadingRightScores = [0,0,0,0,0]
    self.scorePosition = 0

  # This is common routine to update the dictionary 'state' items associated
  # with the sensors... we need this because we need the state to persist for
  # a given amount of time before we think of it as 'real' (the bot sensors are flakey)
  # NOTE: The state will only be updated when wheels are moving, or you pass in the 
  # forceUpdate indicator
  def updateMyState(self, forceUpdate=False):
    if self.leftWheel != 0.0 or self.rightWheel != 0.0 or forceUpdate:
      stateTime = time.time()
    
      leftObst, rightObst  = self.myBot.obstacle()

      # Because obstacle readings are erradic I take last 5 readings, and report that
      # value if sum of array is > 2 then report True else report false
      if leftObst == True:
        leftIntValue = 1
      else:
        leftIntValue = 0
      if rightObst == True:
        rightIntValue = 1
      else:
        rightIntValue = 0
      indexPosition = self.scorePosition % 5
      self.lastObstacleReadingLeftScores[indexPosition] = leftIntValue
      self.lastObstacleReadingRightScores[indexPosition] = rightIntValue

      self.scorePosition = indexPosition + 1

      lastReadingElapsed = round(stateTime - self.lastObstacleReading,3)
      finchClassLogger.debug("finchClass-updateMyState, lastReadingElapsed: {0}, leftObst: {1} rightObst{2}".format(lastReadingElapsed,leftObst,rightObst))
      # If reading is less than intervals ignore it
      if lastReadingElapsed < OBSTACLE_READING_DELAY:
        return

      self.lastObstacleReading = stateTime

      # Calculate the value for each of the obstacle sensors
      leftIntValue = 0
      rightIntValue = 0
      indexPosition = 0
      while indexPosition < self.obstacleNumberOfScores:
        leftIntValue += self.lastObstacleReadingLeftScores[indexPosition]
        rightIntValue += self.lastObstacleReadingRightScores[indexPosition]
        indexPosition += 1

      if leftIntValue > 2:
        leftObstacleReading = True
      else:
        leftObstacleReading = False

      if rightIntValue > 2:
        rightObstacleReading = True
      else:
        rightObstacleReading = False
      finchClassLogger.debug("finchClass-updateMyState, leftObstacleReading: {0} rightObstacleReading: {1}".format(leftObstacleReading,rightObstacleReading))
      
      # State changed or time hasn't been set
      if self.obstacleState["left"] != leftObstacleReading or self.obstacleState["leftStateTime"] == 0.0:
        finchClassLogger.info("finchClass-updateMyState, STATE Changed, Left was:{0} is:{1}".format(str(self.obstacleState["left"]),str(leftObstacleReading)))
        self.obstacleState["left"] = leftObstacleReading
        self.obstacleState["leftStateTime"] = stateTime
        self.obstacleState["leftElapsedTime"] = 0.0        
      else:
        # Calculate the elapsed time in this state
        self.obstacleState["leftElapsedTime"] = round(stateTime - self.obstacleState["leftStateTime"],4)

      # Same as above but check the right obstacle sensor
      if self.obstacleState["right"] != rightObstacleReading or self.obstacleState["rightStateTime"] == 0.0:
        finchClassLogger.info("finchClass-updateMyState, STATE Changed, Right was:{0} is:{1}".format(str(self.obstacleState["right"]),str(rightObstacleReading)))
        self.obstacleState["right"] = rightObstacleReading
        self.obstacleState["rightStateTime"] = stateTime
        self.obstacleState["rightElapsedTime"] = 0.0
      else:
        self.obstacleState["rightElapsedTime"] = round(stateTime - self.obstacleState["rightStateTime"],4)
  
  # Helper to return indicator if an obstacle exists, we did this because we need the obstacle to
  # persist for an amount of time (thresholdInSecs) before we say it's on
  # Caller can specify which sensor to check (LEFT/RIGHT, if they don't then it'll return True if
  # either sensor reports an obstacle)
  def hasObstacle(self,whichOne,thresholdInSecs=OBSTACLE_PERSIST_TIME_REQUIRED):
    # Commented out logger... too many messages here, changed 'updateMyState' to report when state changes
    # finchClassLogger.debug("finchClass-hasObstacle, obstacleState:{0}".format(str(self.obstacleState)))
    leftObst = False
    if self.obstacleState["leftElapsedTime"] > thresholdInSecs:
      leftObst = self.obstacleState["left"]
      if leftObst != self.lastPersistedLeftObstacleState:    
        finchClassLogger.info("finchClass-hasObstacle, PERSISTED Left Obstacle State Change old/new: {0}/{1}".format(self.lastPersistedLeftObstacleState,leftObst))
        self.lastPersistedLeftObstacleState = leftObst
    
    rightObst = False
    if self.obstacleState["rightElapsedTime"] > thresholdInSecs:
      rightObst = self.obstacleState["right"]
      if leftObst != self.lastPersistedLeftObstacleState:    
        finchClassLogger.info("finchClass-hasObstacle, PERSISTED Right Obstacle State Change old/new: {0}/{1}".format(self.lastPersistedRightObstacleState,rightObst))
        self.lastPersistedRightObstacleState = rightObst

    # finchClassLogger.debug("finchClass-hasObstacle, leftObst:{0} rightObst{1}".format(leftObst,rightObst))

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
    finchClassLogger.debug("finchClass-update, left: {0:.2f} right: {1:.2f}".format(self.wheelHelper("L"), self.wheelHelper("R")))

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
  def canMove(self, ignoreObstacles):
    # Add logic for other sensors
    # If we're going in reverse then don't check sensors
    if (self.leftWheel <= 0.0 and self.rightWheel <= 0.0) or ignoreObstacles:
      # print("canMove, ignoring obstacles")
      return True
    else:
      self.updateMyState()
      rtnValue = (self.hasObstacle("BOTH") == False)
      # print("canMove returns {0}".format(rtnValue))
      return rtnValue

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
    distanceToBackup = (finchConstants.TOTALWIDTH) / botUtils.degreesSin(45)
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
    finchClassLogger.info("finchClass-flipObstacleDirectionToTry, new direction: {0}".format(self.obstacleDirectionToTry))

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
    if ( robotPosition[botUtils.POS_OF_ANGLE] < 10 or robotPosition[botUtils.POS_OF_ANGLE] > 350 ):
      orientedTowardAxis = "X+"
    elif ( robotPosition[botUtils.POS_OF_ANGLE] > 170 and robotPosition[botUtils.POS_OF_ANGLE] < 190 ):
      orientedTowardAxis = "X-"
    elif ( robotPosition[botUtils.POS_OF_ANGLE] > 80 and robotPosition[botUtils.POS_OF_ANGLE] < 100 ):
      orientedTowardAxis = "Y+"
    elif ( robotPosition[botUtils.POS_OF_ANGLE] > 260 and robotPosition[botUtils.POS_OF_ANGLE] < 280 ):
      orientedTowardAxis = "Y-"
    return orientedTowardAxis

  # Determine if robot is close to a particular regions edge
  def getRobotClosestEdges(self, robotPosition, regionOfTravel, threshold=THRESHOLDTOSIDE):
    # Calculate the distance from coordinates
    closeEdges = []
    distanceToLeftX = robotPosition[botUtils.POS_OF_X] - regionOfTravel[0]
    distanceToRightX = regionOfTravel[2] - robotPosition[botUtils.POS_OF_X] 
    distanceFromBottomY = robotPosition[botUtils.POS_OF_Y] - regionOfTravel[1]
    distanceFromTopY = regionOfTravel[3] - robotPosition[botUtils.POS_OF_Y]
    
    tempString = "finchClass.py, getRobotClosesEdges, robotPosition: {0} regionOfTravel: {1} threshold: {2}"
    finchClassLogger.debug(tempString.format(str(robotPosition),str(regionOfTravel),threshold))
    tempString = "   leftXDist: {0} rightXDist: {1}, lowerYDist: {2} upperYDist: {3}"
    finchClassLogger.debug(tempString.format(distanceToLeftX,distanceToRightX, distanceFromBottomY, distanceFromTopY))
    
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
  def checkAndSetObstacleDirectionToTry(self, robotPosition, regionOfTravel, threshold=THRESHOLDTOSIDE):
    # Get closest edges
    finchClassLogger.debug("finchClass.py, checkAndSetObstacleDirectionToTry, start")
    myCloseEdges = self.getRobotClosestEdges(robotPosition, regionOfTravel, threshold)
    newDirection = " "
    if len(myCloseEdges) > 0:
      finchClassLogger.debug("finchClass.py, checkAndSetObstacleDirectionToTry, values below")
      for anEdge in myCloseEdges:
        finchClassLogger.debug("  {0}".format(str(anEdge)))
   
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

      finchClassLogger.debug("finchClass.py, checkAndSetObstacleDirectionToTry, oldDirection: {0} newDirection: {1}".format(self.obstacleDirectionToTry,newDirection))
      if newDirection != self.obstacleDirectionToTry:
        self.flipObstacleDirectionToTry()
    finchClassLogger.debug("finchClass.py, checkAndSetObstacleDirectionToTry, start")

  # Helper just returns true or false stating that we're close to edge.
  def isRobotCloseToEdge(self, robotPosition, regionOfTravel, threshold=THRESHOLDTOSIDE):
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
    currStat = (self.getElapsedTime(),
                (self.wheelHelper("L",True), self.wheelHelper("R",True)),  
                self.myBot.temperature(),
                (self.myBot.light()),
                (leftObst, rightObst),
                (self.myBot.acceleration()))
    
    return currStat
    # comment below was up above
    #            (self.leftWheel+finchConstants.LEFTWHEELADJUSTMENT, self.rightWheel+finchConstants.RIGHTWHEELADJUSTMENT), \