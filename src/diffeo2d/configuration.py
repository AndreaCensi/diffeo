from conf_tools import ConfigMaster, ObjectSpec
from contracts import contract

__all__ = ['get_diffeo2d_config',
           'get_conftools_diffeo2d_distances']

@contract(returns=ObjectSpec)
def get_conftools_diffeo2d_distances():
    """ Returns the object responsible for instancing UncertainImagesDistance. """
    return get_diffeo2d_config().diffeo2d_distances

class Diffeo2dConfig(ConfigMaster):
    def __init__(self):
        ConfigMaster.__init__(self, 'diffeo2d')
 
        from diffeo2d.interfaces.diffeo2d_distance import Diffeo2dDistance
        self.diffeo2d_distances = \
            self.add_class_generic('diffeo2d_distances',
                                   '*.diffeo2d_distances.yaml',
                                   Diffeo2dDistance)

    def get_default_dir(self):
        from pkg_resources import resource_filename  # @UnresolvedImport
        return resource_filename("diffeo2d", "configs")
 
get_diffeo2d_config = Diffeo2dConfig.get_singleton
 
