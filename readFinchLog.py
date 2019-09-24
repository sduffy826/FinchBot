import sys
import os.path
import glob
import datetime
import pythonUtils

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
    # Strip whitespace, and remove parens (from tuples)
    aLine = aLine.strip().strip("()")
    recCount += 1
    if DEBUGIT:
      print("Line read:", aLine)
    if recCount == 1:
      listOfLines = aLine.strip().split("Shake")
      if len(listOfLines) > 0 and DEBUGIT:
        print("Split header: ",aLine.strip())

      theList.append(listOfLines[0]+"Shake")
      currPos = 1
      while currPos < len(listOfLines):
        theList.append(listOfLines[currPos])
        currPos += 1
    elif len(aLine) > 0:
      theList.append(aLine)
      lastLine = aLine

  lastLineArray = lastLine.split(",")    
  if DEBUGIT:
    print("lastLine:{0}: arraySize:{1}:".format(lastLine,len(lastLineArray)))

  goodData = False
  if len(lastLineArray) == 3: 
    if DEBUGIT:
      print("lastLineArray[0]:{0}: lastLineArray[1]:{1}: lastLineArray[2]:{2}:".format(lastLineArray[0],
                                                                                       lastLineArray[1],lastLineArray[2]))
    if lastLineArray[0] == "'EOF'" and pythonUtils.isFloat(lastLineArray[1]) and pythonUtils.isFloat(lastLineArray[2]):
      totalDistance = float(lastLineArray[1])
      deviationOffAxis = float(lastLineArray[2])
      if (totalDistance > 0.0):
        goodData = True
      if DEBUGIT:
        print("totalDistance:{0}: deviationOffAxis:{1}: goodData:{2}".format(totalDistance,deviationOffAxis,goodData))
  else:
    if DEBUGIT:
      print("lastLineArray len not 3, it's:{0}:".format(len(lastLineArray)))

  if goodData == False:
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