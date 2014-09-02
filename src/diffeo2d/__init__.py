import logging
import sys

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from .diffeo_basic import *

from .configuration import *
from .interfaces import *
from .misc_utils import *
from .visualization import *
from .diffeomorphism2d_continuous import *

from .plumbing import *
from .stats import *

from . import library



def jobs_comptests(context):
    from conf_tools import GlobalConfig
    config_dirs = [
        'diffeo2d.configs',
    ]
    GlobalConfig.global_load_dirs(config_dirs)
    
    from . import unittests
    
    from comptests import jobs_registrar
    jobs_registrar(context, get_diffeo2d_config())
