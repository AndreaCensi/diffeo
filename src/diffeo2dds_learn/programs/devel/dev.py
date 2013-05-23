from diffeo2dds_learn.programs import DDSL
from quickapp import QuickMultiCmdApp, add_subcommand


class Dev(QuickMultiCmdApp):  # @UndefinedVariable
    """ Development tests for diffeo learning """
    
    cmd = 'dev'
    
    def define_multicmd_options(self, options):
        pass
  
    def initial_setup(self):
        pass
    
    
add_subcommand(DDSL, Dev)
#         options = self.get_options()
#         # Load configurations for all modules
#         GlobalConfig.global_load_dirs(options.config_dirs)
#                   
        

