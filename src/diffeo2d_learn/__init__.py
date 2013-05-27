from diffeo2d import logger
from .configuration import *
from .interfaces import *
from . import library




def get_comptests():
    from . import unittests
    from comptests import get_comptests_app
    app = get_comptests_app(get_diffeo2dlearn_config())
    return [app]
