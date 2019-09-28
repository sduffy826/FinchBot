# Description
This repo has code/artifacts I developed as I was working with the finch robot.
The end goal of my code was to have the finch successfully navigate from a given
starting point to and ending point, and be able to handle obstacles found along
the way.  
The 'important' code is describe below, there's a lot of other stuff in the repo.
That code was for testing/poc work; only included as might be useful down the
road :)

# Some design notes on movement
The philosphy is to have a stack that represents the target position you want to get to.  We also
have a list that keeps track of the robot positions.  The last element in the list reflects the
current robot position.
Pseudo is:
  - ATTEMPTS = 0
  - DIRECTION2TRY = LEFT
  - while stack of target 
    - pull TARGET off stack    
    - get CURRENTPOS (last item in robot positions)
    - calculate movements to get from CURRENTPOS to TARGET, it returns a list of movements to make
    - CONTINUEMOVEMENTS <-- True
    - ATTEMPTS ++ 
    - while movements to make and CONTINUEMOVEMENTS
      - make movement
      - if failed making movement
        - CONTINUEMOVEMENTS <- False
        - if failed because brushing against up against obstacle
          - backup, turn a little away from obstacle
        - elseIf obstacle straight ahead of you
          - try position 1/2 your width in direction of DIRECTION2TRY if you
            are at wall there or outside boundry
              DIRECTION2TRY <- !DIRECTION2TRY
      - log your current position
    - if CONTINUEMOVMENTS == False:
      - push TARGET back on stack
      - if ATTEMPTS >= SOMETHRESHOLD (maybe (2*obstacleWidth/(.5 robotWidth)))
          FAILED, tried every combination
    - else
      - ATTEMPTS = 0


# Code
| Code | Description |
| --------------- | ------------------------------- |
| pythonUtils.py | Various utilities to help (i.e. isFloat()) |
| botUtils.py | Common robot utilities (calculate movements, angles, etc..) |
| finchClass.py | Class to encapsulate the finch robot, has methods for movement, status ... |
| finchConstants.py | Various constants to support finch, typically update this after analysis on finch (from readFinchLog.py) |
| finchLog.py | Utility to log finch characteristics, mainly used for determining velocity and deviation off a straight line.  Use this program to calculate how the robot performs at different speeds, it writes the output to a file that can be processed by the program below |
| readFinchLog.py | Reads the log files created by finchLog.py and generates csv for analysis.  You need this to determine wheel speed/deviation during movement |
| finchMazeTest.py | Program to test the movements calculated to get to target locations.  It outputs the movements it'd make to console |
| finchMaze.py | The program to move finch thru a maze; the program has stack of target points to move thru, it handles obstacles etc.. |


## Logic for obstacle
```
  We keep track of the positionToTry (i.e. positionToTry = LEFT)
  We know our width (BOTWIDTH)
  We have different obstacles types (SCRAPE, OBSTACLE)
  If we have a scrap we:
    backup 1/2 BOTLENGTH
    turn SCRAPEDEGREES away from wall
    calculate new position
    recalculate path to target and proceed as normal
  If we have obstacle:
    while haveObstacle and LOST == false:
        triedAllAvailablesPositions = 0
        rotate opposite position to try by 20 degrees
        determine how much we need to backup
        oppositeLen = 1/2 BOTWIDTH
        hypotenuseLen = oppositeLen / sin(20)
        adjacentLen = oppositeLen / tan(20)
        move in reverse hypotenuseLen
        if feelObstacle during backup 
            # Reset values for movement
            hypotenuseLen = lenYouActuallyTravelled
            oppositeLen = hypotenuseLen * sin(20)
            adjacentLen = oppositeLen / tan(20)
            triedAllAvailablePositions ++
            if triedAllAvailbePositions == 2:
            LOST 
        rotate 20 degrees toward position
        moveForward adjacentLen
        calculate new position
        haveObstacle <- obstacle status
```
## When moving
```
  If rightSensor triggered and not left one 
    " We're against right wall
    positionToTry = LEFT
    SCRAPE = true

If leftSensor triggered and not right one
  " We're against left wall
  positionToTry = RIGHT
  SCRAPE = true

if both sensors triggered
  OBSTACLE = true
```  