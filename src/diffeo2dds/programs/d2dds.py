from conf_tools import GlobalConfig
from quickapp import QuickMultiCmdApp

class Diffeo2dds(QuickMultiCmdApp):
    
    cmd = 'd2dds'
    description = 'Main program for manipulating symbolic diffeomorphisms.'
    
    def define_multicmd_options(self, options):
        options.add_flag('dummy', help='workaround for a bug')
        options.add_string('config', help='Configuration directory',
                               default='default')
  
    def initial_setup(self):
        options = self.get_options()
        # Load configurations for all modules
        GlobalConfig.global_load_dir(options.config)
                  
        
