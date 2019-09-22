from collections import deque
myStack = deque()

myStack.append('a')
myStack.append('b')
myStack.append('c')

myStack

try:
  print(myStack.pop(), len(myStack))
  print(myStack.pop(), len(myStack))
  print(myStack.pop(), len(myStack))
  print(myStack.pop(), len(myStack))
except:
  print("Exception raised")
finally:
  print("Finally got here")  