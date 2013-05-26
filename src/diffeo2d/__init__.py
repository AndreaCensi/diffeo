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


# from bootstrapping_olympics.utils.change_module import assign_all_symbols_to_module
# assign_all_symbols_to_module(__name__)

