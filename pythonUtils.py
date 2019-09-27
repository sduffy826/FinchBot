
import logging
import datetime

from getkey import getkey, keys

# Prompt for a key from the user
def input_char(message):
  print(message)
  return getkey()

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

# Convert the tuple (or list) into a string of values
def convertTupleToString(tupleVar):
  theString = ""
  for aValue in tupleVar:
    theString += ", " + str(aValue)
  if type(tupleVar) is list: 
    return "["+theString.lstrip(", ")+"]"      
  else:
    return "("+theString.lstrip(", ")+")"      

# Return a logger instance, caller passes in the logger name, level for console, level
# for file, and forceCreate (all parms are optional); note if logger exists and forceCreate
# is not True then the existing logger is returned.
def getCustomLogger(loggerName="seansLogger",consoleLevel=logging.INFO,fileLevel=logging.DEBUG,forceCreate=False):
  # create logger
  logger = logging.getLogger(loggerName)

  # If logger already has handles it was previously defined, If the forceCreate is off then just return the 
  # logger, if it's on then close the existing handlers... we'll redefine below.
  shallowCopyOfHandlers = logger.handlers[:]
  if len(shallowCopyOfHandlers) > 0:
    if forceCreate == False:
      return logger
    else:
      for handler in shallowCopyOfHandlers:
        handler.close()
        logger.removeHandler(handler)

  logger.setLevel(logging.DEBUG)

  # create formatter
  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

  # create console handler and set level to information
  ch = logging.StreamHandler()
  ch.setLevel(consoleLevel)
  # add formatter to ch
  ch.setFormatter(formatter)
  # add ch to logger
  logger.addHandler(ch)

  # create file handler which logs even debug messages, set formatter and add handler to logger
  fh = logging.FileHandler(loggerName+"_{0}.log".format(datetime.datetime.now().isoformat().replace(".",":")))
  fh.setLevel(fileLevel)
  fh.setFormatter(formatter)
  logger.addHandler(fh)
  return logger

