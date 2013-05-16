from conf_tools import ConfigMaster


class Diffeo2sConfig(ConfigMaster):
    def __init__(self):
        ConfigMaster.__init__(self, 'diffeo2s')

        from diffeo2s.symdiffeo import SymbolicDiffeo
        self.symdiffeos = self.add_class_generic('symdiffeos',
                                                 '*.symdiffeos.yaml',
                                                 SymbolicDiffeo)

    def get_default_dir(self):
        from pkg_resources import resource_filename  # @UnresolvedImport
        return resource_filename("diffeo2s", "configs")

get_diffeo2s_config = Diffeo2sConfig.get_singleton
 
