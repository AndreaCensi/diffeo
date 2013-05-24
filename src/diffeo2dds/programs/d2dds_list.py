from ..configuration import get_diffeo2dds_config
from .d2dds import Diffeo2dds
import sys

__all__ = ['Diffeo2ddsList']

class Diffeo2ddsList(Diffeo2dds.get_sub()):
    cmd = 'list'
    description = 'Lists the available configuration'
    
    def define_program_options(self, params):
        params.add_flag('verbose', help='Instances all configuration')        
        config = get_diffeo2dds_config()
        classes = config.get_classes() 
        examples = ', '.join(classes)
        params.add_string('type',
                          help='Only print one type of objects (%s)' % examples,
                          default=None)
        
    def go(self):
        config = get_diffeo2dds_config()
        config.print_summary(sys.stdout,
                             instance=self.options.verbose,
                             only_type=self.options.type)
        
         
