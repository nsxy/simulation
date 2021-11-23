# coding=utf-8
import logging
from datetime import datetime

from simulation.object import *
from simulation.utils import *

'''Config for global logger
LOG_FORMAT: format for the logger
FILE_NAME: file name for the logger output

filter the log level below INFO level 
'''
LOG_FORMAT = '%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] [%(funcName)s] %(message)s'
FILE_NAME = '{}.log'.format(datetime.now().strftime('%m%d.%H%M%S.%f'))
logging.basicConfig(filename=FILE_NAME, level=logging.WARNING, format=LOG_FORMAT)