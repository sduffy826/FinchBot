import time
def writeFile(fileName):
    fileHandle = open(fileName,"at") # Append and text file
    theList = []
    someTuple = (123, 456, 1.234)
    theList.append(someTuple)

    someTuple2 = (4, 3, "ABC", 3.1)
    theList.append(someTuple2)

    for anItem in theList:
        fileHandle.write(str(anItem))
        fileHandle.write('\n')
        print("Just wrote:", str(anItem))
    
    fileHandle.close()

def readFile(fileName):
    with open(fileName,"r") as fileHandle:
        lines = fileHandle.readlines()

    print("Read: ", len(lines), "lines")

    theList = []
    for aLine in lines:
        aTuple = tuple(aLine.strip())
        theList.append(aTuple)
        print(aLine.strip())
    print("Size of theList is: ", len(theList))

start = time.time()
writeFile("foo.txt")
print("Done with writing file")
end = time.time()
readFile("foo.txt")
print("Elapsed (and a print): ", round(end-start,4))
