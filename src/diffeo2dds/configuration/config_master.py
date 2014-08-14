from conf_tools import ConfigMaster, ObjectSpec
from contracts import contract 

__all__ = [
   'get_diffeo2dds_config',
   'get_conftools_discdds',
   'get_conftools_uncertain_images',
   'get_conftools_uncertain_image_distances',
   'get_conftools_symdds',
]


class Diffeo2dDynamicsConfig(ConfigMaster):
    def __init__(self):
        ConfigMaster.__init__(self, 'diffeo2dds')
 
        from diffeo2dds import (UncertainImage, UncertainImageDistance,
                                SymDiffeoSystem, DiffeoSystem, DiffeoActionDistance)

        self.add_class_generic('images', '*.images.yaml',  UncertainImage)
        
        self.add_class_generic('uncertain_image_distances',
                           '*.uncertain_image_distances.yaml',
                           UncertainImageDistance)
        
        self.add_class_generic('symdds', '*.symdds.yaml', SymDiffeoSystem)
        
        self.add_class_generic('discdds', '*.discdds.yaml', DiffeoSystem)
            
        self.add_class_generic('diffeo_action_distances',
                               '*.diffeo_action_distances.yaml',
                               DiffeoActionDistance)

    def get_default_dir(self):
        return "diffeo2dds.configs" 
 
get_diffeo2dds_config = Diffeo2dDynamicsConfig.get_singleton
 

@contract(returns=ObjectSpec)
def get_conftools_discdds():
    """ Returns the object responsible for instancing DiffeoSystem. """
    return get_diffeo2dds_config().discdds

@contract(returns=ObjectSpec)
def get_conftools_symdds():
    """ Returns the object responsible for instancing SymDiffeoSystem. """
    return get_diffeo2dds_config().symdds

@contract(returns=ObjectSpec)
def get_conftools_uncertain_images():
    """ Returns the object responsible for instancing UncertainImages. """
    return get_diffeo2dds_config().uncertain_images

@contract(returns=ObjectSpec)
def get_conftools_uncertain_image_distances():
    """ Returns the object responsible for instancing UncertainImagesDistance. """
    return get_diffeo2dds_config().uncertain_image_distances

@contract(returns=ObjectSpec)
def get_conftools_diffeo_action_distances():
    """ Returns the object responsible for instancing DiffeoActionDistance. """
    return get_diffeo2dds_config().diffeo_action_distances
