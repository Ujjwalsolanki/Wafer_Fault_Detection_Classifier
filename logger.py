import os
import sys
import logging
from datetime import datetime


LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
LOGS_PATH = os.path.join(os.getcwd(),"logs", LOG_FILE)
os.makedirs(LOGS_PATH, exist_ok=True)

LOG_FILE_PATH = os.path.join(LOGS_PATH, LOG_FILE)

# logging_str = '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'
LOGGING_STR = '[%(asctime)s] {%(filename)s:%(funcName)s():%(lineno)d} %(levelname)s - %(message)s'
# logging_str = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"

logging.basicConfig(
    level= logging.INFO,
    format= LOGGING_STR,

    handlers=[
        logging.FileHandler(LOG_FILE_PATH, mode="a"),
        logging.StreamHandler(sys.stdout)
    ]
)
