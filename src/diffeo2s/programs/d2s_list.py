from .d2s import Diffeo2s
from diffeo2s.configuration import get_diffeo2s_config
import sys

__all__ = ['Diffeo2sList']

class Diffeo2sList(Diffeo2s.sub):  # @UndefinedVariable
    cmd = 'list'
    description = 'Lists the available configuration'
    
    def define_program_options(self, params):
        params.add_flag('verbose', help='Instances all configuration')        
        config = get_diffeo2s_config()
        classes = config.get_classes() 
        examples = ', '.join(classes)
        params.add_string('type',
                          help='Only print one type of objects (%s)' % examples,
                          default=None)
        
    def go(self):
        options = self.get_options()        
        config = get_diffeo2s_config()
        config.print_summary(sys.stdout,
                             instance=options.verbose, only_type=options.type)
        
         
