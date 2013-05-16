from conf_tools import GlobalConfig
from quickapp import QuickMultiCmdApp

class Diffeo2s(QuickMultiCmdApp):
    
    cmd = 'd2s'
    description = 'Main program for manipulating symbolic diffeomorphisms.'
    
    def define_multicmd_options(self, options):
        options.add_flag('dummy', help='workaround for a bug')
        options.add_string_list('config_dirs', help='Configuration directory',
                               default=['default'])
  
    def initial_setup(self):
        options = self.get_options()
        # Load configurations for all modules
        GlobalConfig.global_load_dirs(options.config_dirs)
                  
        
