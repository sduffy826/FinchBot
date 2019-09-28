# Description
This repo has code/artifacts I developed as I was working with the finch robot.  

The end goal of my work was to have the finch successfully navigate from a given starting point to and ending point; it needed to navigate obstacles and also be able to crash into them (depending on where it was).  It is basically to have the finch act as a bowling ball going down the alley that had bumpers on the side... it needed to avoid them, but also have the smarts to knock down the pins at the end.

The 'important' code is described below, there's a lot of other stuff in the repo.  That code was for testing/poc work (and learning); it may be ugly... but I am learning python along my way :)

## Challenges/Difficulties
<ol>
<li>Finch
  <ol>
    <li>Wheel speed is inconsistent </li>
    <li>Surface friction impacts velocity</li>
    <li>Calculating turning angle</li>
    <li>Lack of sensors available - only sensor could use was obstacle</li>
    <li>Sensor consistency; got erratic results (flipping between True/False)</li>
    <li>Wheel polarity off (one wheel was going in reverse while other going forward)</li>
  </ol></li>
<li>Single sensor - obstacle</li>
<li>Localization</li>
<li>Obstacles</li>
<li>Target
  <ol>
    <li>Consideration to think about with our target</li>
    <li>How do you represent it</li>
    <li> What path do you use to get to target, and how do you break that down into instruction for the robot</li>
    <li> What's the algorithm to move to the target and how does it account for obstacles</li>
  </ol></li>
<li>My knowledge</li>
<li>Time</li>
</ol>

## Addressing Challenges Above
<ol>
<li>Finch
  <ol>
    <li>Wheel speed inconsistency: Analyze performance - wrote programs: <strong>finchLog.py</strong> to gather finch sensors; program <strong>readFinchLog.py</strong> reads log (or all log) files and outputs a .csv file.  The csv was brought into spreadsheet to analyze, look at the <strong>LogResults</strong>* file for examples.  The analysis allowed me to define entries in the <strong>finchConstants.py</strong> file to compensate for velocities in the wheels (i.e. had to have one wheel velocity at 0.324 and the other at 0.30 in order for finch to go in a straight line). Also derived trivial algorithm (in <strong>finchConstants.py</strong> (getDistancePerSecond)) to determine distance traveled per second at any given wheel velocity</li>
    <li>Surface friction: Used analysis at prior step to determine velocity, updated single value in <strong>finchConstants.py</strong> </li>
    <li>Calculate turning angle: Used <strong>finchLog.py</strong> determine time to rotate 360 degrees left or 360 degrees right; created constant for each in <strong>finchConstants.py</strong>  Note: later wrote <strong>finchSensorTest.py</strong> to test sensors; look at both</li>
    <li>Lack of sensors: For this project the temp and light sensors were unavailable (temp not meaningful and couldn't use light (wasn't allowed to use a flashlight), so the only sensors available were the acceleration and obstacle sensors.  The acceleration didn't report any consistent tap/shake readings, so I was left with obstacle sensor (infrared).</li>
    <li>Sensor consistency: While moving I continually checking the obstacle sensors.  I kept a list of the last 5 sensor readings and used the average of those readings to determine the state of the sensor.  I also defined a constant (finchClass-OBSTACLE_READING_DELAY (set to .01 seconds)) to wait before setting the current obstacle state (strored in a dictionary structure)</li>
    <li>Wheel polarity: I defined constants (LEFTPOLARITY, RIGHTPOLARITY) to represent polarity adjustment; if one wheel is going in the wrong direction set it's value to -1.0.  Method finchClass-wheelHelper uses this (and wheelAdjustment) to calculate wheel values.</li>
  </ol></li>
