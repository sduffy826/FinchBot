#import sys
#sys.path.append('../../../FinchPython120')

from finch import Finch 
import time 
import curses

class MyRobot:

  def __init__(self, left, right):
    self.leftWheel = left
    self.rightWheel = right
    self.finch = Finch()
 
  def update(self):
    self.finch.wheels(self.leftWheel, self.rightWheel)

  def stop(self):
    self.leftWheel = 0.0
    self.rightWheel = 0.0
    self.update()

  def left(self):
    if self.rightWheel >= 1.0:
      self.leftWheel -= 0.1
    else:
      self.rightWheel += 0.1
    self.update()

  def right(self):
    if self.leftWheel >= 1.0:
      self.rightWheel -= 0.1
    else:
      self.leftWheel += 0.1
    self.update()

  def run(self):
    self.leftWheel = 1.0
    self.rightWheel = 1.0
    self.update()

  def shutDown(self):
    self.finch.close()
  
# ------------------------------------------------------
# Routine to prompt for a single character from the user   
def input_char(message):
  try:
    win = curses.initscr()
    # win.addstr(0, 0, message)
    curses.echo()
    while True:
      ch = win.getch()
      #if ch in range(32, 127):
      break
      # time.sleep(0.05)
  except:
    raise
  finally:
    curses.endwin()
  return chr(ch)



myRobot = MyRobot(0.0, 0.0)

ans = "l"
while ans <> "q":
  ans = input_char("j-left, k-right, i-increase, l-stop, spacebar-topspeed")
  #time.sleep(1)
  print("Response", ans)
  time.sleep(0.5)

  if ans is "j":
    myRobot.left()
  elif ans is "k":
    myRobot.right()
  elif ans is "l":
    myRobot.stop()
  elif ans is "u":
    myRobot.run()

myRobot.shutDown()

time.sleep(1)
