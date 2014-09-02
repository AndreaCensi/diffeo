from diffeo2d import logger
from .configuration import *
from .interfaces import *
from . import library


def jobs_comptests(context):
    # config
    from conf_tools import GlobalConfig
    config_dirs = [
        'diffeo2d_learn.configs',
    ]
    GlobalConfig.global_load_dirs(config_dirs)
     

    # unittests 
    from . import unittests
    
    from comptests import jobs_registrar
    config = get_diffeo2dlearn_config()
    return jobs_registrar(context, config)
