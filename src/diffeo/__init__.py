""" This is sort of a "main" modules for the others in this package.  """

__version__ = '1.0dev1'

from conf_tools.master import GlobalConfig
from diffeo2dds.programs import Diffeo2dds
from diffeo2dds_learn.programs import DDSL
from diffeo2s.programs.d2s import Diffeo2s
from quickapp import QuickMultiCmdApp, add_subcommand
from conf_tools.instantiate_utils import import_name


class Diffeo(QuickMultiCmdApp):
    """ Main program that links to others."""
    
    cmd = 'diffeo'
    
    def define_multicmd_options(self, options):
        options.add_string('config', help='Configuration directory',
                            default='default')
  
    def initial_setup(self):
        options = self.get_options()
        # Load configurations for all modules
        GlobalConfig.global_load_dir(options.config)
                  

# These are all subcommands
add_subcommand(Diffeo, Diffeo2s)
add_subcommand(Diffeo, Diffeo2dds)
add_subcommand(Diffeo, DDSL)

diffeo_main = Diffeo.get_sys_main()

# 
# def get_comptests():
#     """ Returns the list of QuickApp applications to be used as tests
#         by "comptests" (in package quickapp). """
#     modules = [
#         'diffeo2d',
#         'diffeo2s',
#         'diffeo2d_learn',
#         'diffeo2dds',
#         'diffeo2dds_learn',
#         'diffeo2dds_sim'
#     ]
#     tests = []
#     for name in modules:
#         m = import_name(name)
#         tests.extend(m.get_comptests())
#     return tests
