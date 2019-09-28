import threading
from queue import Queue 
import pythonUtils
from time import sleep

queueForCommunication = Queue()

# A function that gets the keyboard input and puts it onto the queue passed in
def keyProducer(outputQueue, keepRunning): 
  while keepRunning(): 
    keyPressed = pythonUtils.input_char("In thread, hit a key, 'q' to quit")
    outputQueue.put(keyPressed)
  print("Thread stopped")
          
# Create thread
continuePromptForKey = True
threadForKey         = threading.Thread(target = keyProducer, args =(queueForCommunication, lambda: continuePromptForKey )) 
threadForKey.start() 

# For testing enter a loop that will continue for 'secondsToDelay' or the thread returned key telling us to stop
# Just using sleep as way to simulate some other action taking place
threadToldMeToStop = False
secondsToDelay     = 10
currentSecond      = 0
while currentSecond < secondsToDelay and threadToldMeToStop == False:
  print("Iteration count: {0} or {1}".format(currentSecond+1,secondsToDelay))
  # Since sleep is blocking I simulate 'real time' by only sleeping for .1 seconds before checking if the thread
  # put something on the queue
  for y in range(10):
    if queueForCommunication.empty() == False:
      keyFromThread = queueForCommunication.get(False)
      print("Got key: {0}".format(keyFromThread))  
      threadToldMeToStop = (keyFromThread == "q")
    sleep(0.1)
    print("  sleeping...")

if threadToldMeToStop:
  print("Thread told me to stop")
else:
  print("Stopped due to Timeout")

print("\n\nHit any key to terminate this program and the thread")
# Stop thread
continuePromptForKey = False
threadForKey.join()

          