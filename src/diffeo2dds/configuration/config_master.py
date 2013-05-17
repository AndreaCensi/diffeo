from conf_tools import ConfigMaster, check_generic_code_desc, GenericCall
from diffeo2dds.model.symdiffeo_system import SymDiffeoSystem


class Diffeo2dDynamicsConfig(ConfigMaster):
    def __init__(self):
        ConfigMaster.__init__(self, 'diffeo2dds')
 
        from ..model import DiffeoSystem

        self.images = self.add_class('images', '*.images.yaml',
                                     check_valid_image_config,
                                     GenericCall(check_valid_image))

        self.symdds = \
            self.add_class_generic('symdds',
                                   '*.symdds.yaml',
                                   SymDiffeoSystem)
        
        self.discdds = \
            self.add_class_generic('discdds', '*.discdds.yaml',
                                   DiffeoSystem)

    def get_default_dir(self):
        from pkg_resources import resource_filename  # @UnresolvedImport
        return resource_filename("diffeo2dds", "configs")
 
get_diffeo2dds_config = Diffeo2dDynamicsConfig.get_singleton




def check_valid_image_config(spec):
    check_generic_code_desc(spec, 'image')


def check_valid_image(x):
    pass  # TODO


def check_valid_symdds_config(spec):
    check_generic_code_desc(spec, 'DDS') 

def check_valid_dds(x):
    pass  # TODO
