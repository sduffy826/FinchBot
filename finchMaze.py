# Little program to test the finch and path's it'd take

#from finch import Finch 
import finchClass
import finchConstants
import botUtils
import time 
import pythonUtils

from collections import deque

DEBUGIT = True
DEBUGIT2 = False

smallTest = True

# This a stack, it has our current target location and the speed
# we should use to get there... it's a stack so targets are processed
# from bottom up
targetPosition = deque()

if smallTest == False:
  targetPosition.append((72.0, 6.0, 0.0, finchConstants.TOPSPEED))
  targetPosition.append((68.0, 6.0, 0.0, finchConstants.SLOWSPEED)) 
else:
  targetPosition.append((50.0, 18.0, 0.0, finchConstants.TOPSPEED))
  targetPosition.append((46.0, 18.0, 0.0, finchConstants.SLOWSPEED))

# This just tracks where we have been, we start at the origin
robotPositions = []
robotPositions.append((0.0,0.0,0.0))

myRobot = finchClass.MyRobot(0.0, 0.0, True)

for i in range(10):
  print("\n")

# Enter while loop to process all the records that have the location
# we should be moving to.
while len(targetPosition) > 0:
  if DEBUGIT:
    print("=============================================================================================================")
    dumbKey = pythonUtils.input_char("Debug mode, hit any key 'q' to quit")
    if dumbKey == "q":
      break

  # Get next target, what the speed specified to get there and then
  # calculate how much distance will be covered with that speed (per sec)
  nextTarget        = targetPosition.pop()
  wheelSpeed2Use    = nextTarget[3] 
  distancePerSecond = finchConstants.getSpeedPerSecond(wheelSpeed2Use)
 
  # Current position is the last one in the robotPositions array
  positionOfCurrentPosition = len(robotPositions)-1
  currPos                   = robotPositions[positionOfCurrentPosition]
 
  if DEBUGIT:
    print("Next target:{0} currPos{1}".format(str(nextTarget),str(currPos)))
   
  # MAKE THIS A CONFIGURATION PARAMETER
  # Calculate using the X axis as primary movement
  print("Calculating path when traveling along X axis first")
  pathToUse = botUtils.calculateMovementToTarget(currPos,nextTarget,botUtils.X_PATH)

  if DEBUGIT:
    print("Paths to use")
    for aPath in pathToUse:
      print("  {0}".format(str(aPath)))
    dumbKey = pythonUtils.input_char("Debug mode, hit any key 'q' to quit")
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
    if DEBUGIT:
      print("Movement:{0} is:{1}".format(movementPosition,str(theMovement)))

    # Process turn movement or forward movement, only two kinds :) 
    if theMovement[0] == botUtils.TURN:
      if theMovement[1] < 0.0:
        myRobot.rightTurn(-theMovement[1])
      else:
        myRobot.leftTurn(theMovement[1])
      currPos = botUtils.whatsNewPositionAfterMovement(currPos, theMovement)
      robotPositions.append(currPos)
    elif theMovement[0] == botUtils.FORWARD or theMovement[0] == botUtils.BACKWARD:
      if theMovement[0] == botUtils.BACKWARD:
        wheelDirection = -1.0
      else:
        wheelDirection = 1.0

      # Reset the timer, we need to keep track of how long we're traveling
      time2Target = (theMovement[1]/distancePerSecond)

      if DEBUGIT:
        print("  wheelDirection:{0} time2Target{1:.2f} wheelSpeed2Use:{2:.2f}".format(wheelDirection,time2Target,wheelSpeed2Use))

      myRobot.resetTimer()
      myRobot.resetState()
      # Start moving forward at the requested speed, we'll continue moving
      # till we reach our destination or we can't move any longer
      myRobot.setWheels(wheelSpeed2Use*wheelDirection,wheelSpeed2Use*wheelDirection,True)
      while True:
        timeMoving   = myRobot.getElapsedTime()
        robotCanMove = myRobot.canMove()
        if DEBUGIT2:
          print("  Looping, timeMoving:{0} robotCanMove:{1}".format(timeMoving,robotCanMove))
        if timeMoving >= time2Target or robotCanMove == False:
          break
      myRobot.stop()

      # Calculate the new position we are at, we create a movement tuple
      # so that we can call routine to calculate current position 
      actualMovement = (theMovement[0],(timeMoving * distancePerSecond))
      currPos        = botUtils.whatsNewPositionAfterMovement(currPos,actualMovement)
      robotPositions.append(currPos)

      if DEBUGIT:
        print("  Time moved:{0}  time2Target was:{1}".format(timeMoving,time2Target))

      # If we didn't reach our target then we were unsuccessful
      if timeMoving < time2Target: 
        successfulMovements = False
        if correctingOurself == False: 
          correctingOurself = True
          # We hit an obstacle... try fixing ourselvs
          # First we clear out all the remaining movements, we replace them with our correcing ones
          movementPosition = 0
          pathToUse.clear()
          if myRobot.isObstacle():
            pathToUse = myRobot.getOutOfObstacle(myRobot.getObstacleDirectionToTry())
          else:
            pathToUse = myRobot.getOutOfScrape(myRobot.getLastScrapeSide())
          if DEBUGIT:
            print("In Obstacle avoidance, the path selected will be")
            for aMovement in pathToUse:
              print(str(aMovement))

  
  if successfulMovements == False:
    # We weren't successful, put the target back onto the stack
    targetPosition.append(nextTarget)

myRobot.shutDown()

if DEBUGIT:
  print("Value of robotPositionss")
  for aPos in robotPositions:
    print(str(aPos))
