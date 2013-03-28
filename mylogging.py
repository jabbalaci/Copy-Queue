import logging
import sys
import config as cfg

DEBUG_LOG_FILENAME = cfg.LOGFILE
#WARNING_LOG_FILENAME = 'my-warning.log'

# set up formatting
#formatter = logging.Formatter('[%(asctime)s] %(levelno)s (%(process)d) %(module)s: %(message)s')
#formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s",
                              # "%Y-%m-%d %H:%M:%S")
formatter = logging.Formatter("%(levelname)-5s %(asctime)s %(module)s.%(funcName)s() [%(lineno)d]: %(message)s",
                              "%Y-%m-%d %H:%M:%S")

# set up logging to STDOUT for all levels DEBUG and higher
sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.DEBUG)
sh.setFormatter(formatter)

# set up logging to a file for all levels DEBUG and higher
fh = logging.FileHandler(DEBUG_LOG_FILENAME)
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

# set up logging to a file for all levels WARNING and higher
#fh2 = logging.FileHandler(WARNING_LOG_FILENAME)
#fh2.setLevel(logging.WARN)
#fh2.setFormatter(formatter)

# create Logger object
mylogger = logging.getLogger('MyLogger')
mylogger.setLevel(logging.DEBUG)
# mylogger.addHandler(sh)
mylogger.addHandler(fh)
#mylogger.addHandler(fh2)

# create shortcut functions
debug = mylogger.debug
info = mylogger.info
warning = mylogger.warning
error = mylogger.error
critical = mylogger.critical
