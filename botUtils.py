import math
import logging

FORWARD = "F"
TURN = "T"
BACKWARD = "B"

X_PATH = "X"
Y_PATH = "Y"
DIRECT_PATH = "S"
DEBUGIT = True

MINANGLETOTURN=3.0
MINDISTANCETOTRAVEL=0.5
POS_OF_X=0
POS_OF_Y=1
POS_OF_ANGLE=2

# For movements
MOVEMENT_TYPE=0
MOVEMENT_VALUE=1

logging.basicConfig(filename='finchRobot.log', level=logging.DEBUG)

# ----------------------------------------------------------------------
# Calculate the angle required to get from the current position to the
# desired point
def calculateAngleToTarget(currentPosition, endX, endY):
  xDelta = endX - currentPosition[POS_OF_X]
  yDelta = endY - currentPosition[POS_OF_Y]

  logging.debug("boUtils-calculateAngleToTarget, xDelta: {0:.2f} yDelta: {1:.2f}".format(xDelta,yDelta))

  arcTanVar = 0.0
  if (xDelta == 0.0):
    angle2GetThere = 90.0 
  else:
    if (yDelta != 0.0):
      arcTanVar = (yDelta*1.0)/(xDelta*1.0)
    
    angle2GetThere = round(math.degrees(math.atan(abs(arcTanVar))),0)
    logging.debug("boUtils-calculateAngleToTarget, arcTan: {2:.4f}".format(arcTanVar))

  if xDelta < 0:
    if yDelta < 0:
      angle2GetThere += 180.0
    else:
      angle2GetThere = 180.0 - angle2GetThere
  else:
    # X positive, if y negative then 4th quadrant and desired angle
    # is 360 - calculated angle
    if yDelta < 0:
      angle2GetThere = 360 - angle2GetThere 

  logging.debug("boUtils-calculateAngleToTarget,, angle: {0:.2f}".format(angle2GetThere))
  
  return angle2GetThere


# ----------------------------------------------------------------------
# Calculate the number of degrees you need to turn left or right
# in order to get oriented to the desired angle.  It will
# return a tuple (leftDegrees, rightDegrees).  fyi: Right degrees
# are always negative (angles of rotation).
def calculateDegrees(fromPosition, toPosition):
  toPositionNegativeRotation = -(360.0 - toPosition)
  degreesRight = ( fromPosition - toPositionNegativeRotation ) % 360
  degreesLeft  = ((toPosition + 360) - fromPosition) % 360
  return (degreesLeft, -degreesRight)


# ----------------------------------------------------------------------
# Calculate difference between two points 
def calculateDistanceBetweenPoints(startPosition,endPosition):
  deltaX = endPosition[POS_OF_X]-startPosition[POS_OF_X]
  deltaY = endPosition[POS_OF_Y]-startPosition[POS_OF_Y]
  return round(math.sqrt((deltaX*deltaX)+(deltaY*deltaY)),2)


# ----------------------------------------------------------------------
# Calculate target position(s)
# In this routine we have three possible ways to get from A to B
#  1)  We can travel along the x axis until we get to the y position
#       then rotate toward the y position and move there.
#  2)  We can do the similarly but move in y position first, then
#       the x one
#  3)  We can go in a straight line from A to B
# This routine is passed the currentPosition (tuple (x, y, degrees)),
# the targetPosition (tuple) and the PathToCalculate ('X', 'Y' or 'S')
# It will return a list of tuples that defines how to get there, the tuple
# returned has xDistance, yDistance, deltaAngle
def calculateMovementToTarget(currentPosition, targetPosition, path2Use):
  logging.debug("boUtils-calculateMovementToTarget, curr:{0} targ:{1} path:{2}".format(str(currentPosition),
                                                                                       str(targetPosition),path2Use))
  if path2Use == X_PATH:
    return calculateMovementToTargetUsingXAxis(currentPosition, targetPosition)
  elif path2Use == Y_PATH: 
    return calculateMovementToTargetUsingYAxis(currentPosition, targetPosition)
  elif path2Use == DIRECT_PATH:
    return calculateMovementToTargetUsingDirectLine(currentPosition, targetPosition)
  else:
    logging.error("Invalid path of {0}".format(path2Use))
  return []


