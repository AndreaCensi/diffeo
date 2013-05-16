from conf_tools import ConfigMaster
from diffeo2d_learn.diffeo_estimator_interface import Diffeo2dEstimatorInterface

class Diffeo2dLearnConfig(ConfigMaster):
    def __init__(self):
        ConfigMaster.__init__(self, 'diffeo2dlearn')

        self.diffeo2d_estimators = self.add_class_generic('diffeo2d_estimators',
                                                '*.diffeo2d_estimators.yaml',
                                                Diffeo2dEstimatorInterface)

#         self.symdiffeos = self.add_class('symdiffeos', '*.symdiffeos.yaml',
#                                      check_valid_symdiffeo_config,
#                                      GenericCall(check_valid_symdiffeo))
# 
#         self.symdds = self.add_class('symdds', '*.symdds.yaml',
#                                      check_valid_symdds_config,
#                                      GenericCall(check_valid_dds))
# 
#         self.discdds = self.add_class('discdds', '*.discdds.yaml',
#                                      check_valid_discdds_config,
#                                      GenericCall(check_valid_dds))
  

    def get_default_dir(self):
        from pkg_resources import resource_filename  # @UnresolvedImport
        return resource_filename("diffeo2d_learn", "configs")
 
get_diffeo2dlearn_config = Diffeo2dLearnConfig.get_singleton
# set_diffeo2dlearn_config = Diffeo2dLearnConfig.set_singleton






