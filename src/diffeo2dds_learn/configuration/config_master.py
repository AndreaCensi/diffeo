from conf_tools import ConfigMaster
from contracts import contract
from conf_tools.objspec import ObjectSpec


__all__ = [
   'get_diffeo2ddslearn_config',
   'get_conftools_diffeoaction_estimators',
   'get_conftools_diffeosystem_estimators',
   'get_conftools_image_streams',
   'get_conftools_streams'
]

class Diffeo2ddsLearnConfig(ConfigMaster):
    def __init__(self):
        
        from diffeo2dds_learn import (DiffeoActionEstimatorInterface, ImageStream,
                                    DiffeoSystemEstimatorInterface, Stream)
        
        ConfigMaster.__init__(self, 'diffeo2ddslearn')

        self.streams = \
            self.add_class_generic('streams',
                                   '*.streams.yaml',
                                    Stream)
        
        self.image_streams = \
            self.add_class_generic('image_streams',
                                   '*.image_streams.yaml',
                                    ImageStream)

        self.diffeoaction_estimators = \
            self.add_class_generic('diffeoaction_estimators',
                                   '*.diffeoaction_estimators.yaml',
                                    DiffeoActionEstimatorInterface)

        self.diffeosystem_estimators = \
            self.add_class_generic('diffeosystem_estimators',
                                   '*.diffeosystem_estimators.yaml',
                                    DiffeoSystemEstimatorInterface)

    def get_default_dir(self):
        from pkg_resources import resource_filename  # @UnresolvedImport
        return resource_filename("diffeo2dds_learn", "configs")
 
get_diffeo2ddslearn_config = Diffeo2ddsLearnConfig.get_singleton 

@contract(returns=ObjectSpec)
def get_conftools_diffeoaction_estimators():
    """ Returns the object responsible for instancing UncertainImages. """
    return get_diffeo2ddslearn_config().diffeoaction_estimators


@contract(returns=ObjectSpec)
def get_conftools_diffeosystem_estimators():
    """ Returns the object responsible for instancing UncertainImages. """
    return get_diffeo2ddslearn_config().diffeosystem_estimators


@contract(returns=ObjectSpec)
def get_conftools_streams():
    """ 
        Returns the object responsible for instancing Streams
        of LogItem. 
    """
    return get_diffeo2ddslearn_config().streams


@contract(returns=ObjectSpec)
def get_conftools_image_streams():
    """ 
        Returns the object responsible for instancing ImageStream.
    """
    return get_diffeo2ddslearn_config().image_streams