# ----------------------------------------------------------------------
# Calculate the movement for a direct line from source to target
def calculateMovementToTargetUsingDirectLine(startingPosition, endingPosition):
  movement = []
  # Determine angle to target
  destAngleFromHere = calculateAngleToTarget(startingPosition, endingPosition[POS_OF_X], endingPosition[POS_OF_Y])
  # Calculate delta between angle we're at and were we want to be, turn to that (if need to)
  deltaAngle = getMinDegrees(startingPosition[POS_OF_ANGLE],destAngleFromHere)
  if abs(deltaAngle) > MINANGLETOTURN:
    movement.append((TURN, deltaAngle))

  # Calculate distance to target and move to it if need to
  deltaDistance = calculateDistanceBetweenPoints(startingPosition,endingPosition)
  if abs(deltaDistance) > MINDISTANCETOTRAVEL:
    movement.append((FORWARD,deltaDistance))
  return movement


# ----------------------------------------------------------------------
def calculateMovementToTargetUsingXAxis(currentPos, targetPos):  
  # Get the movements necessary to get to the target x position, we pass in the
  # current x position, current angle and the desired x position
  xMovements = calculatePerpendicularMovementToX(currentPos[POS_OF_X], currentPos[POS_OF_ANGLE], targetPos[POS_OF_X])

  logging.debug("boUtils-calculateMovementToTargetUsingXAxis, (X Movment) values below")
  for aMove in xMovements:
    logging.debug("  {0}".format(str(aMove)))

  # We have the movements necessary to get there... determine what your new position
  # would be after it.. need that for determining next set of movements.
  tempPos = whatsNewPositionAfterMovements(currentPos, xMovements)

  logging.debug("boUtils-calculateMovementToTargetUsingXAxis, newPos after that {0}".format(str(tempPos)))

  yMovements = calculatePerpendicularMovementToY(tempPos[POS_OF_Y],tempPos[POS_OF_ANGLE],targetPos[POS_OF_Y])
  logging.debug("boUtils-calculateMovementToTargetUsingXAxis, (Y Movement) values below")
  for aMove in yMovements:
    logging.debug("  {0}".format(str(aMove)))


  # Return the two lists concatenated together.
  return xMovements+yMovements


# ----------------------------------------------------------------------
def calculateMovementToTargetUsingYAxis(currentPos, targetPos):  
  # This is similar to calculateMovementToTargetUsingXAxis except it moves along the Y
  # axis first.
  yMovements = calculatePerpendicularMovementToY(currentPos[POS_OF_Y],currentPos[POS_OF_ANGLE],targetPos[POS_OF_Y])
  # Get new position
  tempPos = whatsNewPositionAfterMovements(currentPos, yMovements)
  # Get xMovements
  xMovements = calculatePerpendicularMovementToX(tempPos[POS_OF_X], tempPos[POS_OF_ANGLE], targetPos[POS_OF_X])

  # Return the two lists concatenated together.
  return yMovements+xMovements


# ----------------------------------------------------------------------
def calculatePerpendicularMovementToX(startX,startAngle,endX):
  # Calculate the degreee of angle to point toward X axis
  # and the distance you need to travel (note the distance is the
  # value from startX so it can be negative)
  x_moves = []
  xUnits = endX - startX

  # Calculate how to move in the x direction
  if xUnits < 0: 
    targetAngle = 180
  else:
    targetAngle = 0
  
  if abs(xUnits) > MINDISTANCETOTRAVEL:
    deltaAngle = getMinDegrees(startAngle,targetAngle)
    # If angle needs to be changed then log the movememtn
    if abs(deltaAngle) > MINANGLETOTURN:
      x_moves.append((TURN,deltaAngle))
    x_moves.append((FORWARD,xUnits))
  return x_moves


# ----------------------------------------------------------------------
def calculatePerpendicularMovementToY(startY,startAngle,endY):
  # Calculate the degreee of angle to point toward Y axis
  # and the distance you need to travel (note the distance is the
  # value from startY so it can be negative)
  y_moves = []
  yUnits = endY - startY

  # Calculate how to move in the y direction, similar to above
  if yUnits < 0: 
    targetAngle = 270
  else:
    targetAngle = 90
  
  if abs(yUnits) > MINDISTANCETOTRAVEL:
    deltaAngle = getMinDegrees(startAngle,targetAngle)
    # If angle needs to be changed then log the movememtn
    if abs(deltaAngle) > MINANGLETOTURN:
      y_moves.append((TURN,deltaAngle))
    y_moves.append((FORWARD,yUnits))
  return y_moves


