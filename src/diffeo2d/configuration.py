from conf_tools import ConfigMaster, ObjectSpec
from contracts import contract

__all__ = [
   'get_diffeo2d_config',
   'get_conftools_diffeo2d_distances',
   'get_conftools_diffeo2d',
]


class Diffeo2dConfig(ConfigMaster):
    def __init__(self):
        ConfigMaster.__init__(self, 'diffeo2d')
 
        from diffeo2d import Diffeo2dDistance
        self.add_class_generic('diffeo2d_distances',
                               '*.diffeo2d_distances.yaml',
                               Diffeo2dDistance)
        
        from diffeo2d import Diffeomorphism2D
        self.add_class_generic('diffeo2d', '*.diffeo2d.yaml', 
                               Diffeomorphism2D)

    def get_default_dir(self):
        return "diffeo2d.configs"
 
get_diffeo2d_config = Diffeo2dConfig.get_singleton
 

@contract(returns=ObjectSpec)
def get_conftools_diffeo2d():
    return get_diffeo2d_config().diffeo2d

@contract(returns=ObjectSpec)
def get_conftools_diffeo2d_distances():
    """ Returns the object responsible for instancing Diffeo2dDistance. """
    return get_diffeo2d_config().diffeo2d_distances
