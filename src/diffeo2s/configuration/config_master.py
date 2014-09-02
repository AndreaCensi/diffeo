from conf_tools import ConfigMaster
from contracts import contract
from conf_tools.objspec import ObjectSpec

__all__ = ['get_diffeo2s_config', 'get_conftools_symdiffeos']

class Diffeo2sConfig(ConfigMaster):
    def __init__(self):
        ConfigMaster.__init__(self, 'diffeo2s')

        from diffeo2s import SymbolicDiffeo
        self.symdiffeos = self.add_class_generic('symdiffeos',
                                                 '*.symdiffeos.yaml',
                                                 SymbolicDiffeo)

    def get_default_dir(self):
        return "diffeo2s.configs"

get_diffeo2s_config = Diffeo2sConfig.get_singleton
 


@contract(returns=ObjectSpec)
def get_conftools_symdiffeos():
    return get_diffeo2s_config().symdiffeos
