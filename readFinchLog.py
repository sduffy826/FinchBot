import sys

stripLeadingTrailingParens = True

if len(sys.argv) < 2:
  print("You should pass in the logFile to read")

inputFile = sys.argv[1]

with open(inputFile,"r") as fileHandle:
  lines = fileHandle.readlines()

theList = []
" First check if no newline on header record"
recCount = 0
for aLine in lines:
  recCount += 1
  print("Line read:", aLine)
  if recCount == 1:
    listOfLines = aLine.strip().split("Shake")
    if len(listOfLines) > 0:
      print("Split header: ",aLine.strip())
    theList.append(listOfLines[0]+"Shake")
    currPos = 1
    while currPos < len(listOfLines):
      theList.append(listOfLines[currPos])
      currPos += 1
  else:
    theList.append(aLine.strip())
  
for aLine in theList:
  print(aLine)  









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