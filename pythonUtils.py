
# Check if argument is a valid floating point number
def isFloat(checkThis, debugIt=False):
  try:
    float(checkThis)
    if debugIt:
      print("isFloat({0}) returned:{1}".format(checkThis,True))
    return True
  except ValueError:
    if debugIt:
      print("isFloat({0}) returned:{1}".format(checkThis,False))
    return False