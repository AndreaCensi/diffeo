from diffeo2d import logger

from .configuration import *
from .interface import *
from .programs import *


def jobs_comptests(context):
    config_dirs = [
        'diffeo2ddslearn.configs',
    ]
    from conf_tools.global_config import GlobalConfig
    GlobalConfig.global_load_dirs(config_dirs)


    from . import unittests
    from comptests import jobs_registrar


    config = get_diffeo2ddslearn_config()
    jobs_registrar(context, config)
    jobs_ddsl_demo(context)
    