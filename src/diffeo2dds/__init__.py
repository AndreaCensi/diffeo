from diffeo2d import logger

from . import utils
from .configuration import *
from .interfaces import *
from .model import *
from .manipulation import *
from . import library
from .visualization import *



# def get_comptests():
#     from . import unittests
#     from comptests import get_comptests_app
#     get_diffeo2dds_config().load('default')
#     app = get_comptests_app(get_diffeo2dds_config())
#     return [app]


def jobs_comptests(context):
    import warnings
    from . import unittests
    from comptests import jobs_registrar
    config = get_diffeo2dds_config()
    warnings.warn('fix this')
    config.load('default')
    return jobs_registrar(context, config)
