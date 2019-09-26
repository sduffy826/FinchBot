# Little program to test the finch and path's it'd take

#from finch import Finch 
import finchClass
import finchConstants
import botUtils
import time 

from collections import deque

myRobot = finchClass.MyRobot(0.0, 0.0, True)

# This a stack, it has our current target location and the speed
# we should use to get there
targetPosition = deque()
targetPosition.append((72.0, 6, 0.0, finchConstants.TOPSPEED))
targetPosition.append((68.0, 6.0, 0.0, finchConstants.SLOWSPEED)) 

# This just tracks where we have been, we start at the origin
robotPositions = []
robotPositions.append((0.0,0,0,0.0))

for x in range(5):
  print("")

paths2Test = botUtils.X_PATH
testObstaclesAndScrapes = True

while len(targetPosition) > 0:
  nextTarget = targetPosition.pop()
  speedToTravel = nextTarget[3]

  positionOfCurrentPosition = len(robotPositions)-1
  currentPosition = robotPositions[positionOfCurrentPosition]

  if paths2Test == "ALL" or paths2Test == botUtils.X_PATH:  
    # Calculate using the X axis as primary movement
    print("Calculating path when traveling along X axis first")
    pathToUse = botUtils.calculateMovementToTarget(currentPosition,nextTarget,botUtils.X_PATH)
    for movements in pathToUse:
      print(str(movements))

  if paths2Test == "ALL" or paths2Test == botUtils.Y_PATH:  
    # Calculate using the Y axis as primary movement
    print("\nWhen going along Y axis first")
    pathToUse = botUtils.calculateMovementToTarget(currentPosition,nextTarget,botUtils.Y_PATH)
    for movements in pathToUse:
      print(str(movements))

  if paths2Test == "ALL" or paths2Test == botUtils.DIRECT_PATH:  
    # Calculate using she shortest path
    print("\nWhen going in straight line")
    pathToUse = botUtils.calculateMovementToTarget(currentPosition,nextTarget,botUtils.DIRECT_PATH)
    for movements in pathToUse:
      print(str(movements))

  # Calculate the new current position (we use movements from last one, but the endpoint should
  # be the same for all)
  robotPositions.append(botUtils.whatsNewPositionAfterMovements(currentPosition, pathToUse))

  if testObstaclesAndScrapes:
    # Check the obstacle and scrapes
    pathToUse = myRobot.getOutOfObstacle(finchConstants.LEFT)
    print("\n\nObstacle simulation, turning LEFT")
    for movements in pathToUse:
      print(str(movements))

    # Check the obstacle and scrapes
    pathToUse = myRobot.getOutOfObstacle(finchConstants.RIGHT)
    print("\n\nObstacle simulation, turning RIGHT")
    for movements in pathToUse:
      print(str(movements))

    # Check scrape on right
    pathToUse = myRobot.getOutOfScrape(finchConstants.RIGHT)
    print("\n\nObstacle simulation, scrap on right side")
    for movements in pathToUse:
      print(str(movements))      

    # Check scrape on left
    pathToUse = myRobot.getOutOfScrape(finchConstants.LEFT)
    print("\n\nObstacle simulation, scrap on left side")
    for movements in pathToUse:
      print(str(movements))      







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

