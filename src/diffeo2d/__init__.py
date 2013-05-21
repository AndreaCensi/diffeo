import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from .misc_utils import *
from .diffeo_basic import *
from .visualization import *
from .diffeomorphism2d import *
from .diffeomorphism2d_continuous import *

from .plumbing import *
from .stats import *


