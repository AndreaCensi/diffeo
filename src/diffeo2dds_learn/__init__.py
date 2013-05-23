from diffeo2d import logger

from .configuration import *
from .interface import *
from .programs import *

def get_comptests():
    """ Returns the list of QuickApp applications to be used as tests
        by "comptests" (in package quickapp). """
    return [DDSLDemo1]
