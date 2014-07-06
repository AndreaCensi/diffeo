from diffeo2d import logger

from .configuration import *
from .interface import *
from .programs import *

#
# def get_comptests():
#     """ Returns the list of QuickApp applications to be used as tests
#         by "comptests" (in package quickapp). """
#     from . import unittests
#     from comptests import get_comptests_app
#     app = get_comptests_app(get_diffeo2ddslearn_config())
#
#     return [app, DDSLDemo1]


def jobs_comptests(context):
    import warnings
    from . import unittests
    from comptests import jobs_registrar
    config = get_diffeo2ddslearn_config()
    j1 = jobs_registrar(context, config)
    j2 = jobs_ddsl_demo(context)
    return j1, j2
