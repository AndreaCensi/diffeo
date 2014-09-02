from conf_tools import ConfigMaster, ObjectSpec
from contracts import contract


__all__ = ['get_diffeo2dlearn_config', 'get_conftools_diffeo2d_estimators']

class Diffeo2dLearnConfig(ConfigMaster):
    def __init__(self):
        ConfigMaster.__init__(self, 'diffeo2dlearn')
        from diffeo2d_learn import Diffeo2dEstimatorInterface
        self.diffeo2d_estimators = self.add_class_generic('diffeo2d_estimators',
                                                '*.diffeo2d_estimators.yaml',
                                                Diffeo2dEstimatorInterface)


    def get_default_dir(self):
        return "diffeo2d_learn.configs"
 
get_diffeo2dlearn_config = Diffeo2dLearnConfig.get_singleton


@contract(returns=ObjectSpec)
def get_conftools_diffeo2d_estimators():
    return get_diffeo2dlearn_config().diffeo2d_estimators
