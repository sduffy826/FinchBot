import sys

if len(sys.argv) < 2:
  print("You should pass in the logFile to read")

inputFile = sys.argv[1]

with open(inputFile,"r") as fileHandle:
  lines = fileHandle.readlines()

theList = []
for aLine in lines:
  print("Line read:", aLine)
  tempTuple = tuple(aLine.strip())
  print(str(tempTuple))

  aTuple = tempTuple[1]
  #aTuple = aLine.strip()
  #print(str(aTuple))
  # time
  print(tempTuple[0])
  # Wheels
  print(str(aTuple[0]))
  # Temp: 
  print(str(aTuple[1]))
  # Lights
  print(str(aTuple[2]))
  # Obstacles
  print(str(aTuple[3]))
  # Accelerator 
  print(str(aTuple[4]))
  print("\n")