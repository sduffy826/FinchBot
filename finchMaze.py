# Little program to test the finch and path's it'd take

#from finch import Finch 
import finchClass
import finchConstants
import botUtils
import time 
import pythonUtils
import logging 
import sys

from collections import deque

STEPTHRU = False

logging.basicConfig(stream=sys.stdout, filename='finchRobot.log', level=logging.DEBUG)

# file_handler = logging.FileHandler(filename='finchRobot.log')
# stdout_handler = logging.StreamHandler(sys.stdout)
# handlers = [file_handler, stdout_handler]

# logging.basicConfig(
#     level=logging.DEBUG, 
#     format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
#     handlers=handlers
#)

# handler = logging.StreamHandler(sys.stdout)
# handler.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# root.addHandler(handler)

smallTest = True

# This a stack, it has our current target location and the speed
# we should use to get there... it's a stack so targets are processed
# from bottom up
targetPosition = deque()

if smallTest == False:
  targetPosition.append((72.0, 6.0, 0.0, finchConstants.TOPSPEED))
  targetPosition.append((68.0, 6.0, 0.0, finchConstants.SLOWSPEED)) 
  robotRegion = (0.0, -6.0, 18, 96)
else:
  targetPosition.append((42.0, 18.0, 0.0, finchConstants.TOPSPEED))
  targetPosition.append((38.0, 18.0, 0.0, finchConstants.SLOWSPEED))
  robotRegion = (0.0,-6.0,50,24)

# This just tracks where we have been, we start at the origin
robotPositions = []
robotPositions.append((0.0,0.0,0.0))

myRobot = finchClass.MyRobot(0.0, 0.0, True)

logging.info("finchMaze.py, Program started")

