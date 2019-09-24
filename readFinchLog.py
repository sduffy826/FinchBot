# This reads the logfile(s) created by the 'finchLog.py' program.
# The original version of this was much more complicated than
# what is is now (mainly cause the way the records were written).
# See the older version in git around 9/24/2019 to look at it.

import sys
import os.path
import glob
import datetime
import pythonUtils
import math

DEBUGIT = True

if len(sys.argv) < 2:
  print("You should pass in the logFile to read")
  exit(99)

def getLogFile():
  some_datetime_obj = datetime.datetime.now()  # Store current datetime
  datetime_str = some_datetime_obj.isoformat()  # Convert to ISO 8601 string
  return "LogResults." + datetime_str + ".csv"


# Read the log file passed in, return a list of it's records
# if the data is valid (ie got a valid last record)
def readLogFile(inputFile):
  if DEBUGIT:
    print("\n\nProcessing: {0}".format(inputFile))

  # Read file
  with open(inputFile,"r") as fileHandle:
    lines = fileHandle.readlines()

  theList = []
  
  # First check if no newline on header record"
  recCount = 0
  lastLine = ''
  for aLine in lines:
    # Strip whitespace
    aLine = aLine.strip()
    recCount += 1
    if DEBUGIT:
      print("Line read:", aLine)
    
    if len(aLine) > 0:
      theList.append(aLine)
      lastLine = aLine

  lastLineArray = lastLine.split(",")    
  if DEBUGIT:
    print("lastLine:{0}: arraySize:{1}:".format(lastLine,len(lastLineArray)))

  goodData = False
  # Get the speed, it's the min of the two wheels (cause of adjustments)
  theFinalSpeed = 0.0
  rec2Check = len(theList) - 2
  if rec2Check >= 0:
    dumList = theList[rec2Check].split(",")
    lWheel  = dumList[2]
    rWheel  = dumList[3]
    if pythonUtils.isFloat(lWheel) and pythonUtils.isFloat(rWheel):
      theFinalSpeed = min(lWheel, rWheel)
      goodData = True
      
  # Check the last line and calculate real distance and velocity
  if len(lastLineArray) > 3 and goodData: 
    goodData = False
    if DEBUGIT:
      idx = 0
      outString = ""
      for lastLineElement in lastLineArray:
        idx += 1
        outString += " lastLineArray[{0}]: {1}".format(idx,lastLineElement)
      print(outString.lstrip())

    if lastLineArray[0] == "EOF" and pythonUtils.isFloat(lastLineArray[2]) and pythonUtils.isFloat(lastLineArray[6]):
      xDistance        = float(lastLineArray[2])
      elapsedTime      = float(lastLineArray[4])
      deviationOffAxis = float(lastLineArray[6])
      
      if (xDistance > 0.0) and elapsedTime > 0.0:
        goodData = True
        calculatedDistance = math.sqrt(xDistance*xDistance + deviationOffAxis*deviationOffAxis)
        velocity = calculatedDistance / elapsedTime
        summaryRecord = "SUMMARY,xDistance,{0},yDistance,{1},totDistance,{2},elapsedTime,{3},wheelSpeed,{4},velocity,{5}".format(
                            xDistance,deviationOffAxis,calculatedDistance,elapsedTime,theFinalSpeed,velocity)
        if DEBUGIT:
          print("\n\n"+summaryRecord+"\n\n")
        theList.append(summaryRecord)

      if DEBUGIT and goodData == False:
        print("totalDistance:{0:.2f}: elapsedTime:{1:.2f} deviationOffAxis:{2:.2f}: goodData:{3}".format(xDistance,
                                                                                     elapsedTime,deviationOffAxis,goodData))
  else:
    if DEBUGIT:
      print("lastLineArray array len < 3, it's:{0}:".format(len(lastLineArray)))

  if goodData == False and len(theList) > 0:
    print("Clearing list")
    theList.clear()

  return theList

# ----------------------------------------------------------------------
# Start of mainline
# ----------------------------------------------------------------------
firstArgument = sys.argv[1]
isADirectory  = False
isAFile       = False
if os.path.isdir(firstArgument):
  isADirectory = True
elif os.path.isfile(firstArgument):
  isAFile = True

listOfFiles2Process = []
if isADirectory:
  if firstArgument[-1] != "/":
    firstArgument += "/"
  fileList = glob.glob(firstArgument+"LogFile.*")
  for aFile in fileList:
    listOfFiles2Process.append(aFile)
else:
  listOfFiles2Process.append(firstArgument)

outputFile = getLogFile()
outHandle = open(outputFile,"at") # Append and text file
for aFile in listOfFiles2Process:
  print("Would now process: {0}".format(aFile))
  rtnList = readLogFile(aFile)
  if len(rtnList) > 0:    
    print("  File can be processed")
    lineCount = 0
    for aRecordInFile in rtnList:
      lineCount += 1
      outHandle.write(aFile+","+str(lineCount)+","+aRecordInFile+"\n")
  else:
    print("  File is invalid")

outHandle.close()

  #tempTuple = tuple(aLine.strip())
  #print(str(tempTuple))

  #aTuple = tempTuple[1]
  #aTuple = aLine.strip()
  #print(str(aTuple))
  # time
  #print(tempTuple[0])
  # Wheels
  #print(str(aTuple[0]))
  # Temp: 
  #print(str(aTuple[1]))
  # Lights
  #print(str(aTuple[2]))
  # Obstacles
  #print(str(aTuple[3]))
  # Accelerator 
  #print(str(aTuple[4]))
  #print("\n")