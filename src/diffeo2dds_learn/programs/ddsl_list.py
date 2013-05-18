from ..configuration import get_diffeo2ddslearn_config
from .ddsl import DDSL
import sys

__all__ = ['DDSLList']

class DDSLList(DDSL.sub):  # @UndefinedVariable
    cmd = 'list'
    description = 'Lists the available configuration'
    
    def define_program_options(self, params):
        params.add_flag('verbose', help='Instances all configuration')        
        config = get_diffeo2ddslearn_config()
        classes = config.get_classes() 
        examples = ', '.join(classes)
    
        helps = 'Only print one type of objects (%s)' % examples,
        params.add_string('type', help=helps, default=None)
        
    def go(self): 
        config = get_diffeo2ddslearn_config()
        instance = self.options.verbose
        only_type = self.options.type
        config.print_summary(sys.stdout, instance=instance, only_type=only_type)
        
         
