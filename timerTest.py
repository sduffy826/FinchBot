import time
from time import sleep

startTime = time.time()
sleep(0.5) # 1/2 second

endTime = time.time()
print("Started at", time.ctime(startTime)," Ended at", time.ctime(endTime), "Elapsed seconds: ", round(endTime-startTime,4))
print(time.ctime(startTime).split()[3],"->",time.ctime(endTime).split()[3])
