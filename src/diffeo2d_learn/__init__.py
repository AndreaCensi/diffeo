from diffeo2d import logger
from .configuration import *
from .interfaces import *
from . import library


def jobs_comptests(context):
    # config
    from conf_tools import GlobalConfig
    GlobalConfig.global_load_dirs(['diffeo2d_learn.configs'])

    # unittests 
    from . import unittests
    
    from comptests import jobs_registrar
    config = get_diffeo2dlearn_config()
    return jobs_registrar(context, config)
