import pythonUtils
import logging

myLogger = pythonUtils.getCustomLogger("myLog",logging.INFO,logging.DEBUG)

# Put out messages 
myLogger.debug('1 debug message')
myLogger.info('1 info message')
myLogger.warning('1 warn message')
myLogger.error('1 error message')
myLogger.critical('1 critical message')

# Get another logger instance
ayLogger = pythonUtils.getCustomLogger("myLog",logging.INFO,logging.INFO)
ayLogger.info("2 Got another logger")
ayLogger.debug('2 debug message')
ayLogger.warning('2 warn message')
ayLogger.error('2 error message')
ayLogger.critical('2 critical message')

# Get another logger instance
byLogger = pythonUtils.getCustomLogger("myNewLog",logging.INFO,logging.INFO,True)
byLogger.info("3 Got new logger")

byLogger.debug('3 debug message')
byLogger.warning('3 warn message')
byLogger.error('3 error message')
byLogger.critical('3 critical message')

ayLogger.debug('4 this is a new debug message')