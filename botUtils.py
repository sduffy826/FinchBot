import math

FORWARD = "F"
TURN = "T"
X_PATH = "X"
Y_PATH = "Y"
DIRECT_PATH = "S"

# Helper to return cosine of degree angle.
def degreesCos(theDegrees):
  return math.cos(math.radians(theDegrees))

# Helper to return cosine of degree angle.
def degreesSin(theDegrees):
  return math.sin(math.radians(theDegrees))

# Calculate the number of degrees you need to turn left or right
# in order to get oriented to the desired angle.  It will
# return a tuple (leftDegrees, rightDegrees).  fyi: Right degrees
# are always negative (angles of rotation).
def calculateDegrees(fromPosition, toPosition):
  toPositionNegativeRotation = -(360.0 - toPosition)
  degreesRight = ( fromPosition - toPositionNegativeRotation ) % 360
  degreesLeft  = ((toPosition + 360) - fromPosition) % 360
  return (degreesLeft, -degreesRight)

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

def getNewOrientation(existingOrientation, amountTurned):
  if amountTurned < 0:
    # Turned to right
    return (360+existingOrientation+amountTurned)%360
  else:
    return (existingOrientation+amountTurned)%360

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
  print("In calculateMovementToTarget, curr:{0} targ:{1} path:{2}".format(str(currentPosition),
                                                                          str(targetPosition),path2Use))
  if path2Use == X_PATH:
    return calculateMovementToTargetUsingXAxis(currentPosition, targetPosition)
  elif path2Use == Y_PATH:
    print("Implement Y_PATH")
  elif path2Use == DIRECT_PATH:
    print("Implement DIRECT_PATH")
  else:
    print("Invalid path of {0}".format(path2Use))
  return []

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
  
  deltaAngle = getMinDegrees(startAngle,targetAngle)
  # If angle needs to be changed then log the movememtn
  if deltaAngle != 0.0:
    x_moves.append((TURN,deltaAngle))
  if xUnits != 0:
    x_moves.append((FORWARD,xUnits))
  return x_moves

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
  
  deltaAngle = getMinDegrees(startAngle,targetAngle)
  # If angle needs to be changed then log the movememtn
  if deltaAngle != 0.0:
    y_moves.append((TURN,deltaAngle))
  if yUnits != 0:
    y_moves.append((FORWARD,yUnits))
  return y_moves

def calculateMovementToTargetUsingXAxis(currentPos, targetPos):  
  # Get the movements necessary to get to the target x position, we pass in the
  # current x position, current angle and the desired x position
  xMovements = calculatePerpendicularMovementToX(currentPos[0], currentPos[2], targetPos[0])

  # We have the movements necessary to get there... determine what your new position
  # would be after it.. need that for determining next set of movements.
  tempPos = whatsNewPositionAfterMovements(currentPos, xMovements)

  yMovements = calculatePerpendicularMovementToY(tempPos[1],tempPos[2],targetPos[1])

  # Return the two lists concatenated together.
  return xMovements+yMovements

def calculateMovementToTargetUsingYAxis(currentPos, targetPos):  
  # This is similar to calculateMovementToTargetUsingXAxis except it moves along the Y
  # axis first.
  yMovements = calculatePerpendicularMovementToY(currentPos[1],currentPos[2],targetPos[1])
  # Get new position
  tempPos = whatsNewPositionAfterMovements(currentPos, yMovements)
  # Get xMovements
  xMovements = calculatePerpendicularMovementToX(tempPos[0], tempPos[2], targetPos[0])

  # Return the two lists concatenated together.
  return yMovements+xMovements


# Determine what your new position would be after processing the
# movements passed in.  (The currentPosition is a tuple (x, y, angle)
def whatsNewPositionAfterMovements(currentPosition, movements):
  # Can't modify tuple so work with a list and convert back at end
  newPosition = list(currentPosition)
  for theMovement in movements:
    if theMovement[0] == TURN:
      newPosition[2] = getNewOrientation(newPosition[2],theMovement[1])
    elif theMovement[0] == FORWARD:
      # x position is distance*cos(angle)
      newPosition[0] = newPosition[0] + theMovement[1]*degreesCos(newPosition[2])
      newPosition[1] = newPosition[1] + theMovement[1]*degreesSin(newPosition[2])
  return tuple(newPosition)


def oldCalculateMovementToTargetUsingXAxis(currentPos, targetPos):
  moves = []
  xUnits = targetPos[0] - currentPos[0]
  yUnits = targetPos[1] - currentPos[1]

  # Set angle to turn in X direction and move that many units
  # (fyi: we pass xUnits which may be negative because it's also
  # needed to calculate the current position)
  if xUnits < 0:
    xTargetAngle = 180
  else:
    xTargetAngle = 0
  deltaAngle = getMinDegrees(currentPos[2],xTargetAngle)

  if deltaAngle != 0:
    # Orient to new angle
    moves.append((TURN,deltaAngle)) 
  
  if xUnits != 0:
    moves.append((FORWARD,xUnits))

  # Calculate how to move in the y direction, similar to above
  if yUnits < 0: 
    targetAngle = 270
  else:
    targetAngle = 90
  
  deltaAngle = getMinDegrees(xTargetAngle,targetAngle)
  moves.append((TURN,deltaAngle))
  if yUnits != 0:
    moves.append((FORWARD,yUnits))
  return moves