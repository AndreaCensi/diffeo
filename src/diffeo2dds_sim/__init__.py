""" 
    This module contains a simulator of a diffeo system
    as a boot_olympics RobotInterface. 
""" 

from . import library



def jobs_comptests(context):
    from conf_tools import GlobalConfig

    config_dirs = [
        'diffeo2dds_sim.configs',
    ]
    GlobalConfig.global_load_dirs(config_dirs)
    # load into relevant configs

    # don't forget to trigger unittests
    import bootstrapping_olympics.unittests
    import diffeo2dds_learn.unittests

    from comptests import jobs_registrar
    from bootstrapping_olympics import get_boot_config
    jobs_registrar(context, get_boot_config())
    from diffeo2dds_learn import get_diffeo2ddslearn_config
    jobs_registrar(context, get_diffeo2ddslearn_config())
