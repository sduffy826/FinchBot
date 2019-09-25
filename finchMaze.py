# Little program to test the finch and path's it'd take

#from finch import Finch 
import finchClass
import finchConstants
import botUtils
import time 

from collections import deque

DEBUGIT = True

# from getkey import getkey, keys

# This a stack, it has our current target location and the speed
# we should use to get there
targetPosition = deque()
targetPosition.append((72.0, 6.0, 0.0, finchConstants.TOPSPEED))
targetPosition.append((68.0, 6.0, 0.0, finchConstants.SLOWSPEED)) 
#targetPosition.append((8.0, 6, 0.0, finchConstants.SLOWSPEED))
#targetPosition.append((6.0, 0.0, 0.0, finchConstants.SLOWSPEED))
# This just tracks where we have been, we start at the origin
robotPositions = []
robotPositions.append((0.0,0.0,0.0))

myRobot = finchClass.MyRobot(0.0, 0.0, True)

for i in range(10):
  print("\n")

# Enter while loop to process all the records that have the location
# we should be moving to.
while len(targetPosition) > 0:
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

  # Enter a while loop to process all the required movements to get to the
  # target position... if we're unsuccesful then we'll set our current position
  # and push the targetPosition back onto the stack so that it'll be retried
  # again from the current position
  successfulMovements = True
  movementPosition    = 0
  while movementPosition < len(pathToUse) and successfulMovements == True:
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
    elif theMovement[0] == botUtils.FORWARD:
      # Reset the timer, we need to keep track of how long we're traveling
      time2Target = (theMovement[1]/distancePerSecond)
      myRobot.resetTimer()
      # Start moving forward at the requested speed, we'll continue moving
      # till we reach our destination or we can't move any longer
      myRobot.setWheels(wheelSpeed2Use,wheelSpeed2Use,True)
      while True:
        timeMoving   = myRobot.getElapsedTime()
        robotCanMove = myRobot.canMove()
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
  
  if successfulMovements == False:
    # We weren't successful, put the target back onto the stack
    targetPosition.append(nextTarget)

myRobot.shutDown()

if DEBUGIT:
  print("Value of robotPositionss")
  for aPos in robotPositions:
    print(str(aPos))

  # Calculate using the Y axis as primary movement
  #print("\nWhen going along Y axis first")
  #pathToUse = botUtils.calculateMovementToTarget(currentPosition,nextTarget,botUtils.Y_PATH)
  #for movements in pathToUse:
  #  print(str(movements))

  # Calculate using she shortest path
  #print("\nWhen going in straight line")
  #pathToUse = botUtils.calculateMovementToTarget(currentPosition,nextTarget,botUtils.DIRECT_PATH)
  #3for movements in pathToUse:
  #  print(str(movements))








# Goal go from current position to the target one
#   If x we are at is not x target then
#     calculate the angle we need to adjust to get back to angle 0
#     move from current x to the target x
#   else:
#     if the target Y position is greater than what we are at then 
#       adjust angle so we're at 90'
#     else:
#       adjust angle so we-re at -90'
#     move to the y position, if we're at -90 then decreas otherwise increase
#   loop till we have traveled for appropriate time or we have hit an obstacle
#   calculate our new position base on amount of time traveled
#   if we are not at the target location then push the target location back on stack


# calculate the angle we want