# Enter while loop to process all the records that have the location
# we should be moving to.
while len(targetPosition) > 0:
  myRobot.setLedColor(finchConstants.GREEN)

  if STEPTHRU:
    print("=============================================================================================================")
    dumbKey = pythonUtils.input_char("Debug mode, hit any key 'q' to quit")
    if dumbKey == "q":
      break

  # Get next target, what the speed specified to get there and then
  # calculate how much distance will be covered with that speed (per sec)
  nextTarget        = targetPosition.pop()
  wheelSpeed2Use    = nextTarget[3] 
  distancePerSecond = finchConstants.getDistancePerSecond(wheelSpeed2Use)
 
  # Current position is the last one in the robotPositions array
  positionOfCurrentPosition = len(robotPositions)-1
  currPos                   = robotPositions[positionOfCurrentPosition]
 
  logging.info("finchMaze.py. Next target:{0} currPos{1}".format(str(nextTarget),str(currPos)))
   
  # MAKE THIS A CONFIGURATION PARAMETER
  # Calculate using the X axis as primary movement
  logging.debug("finchMaze.py, Calculating path when traveling along X axis first")
  pathToUse = botUtils.calculateMovementToTarget(currPos,nextTarget,botUtils.X_PATH)

  logging.debug("finchMaze.py, paths to use below")
  for aPath in pathToUse:
    logging.debug("  {0}".format(str(aPath)))
  
  if STEPTHRU:
    dumbKey = pythonUtils.input_char("Debug mode, about to make moves, hit any key 'q' to quit")
    if dumbKey == "q":
      break

  # Enter a while loop to process all the required movements to get to the
  # target position... if we're unsuccesful then we'll set our current position
  # and push the targetPosition back onto the stack so that it'll be retried
  # again from the current position
  # If an obstacle is found then correctingMyself with be set to True, we'll
  # try to reposition ourselves to a new position
  successfulMovements = True
  correctingOurself   = False
  movementPosition    = 0
  while movementPosition < len(pathToUse) and (successfulMovements or correctingOurself):
    # Process each movement
    theMovement       = pathToUse[movementPosition]
    movementPosition += 1
    logging.debug("finchMaze.py, Movement:{0} is:{1}".format(movementPosition,str(theMovement)))

    # Process turn movement or forward movement, only two kinds :) 
    if theMovement[botUtils.MOVEMENT_TYPE] == botUtils.TURN:
      if theMovement[botUtils.MOVEMENT_VALUE] < 0.0:
        myRobot.rightTurn(-theMovement[botUtils.MOVEMENT_VALUE])
      else:
        myRobot.leftTurn(theMovement[botUtils.MOVEMENT_VALUE])
      currPos = botUtils.whatsNewPositionAfterMovement(currPos, theMovement)
      robotPositions.append(currPos)
    elif theMovement[botUtils.MOVEMENT_TYPE] == botUtils.FORWARD or theMovement[botUtils.MOVEMENT_TYPE] == botUtils.BACKWARD:
      if theMovement[botUtils.MOVEMENT_TYPE] == botUtils.BACKWARD:
        wheelDirection = -1.0
      else:
        wheelDirection = 1.0

      # Reset the timer, we need to keep track of how long we're traveling
      time2Target = (theMovement[botUtils.MOVEMENT_VALUE]/distancePerSecond)

      logging.debug("finchMaze.py, wheelDirection:{0} time2Target{1:.2f} wheelSpeed2Use:{2:.2f}".format(wheelDirection,time2Target,wheelSpeed2Use))

      myRobot.resetTimer()
      myRobot.resetState()
      # Start moving forward at the requested speed, we'll continue moving
      # till we reach our destination or we can't move any longer
      myRobot.setWheels(wheelSpeed2Use*wheelDirection,wheelSpeed2Use*wheelDirection,True)
      while True:
        timeMoving   = myRobot.getElapsedTime()
        robotCanMove = myRobot.canMove()
        logging.debug("finchMaze.py,  Looping till movement done, timeMoving:{0} robotCanMove:{1}".format(timeMoving,robotCanMove))
        if timeMoving >= time2Target or robotCanMove == False:
          break
      myRobot.stop()

      # Calculate the new position we are at, we create a movement tuple
      # so that we can call routine to calculate current position 
      actualMovement = (theMovement[botUtils.MOVEMENT_TYPE],(timeMoving * distancePerSecond))
      currPos        = botUtils.whatsNewPositionAfterMovement(currPos,actualMovement)
      robotPositions.append(currPos)

      logging.debug("finchMaze.py, time moved:{0}  time2Target was:{1}".format(timeMoving,time2Target))

      # If we didn't reach our target then we were unsuccessful
      if timeMoving < time2Target: 
        successfulMovements = False
        if correctingOurself == False: 
          correctingOurself = True
          # We hit an obstacle... try fixing ourselvs
          # First we clear out all the remaining movements, we replace them with our correcing ones
          movementPosition = 0
          pathToUse.clear()
          if myRobot.isObstacle(currPos,robotRegion):
            # Have an obstacle, first call routine to check direction to move then call routine to 
            # get out of it's path
            myRobot.setLedColor(finchConstants.RED)
            myRobot.checkAndSetObstacleDirectionToTry(currPos, robotRegion)
            pathToUse = myRobot.getOutOfObstacle(myRobot.getObstacleDirectionToTry())
            logging.debug("finchMaze.py, Obstruction:OBSTACLE, path below")
          else:
            myRobot.setLedColor(finchConstants.BLUE)
            pathToUse = myRobot.getOutOfScrape(myRobot.getLastScrapeSide())
            logging.debug("finchMaze.py, Obstruction:SCRAPE, path below")
          
          # Put out the path from the obstacle or scrape
          for aMovement in pathToUse:
            logging.debug("finchMaze.py,  {0}".format(str(aMovement)))
  
  if successfulMovements == False:
    # We weren't successful, put the target back onto the stack
    targetPosition.append(nextTarget)

myRobot.shutDown()

logging.info("finchMaze.py, DONE")
logging.debug("finchMaze.py, robot positions that were recorded are below")
for aPos in robotPositions:
  logging.debug("  {0}".format(str(aPos)))
