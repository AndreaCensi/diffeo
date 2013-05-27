from diffeo2d import logger

from . import utils
from .configuration import *
from .interfaces import *
from .model import *
from .manipulation import *
from . import library
from .visualization import *


def get_comptests():
    from . import unittests
    from comptests import get_comptests_app
    app = get_comptests_app(get_diffeo2dds_config())
    return [app]
