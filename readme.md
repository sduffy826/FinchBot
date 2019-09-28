# Description
This repo has code/artifacts I developed as I was working with the finch robot.  

The end goal of my work was to have the finch successfully navigate from a given starting point to and ending point; it needed to navigate obstacles and also be able to crash into them (depeneding on where it was).  It is basically to have the finch act as a bowling ball going down the ally that had bumpers on the side... it needed to avoid them, but also have the smarts to knock down the pins at the end.

The 'important' code is describe below, there's a lot of other stuff in the repo.  That code was for testing/poc work (and learning); it may be ugly... but I am learning python along my way :)

## Challenges/Difficulties
1. Finch
    1.1. Wheel speed is inconsistent 
    1.2. Surface friction impacts velocity
    1.3. Calculating turning angle
    1.4. Lack of sensors avaible - only sensor could use was obstacle
    1.5. Sensor consistency; got eratic results (flipping between True/False)
    1.6. Wheel polarity off (one wheel was going in reverse while other going forward)
2. Single sensor - obstacle
3. Localization
4. Obstacles
5. Target
    5.1 Consideration to think about with our target
    5.2 How do you represent it
    5.3 What path do you use to get to target, and how do you break that down into instruction for the robot
    5.4 What's the algorithm to move to the target and how does it account for obstacles
5. My knowledge
6. Time

## Disclaimer
Like any coding project, it's never 100%; it can always be improved.  Given that project is due and future 'finch' developement won't yield much value (I don't own
a finch) I am stopping the 'finch' specific code.  I may continue on the 'general/utility' code, but my finch game has reached it's 10th and final frame :)

<ol>
  <li>List 1</li>
  <li>List 2</li>
  <ol>
    <li>sublist</li>
    <li>sublist2</li>
  </ol>
</ol>

## Addressing Challenges Above
1. Finch
    1.1 Analyze performance - wrote programs: **finchLog.py** to gather finch sensors; program **readFinchLog.py** reads log (or all log) files and outputs a .csv file.  The csv was brought into spreadsheet to analyze, look at the **LogResults*** file for examples.  The analysis allowed me to define entries in the **finchConstants.py** file to compensate for velocities in the wheels (i.e. had to have one wheel velocity at 0.324 and the other at 0.30 in order for finch to go in a straight line). Also derived trivial algorithm (in **finchConstants.py** (getDistancePerSecond)) to determine distance traveled per second at any given wheel velocity 
    1.2 Used analysis at 1.1 to determine velocity, updated single value in **finchConstants.py** 
    1.3 Used **finchLog.py** determine time to rotate 360 degrees left or 360 degrees right; created constant for each in **finchConstants.py**  Note: later wrote **finchSensorTest.py** to test sensors; look at both
    1.4 For this project the temp and light sensors were unavailable (temp not meaningufl and couldn't use light (wasn't allowed to use a flashlight), so the only sensors available were the accelaration and obstacle sensors.  The acceleration didn't report any consistent tap/shake readings so I was left with obstacle sensor (infrared).  
    1.5 While moving I was continually checking the obstacle sensors.  I kept a list of the last 5 sensor readings and used the average of those readings to determine the state of the sensor.  I also defined an constant (finchClass-OBSTACLE_READING_DELAY (set to .01 seconds)) to wait before setting the current obstacle state (strored in a dictionary struction)
    1.6 I defined a constants (LEFTPOLARITY, RIGHTPOLARITY) to represent polarity adjustment; if one wheel is going in the wrong direction set it's value to -1.0.  Method finchClass-wheelHelper uses this (and wheelAdjustment) to calculate wheel values.

2. Single sensor - This posed many challenges
    - It could not be used for localization; to get around this I kept track of my current position based on my last position (x, y), the angle of trajectory and using my time and wheel velocity I derived where I should be; I say 'should be' because of the finches limitations this is not accurate.
    - Sensor inaccuracy - part of this described in 1.5; to get around false positives I also implemented a constant (finchClass-OBSTACLE_PERSIST_TIME_REQUIRED) so that I only reported the obstacle state if it persisted for a given amount of time (originally 0.1 secs)
    - Sensor is positioned 1.5 inches in from the edge of the robot so there could be obstacle in front of the finch that it doesn't report.  IMO the finch would be better having the sensors out at it's edge (and another in center).  In terms of me solutioning this, I was thinking of having the finch 'LookAround' before moving... it could rotate left N', take an obstacle reading, do the same by checking in front, then checking to the right N'.  If an obstacle isn't reported then it could proceed.  I was going to implement this but suspect it would make movements very slow.... it could only move forward the distance of 'sensativity' (which is limited (i.e. inches)), have to stop take new readings and move again.

