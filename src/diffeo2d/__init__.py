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

 
# def get_comptests():
#     from . import unittests
#     from comptests import get_comptests_app
#     app = get_comptests_app(get_diffeo2d_config())
#     return [app]


def jobs_comptests(context):
    from . import unittests
    from comptests import jobs_registrar
    config = get_diffeo2d_config()
    return jobs_registrar(context, config)
