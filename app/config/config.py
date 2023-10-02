"""
Module to manage config parameters
"""

import os
from configobj import ConfigObj

BASE = os.path.dirname(os.path.abspath(__file__))
CONFIG = ConfigObj(os.path.join(BASE, 'config.cfg'))

API = CONFIG['api']
LOG = CONFIG['log']
WORKER = CONFIG['worker']