# CONSTANTS for the finch robot, these can be derived from testing (see finchLog)

# Below is used in casd the polarity on the robot is off... you can change to -1.0
# if you want the wheel to go in the opposite direction
LEFTPOLARITY=1.0
RIGHTPOLARITY=1.0

# Amount to adjust wheel speed, this was done at speed 4.0... was going to make
# it a varying scale (i.e. velocity * .06) and add that but didn't need it
LEFTWHEELADJUSTMENT=0.024
RIGHTWHEELADJUSTMENT=0.0

# Turn speed/time for full 360 rotation... we need this so that we can accurately
# determine angles requested.
# Use the finchSensorTest.py program and test rotations if you want to verify time
LEFTROTATIONSPEED=0.3
LEFTROTATIONTIME=4.5

RIGHTROTATIONSPEED=0.3
RIGHTROTATIONTIME=4.5

# Constants for speed
SLOWSPEED=0.4
MEDIUMSPEED=0.7
FASTSPEED=0.9
TOPSPEED=1.0

# When encounter scrape (rub against object) use the speed/angle/distance
# to try and correct the issue
SCRAPESPEED=0.3
SCRAPEANGLE=10.0
SCRAPEBACKUPDISTANCE=3.0

# Var below used when incrementing speed of robot up/down
SPEEDINCREMENT=0.1

# Characteristics of the robot and scale of measurement (INches, CM etc), it
# doesn't really matter unless you start using different scales, in that case
# you need it for conversions
MEASUREMENTSCALE="IN"
TOTALLENGTH=7.0
TOTALWIDTH=5.5
AXLETOFRONT=2.75
AXLETOREAR=TOTALLENGTH-AXLETOFRONT
WHEELBASE=3.5
HALFMYWIDTH=round(TOTALWIDTH/2,2)

# Set max speed for each wheel (take into account wheel adjustments)
RIGHTMAXSPEED=TOPSPEED-LEFTWHEELADJUSTMENT
LEFTMAXSPEED=TOPSPEED-RIGHTWHEELADJUSTMENT

# Constants just to make code more readable :)
LEFT="L"
RIGHT="R"

# Constants for LED colors
RED="R"
GREEN="G"
BLUE="B"

# Function to return the speed of the wheel given a certain velocity,
# it's calculated since it vary's with this robot... different robots
# act differently :)  See the analysis spreadsheet to see how
# I came up with the 2.819 value and 11.91 (base at speed .4)
def getDistancePerSecond(wheelSpeed):
  # Commented value below was with first robot
  # return round(((((wheelSpeed-0.4)*2.819)+11.91)*wheelSpeed),2)
  return round(((((wheelSpeed-0.4)*3.64)+11.47)*wheelSpeed),2)