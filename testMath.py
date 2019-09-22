import math

def conversionTest():
  degrees = input("Enter degrees: ")
  print("{degrees:d} converted to radians is {radians:.2f}".format(degrees=degrees,radians=math.radians(degrees)))

  radians = input("Enter radians: ")
  print("{radians:.2f} converted to degrees is: {degrees:.2f}".format(radians=radians,degrees=math.degrees(radians)))

lastLocationX = 0
lastLocationY = 0

targetLocationX = 72
targetLocationY = 6

currentAngleInRadians = math.radians(45.0) 

velocityPerSecond = 2.0
numberOfSeconds = 0.0
secondInterval = .01
secondsToTravel = 1.0
while True:
  numberOfSeconds += secondInterval
  currentPositionX = velocityPerSecond * numberOfSeconds * math.cos(currentAngleInRadians) + lastLocationX
  currentPositionY = velocityPerSecond * numberOfSeconds * math.sin(currentAngleInRadians) + lastLocationY
  print("{seconds:.2f} seconds x: {x:.2f} y: {y:.2f}".format(seconds=numberOfSeconds,x=currentPositionX,y=currentPositionY))
  if (round(abs(numberOfSeconds-secondsToTravel),2) == 0):
    break