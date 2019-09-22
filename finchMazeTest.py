#import sys
#sys.path.append('../../../FinchPython120')

from finch import Finch 
import finchClass
import botUtils
import time 
from collections import deque
from getkey import getkey, keys

# This a stack, it has our current target location
targetPosition = deque()
targetPosition.append((72.0, 6, 0.0)) 

# This just tracks where we have been, we start at the origin
currentPosition = []
currentPosition.append((0.0,0,0,0.0))

while len(targetPosition) > 0:
  nextTarget = targetPosition.pop()

  positionOfCurrentPosition = len(currentPosition)-1
  currentPosition = currentPosition[positionOfCurrentPosition]
  
  # Calculate using the X axis as primary movement
  pathToUse = botUtils.calculateMovementToTarget(currentPosition,nextTarget,botUtils.X_PATH)
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

