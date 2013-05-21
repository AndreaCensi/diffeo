""" A module to contain the interface to the others. """
__version__ = '1.0dev1'

from conf_tools.master import GlobalConfig
from diffeo2dds.programs import Diffeo2dds
from diffeo2dds_learn.programs import DDSL
from diffeo2s.programs.d2s import Diffeo2s
from quickapp import QuickMultiCmdApp, add_subcommand


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
