from config import config
import logging.handlers
import os
import time
import datetime

API_CONFIG = config.API
LOG_CONFIG = config.LOG
LOG_FOLDER = LOG_CONFIG['folder']
LOG_FILE = LOG_CONFIG['main_file']
DAYS_FOR_ROTATE = int(LOG_CONFIG['days_for_rotate'])
LOG = LOG_FOLDER + LOG_FILE

try:
    os.stat(LOG_FOLDER)
except FileNotFoundError as e:
    print('------------------------------------------------------------------')
    print('[ERROR] Error writing log at %s' % LOG)
    print('[ERROR] Please verify path folder exits')
    print('------------------------------------------------------------------')
    exit()

try:
    logger = logging.getLogger('access')
    loggerHandler = logging.handlers.TimedRotatingFileHandler(filename=LOG, when='midnight', interval=1, backupCount=DAYS_FOR_ROTATE)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    loggerHandler.setFormatter(formatter)
    logger.addHandler(loggerHandler)
    logger.setLevel(logging.DEBUG)
except PermissionError as e:
    print('------------------------------------------------------------------')
    print('[ERROR] Error writing log at %s' % LOG)
    print('[ERROR] Please verify write permissions')
    print('------------------------------------------------------------------')
    exit()


def get_logger():
    """ Return an instance of logger to write log at dispatcher.log file """
    return logger


def write_log(request):
    logger.info("[%s] -- %s %d %fms", str(request.request.method), request.request.uri, request._status_code, 1000 * (time.time() - request.request._start_time))