<li>Single sensor - This posed many challenges
  <ul>
    <li>It could not be used for localization; to get around this I kept track of my current position based on my last position (x, y), the angle of trajectory and using my time and wheel velocity I derived where I should be; I say 'should be' because of the finches limitations this is not accurate.</li>
    <li>Sensor inaccuracy - part of this described in 1.5; to get around false positives I also implemented a constant (finchClass-OBSTACLE_PERSIST_TIME_REQUIRED) so that I only reported the obstacle state if it persisted for a given amount of time (originally 0.1 secs)</li>
    <li>Sensor is positioned 1.5 inches in from the edge of the robot so there could be obstacle in front of the finch that it doesn't report.  IMO the finch would be better having the sensors out at its edge (and another in center).  In terms of me solutioning this, I was thinking of having the finch 'LookAround' before moving... it could rotate left N', take an obstacle reading, do the same by checking in front, then checking to the right N'.  If an obstacle isn't reported then it could proceed.  I was going to implement this but suspect it would make movements very slow.... it could only move forward the distance of 'sensitivity' (which is limited (i.e. inches)), have to stop take new readings and move again.</li>
  </ul></li>

<li>Localization - The single sensor couldn't assist with localization (obstacles could be anywhere).  I developed code to keep track of my current position, it's represented internally as a tuple with (xPosition, yPosition, orientation (it's angle in degrees)).  I also have a tuple that represents the <strong>robots world</strong> (it's bounds).. more on later. I wrote code that calculates my new position based my trajectory, time traveled and wheel speed.  There's quite a bit of code that managers this and instead of going into details take a look at the code in <strong>botUtils.py</strong>   fyi: It's in 'botUtils.py' since that's 'common' robot utilities, it's not related to a finch.</li>

<li>Obstacles - Trying to figure out what to do when you hit an obstacle is challenging, the tail of the finch is long so if you're up against an obstacle on your right you're unable to turn left (the tail will hit obstacle).  With the shape of the finch you can however turn toward the obstacle and then backup.  This is what I did.  I also coded for two different types of obstacles... if only one obstacle sensor went off then I believed the finch was scraping an obstacle; it would reposition itself and turn a small angle away from it.  If both sensors triggered I would backup, move a toward a given DIRECTION for a given SPACE.  For DIRECTION - I take my current position and the <strong>robots world</strong> and see if I am against the edge of my world... if I am; I set my direction accordingly.  For SPACE I originally calculated that as 1/2 my robot's width but changed it to be the width of the robot.  Overall it performed good but more could be done; see last bullet under <strong>Single sensor</strong>.</li>

<li>Target
  <ol>
    <li>Considerations: Our target is basically an x,y position that we want to get to, and an orientation to be at once there.  We also want to knock things over so we might want to change the speed and how the robot reacts to it sensors as we move.  Instead of having one target it's probably good to think of it as a sequence of targets; this way we can change how the robot acts during its journey.  I also noticed that the robot moves differently across the floor depending on where it is.. the tiles aren't even.</li>
    <li>Representation: I use a tuple to represent an individual target location, format (x,y,orientation,speedToGetThere,ignoreObstacles).  I use a stack in the code that has a list of target locations</li>
    <li>Calculation To: My solution considered three different 'path types' (ways) to get from current position to a target location... it could be X oriented (get to x pos first), Y oriented (get to y pos) or DIRECT (a straight line).  I wrote a generic routine (botUtils.calculateMovementToTarget) it uses the 'path type' (as an argument) to return a LIST of MOVEMENTS required to get from 'currentPosition' to 'targetPosition'.  Each movement is a TYPE, VALUE, the types are: FORWARD, BACKWARD or TURN and the values are scalars. (i.e. ("FORWARD",10),("TURN",45) means move forward for a distance of 10, then turn 45 degrees)</li>
    <li>Algorithm: The program starts with a stack of target positions.  I tried describing this in a paragraph, but it wasn't clear, psuedo is probably the easiest:
    <pre>
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
    </pre>
    </li>
  </ol></li>
<li>My knowledge - If I remembered 1/2 of what I've forgotten (linear algebra, geometry etc..) I'd be a genius :)  I am also a python newbie so that added its own set of challenges.</li>

<li>Time - Common issue on any software project; software can always be improved; but time is limited, eventually you have to settle with 'doing your best' in the time allotted.  This task project was no different :)</li>
</ol>


## Disclaimer
Like any coding project, it's never 100%; it can always be improved.  Given that project is due and future 'finch' development won't yield much value (I don't own
a finch) I am stopping the 'finch' specific code.  I may continue on the 'general/utility' code, but my finch game has reached its 10th and final frame :)


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
| finchSensorTest.py | Wrote this later to test sensors, follow on from logger... look at :) |