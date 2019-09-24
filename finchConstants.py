# CONSTANTS for the finch robot, these can be derived from testing (see finchLog)
LEFTPOLARITY=1.0
RIGHTPOLARITY=1.0

LEFTWHEELADJUSTMENT=0.024
RIGHTWHEELADJUSTMENT=0.0

LEFTROTATIONSPEED=0.3
LEFTROTATIONTIME=4.3

RIGHTROTATIONSPEED=0.3
RIGHTROTATIONTIME=4.3

SLOWSPEED=0.4
MEDIUMSPEED=0.7
FASTSPEED=0.9
TOPSPEED=1.0

SPEEDINCREMENT=0.1

MEASUREMENTTYPE="US"
TOTALLENGTH=7.0
TOTALWIDTH=5.5
AXLETOFRONT=2.75
AXLETOREAR=TOTALLENGTH-AXLETOFRONT
WHEELBASE=3.5

RIGHTMAXSPEED=TOPSPEED-LEFTWHEELADJUSTMENT
LEFTMAXSPEED=TOPSPEED-RIGHTWHEELADJUSTMENT