


Logic for obstacle:
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

When moving:
  If rightSensor triggered and not left one 
    " We're against right wall
    positionToTry = LEFT
    SCRAPE = true

If leftSensor triggered and not right one
  " We're against right wall
  positionToTry = RIGHT
  SCRAPE = true

if both sensors triggered
  OBSTACLE = true