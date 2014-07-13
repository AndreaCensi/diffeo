import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


from .configuration import *
from .interfaces import *
from .symdiffeo import *
from . import library



def jobs_comptests(context):
    import warnings
    from . import unittests
    from comptests import jobs_registrar
    config = get_diffeo2s_config()
    return jobs_registrar(context, config)