3. Localization - The single sensor couldn't assist with localization (obstacles could be anywhere).  I developed code to keep track of my current position, it's represented internally as a tuple with (xPosition, yPosition, orientation (it's angle in degrees)).  I also have a tuple that repsents the **robots world** (it's bounds).. more on later. I wrote code that calculates my new position based my trajectory, time traveled and wheel speed.  There's quite a bit of code that managers this and instead of going into details take a look at the code in **botUtils.py**   fyi: It's in 'botUtils.py' since that's 'common' robot utilities, it's not related to a finch.

4. Obstacles - Trying to figure out what to do when you hit an obstacle is challenging, the tail of the finch is long so if you're up against an obstacle on your right you're unable to turn left (the tail will hit obstacle).  With the shape of the finch you can however turn toward the obstacle and then backup.  This is what I did.  I also coded for two different types of obstacles... if only one obstacle sensor went off then I believed the finch was scraping an obstacle; it would reposition itself and turn a small angle away from it.  If both sensors triggered I would backup, move a toward a given DIRECTION for a given SPACE.  For DIRECTION - I take my current position and the **robots world** and see if I am against the edge of my world... if I am I set my direction accordingly.  For SPACE I originally calculated that as 1/2 my robot's width but changed it to be the width of the robot.  Overall it performed good but more could be done; see last bullet under **Single sensor**.

5. Target
    5.1 Considerations - Our target is basically an x,y position that we want to get to, and an orientation to be at once there.  We also want to knock things over so we might want to change the speed and how the robot reacts to it sensors as we move.  Instead of having one target it's probably good to think of it as a sequence of targets; this way we can change how the robot acts during it's journey.  I also noticed that the robot moves differently across the floor depending on where it is.. the tiles aren't even.
    5.2 Representation - I use a tuple to represent an individual target location, format (x,y,orientation,speedToGetThere,ignoreObstacles).  I use a stack in the code that has a list of target locations
    5.3 Calculation To - My solution considered three different 'path types' (ways) to get from current position to a target location... it could be X oriented (get to x pos first), Y oriented (get to y pos) or DIRECT (a straight line).  I wrote a generic routine (botUtils.calculateMovementToTarget) it uses the 'path type' (as an argument) to return a LIST of MOVEMENTS required to get from 'currentPosition' to 'targetPosition'.  Each movement is a TYPE, VALUE, the types are: FORWARD, BACKWARD or TURN and the values are scalars. (i.e. ("FORWARD",10),("TURN",45) means move forward for a distance of 10, then turn 45 degrees)
    5.4 Algorithm - The program starts with a stack of target positions.  I tried describing this in a paragraph but it wasn't clear, psuedo is probably the easiest:
    ```
          while stackOfTargets isnt empty
             CURRENTTARGET <- stackOfTargets.pop()
             listOfMovements <- calculateMovementsToTarget(CURRENTPOSITION, CURRENTTARGET, 'path type')
             SUCCESS <- True
             while listOfMovements isnt empty
               makeAMovement
               if hitAnObstacle 
                 SUCCESS <- False
                 clear listOfMovements 
                 listOfMovements <- newMovmentsToAvoidObstacle    // See 'Obstacle' above 
             if SUCCESS == False
               stackOfTargets.push(CURRENTTARGET)  // We didn't get to target, we hit an obstacle, push it back onto stack to retry
```
6. My knowledge - If I remembered 1/2 of what I've forgotten (linear algebra, geometry etc..) I'd be a genius :)  I am also a python newbie so that added it's own set of challenges.

7. Time - Common issue on any software project; software can always be improved; but time is limited, eventually you have to settle with 'doing your best' in the time allotted.  This task project was no different :)

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