# ----------------------------------------------------------------------
def calculateScrapeMovement(scrapeAngle, distanceToBackup):
  # Calculate the degreee of angle to point toward Y axis
  # and the distance you need to travel (note the distance is the
  # value from startY so it can be negative)
  logging.debug("boUtils-calculateScrapeMovement scrapeAngle: {0} distanceToBackup: {1}".format(scrapeAngle,distanceToBackup))

  scrape_moves = []
  scrape_moves.append((TURN,scrapeAngle))
  scrape_moves.append((BACKWARD,distanceToBackup))
  scrape_moves.append((TURN,-scrapeAngle))

  # Distance back is distanceTraveled * sinOfAngle

  # Found it's better to not move back to the starting postion for now...
  # We're oriented in correct direction so staying back allows time
  # for sensors to get re-oriented
  #directionBack = round(distanceToBackup * degreesCos(abs(scrapeAngle)),2)
  #scrape_moves.append((FORWARD, directionBack))
  return scrape_moves


# ----------------------------------------------------------------------
# Calculate how long it will take to travel a given distance at a
# given speed
def calculateTimeToDistance(distance, speed):
  if speed > 0.001:
    logging.debug("boUtils-calculateTimeToDistance, distance: {0} speed: {1} time: {2}".format(distance,speed,round(distance/speed,2)))
    return round(distance/speed,2)
  else:
    logging.debug("boUtils-calculateTimeToDistance, distance: {0} speed: {1} time: {2}".format(distance,speed,"Infinity"))
    return float("inf")


# ----------------------------------------------------------------------
# Helper to return cosine of degree angle.
def degreesCos(theDegrees):
  return math.cos(math.radians(theDegrees))


# ----------------------------------------------------------------------
# Helper to return cosine of degree angle.
def degreesSin(theDegrees):
  return math.sin(math.radians(theDegrees))


# ----------------------------------------------------------------------
# Returns the minimum degrees to get from 'fromPosition' to
# 'toPosition'; If it's a negative angle of rotation (to the
# right) it's represented by a negative number
def getMinDegrees(fromPosition, toPosition):
  # Get the possible angles (left and right (right always negative))
  # and return the smaller of the two (ignoring sign).
  possibleAngles = calculateDegrees(fromPosition, toPosition)
  if (possibleAngles[0] > (-possibleAngles[1])):
    return possibleAngles[1]
  else:
    return possibleAngles[0]


# ----------------------------------------------------------------------
# Returns what the new orientation (your angle) would be after
# the turn is applied
def getNewOrientation(existingOrientation, amountTurned):
  if amountTurned < 0:
    # Turned to right
    return (360+existingOrientation+amountTurned)%360
  else:
    return (existingOrientation+amountTurned)%360


# ----------------------------------------------------------------------
# Determine what your new position would be after processing the
# movements passed in.  (The currentPosition is a tuple (x, y, angle)
def whatsNewPositionAfterMovements(currentPosition, movements):
  holdPosition = currentPosition
  for theMovement in movements:
    holdPosition = whatsNewPositionAfterMovement(holdPosition,theMovement)
  return holdPosition


# ----------------------------------------------------------------------
# Determine what your new position would be after processing the
# movement passed in.  (The currentPosition is a tuple (x, y, angle)
# the movement is also a tuple (i.e. ("F",32.0)
def whatsNewPositionAfterMovement(currentPosition, theMovement):
  # Can't modify tuple so work with a list and convert back at end
  newPosition = list(currentPosition)
  if theMovement[MOVEMENT_TYPE] == TURN:
    newPosition[POS_OF_ANGLE] = getNewOrientation(newPosition[POS_OF_ANGLE],theMovement[MOVEMENT_VALUE])
  elif theMovement[MOVEMENT_TYPE] == FORWARD:
    # x position is distance*cos(angle)
    newPosition[POS_OF_X] = round(newPosition[POS_OF_X] + theMovement[MOVEMENT_VALUE]*degreesCos(newPosition[POS_OF_ANGLE]),2)
    newPosition[POS_OF_Y] = round(newPosition[POS_OF_Y] + theMovement[POS_OF_Y]*degreesSin(newPosition[POS_OF_ANGLE]),2)
  elif theMovement[MOVEMENT_TYPE] == BACKWARD:
    # x position is distance*cos(angle)
    newPosition[POS_OF_X] = round(newPosition[POS_OF_X] - theMovement[MOVEMENT_VALUE]*degreesCos(newPosition[POS_OF_ANGLE]),2)
    newPosition[POS_OF_Y] = round(newPosition[POS_OF_Y] - theMovement[MOVEMENT_VALUE]*degreesSin(newPosition[POS_OF_ANGLE]),2)
  return tuple(newPosition)  