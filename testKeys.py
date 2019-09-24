import time 
from getkey import getkey, keys

def input_char(message):
  print(message)
  return getkey()

ans = "l"
while ans != 'q':
  ans = input_char("j-left, k-right, i-increase, l-stop, u-topspeed, spacebar-topspeed, a-left90, s-right90")
  print("Response", ans)