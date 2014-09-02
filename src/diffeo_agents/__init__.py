
from .library import *
from conf_tools.global_config import GlobalConfig

def jobs_comptests(context):
    
    config_dirs = [
        'diffeo_agents.configs',
    ]
    GlobalConfig.global_load_dirs(config_dirs)

    from bootstrapping_olympics import get_boot_config
    from comptests import jobs_registrar

    # unittests for boot olympics
    import bootstrapping_olympics.unittests
    jobs_registrar(context, get_boot_config())
