from conf_tools import ConfigMaster


__all__ = ['get_diffeo2ddslearn_config']

class Diffeo2ddsLearnConfig(ConfigMaster):
    def __init__(self):
        
        from diffeo2dds_learn import (DiffeoActionEstimatorInterface, ImageStream,
                                    DiffeoSystemEstimatorInterface, Stream)
        
        ConfigMaster.__init__(self, 'diffeo2dlearn')

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





