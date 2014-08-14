from diffeo2d import logger

from . import utils
from .configuration import *
from .interfaces import *
from .model import *
from .manipulation import *
from . import library
from .visualization import *


def jobs_comptests(context):
    import warnings
    from . import unittests
    from comptests import jobs_registrar
    config = get_diffeo2dds_config()
    warnings.warn('fix this')
    config.load('default')
    return jobs_registrar(context, config)
