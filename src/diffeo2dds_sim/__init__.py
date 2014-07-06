""" 
    This module contains a simulator of a diffeo system
    as a boot_olympics RobotInterface. 
""" 

from . import library
#
#
# def get_comptests():
#     # get testing configuration directory
#     from pkg_resources import resource_filename  # @UnresolvedImport
#     dirname = resource_filename("diffeo2dds_sim", "configs")
#
#     tests = []
#
#     import bootstrapping_olympics
#     bootstrapping_olympics.get_boot_config().load(dirname)
#     tests.extend(bootstrapping_olympics.get_comptests())
#
#     import diffeo2dds_learn
#     diffeo2dds_learn.get_diffeo2ddslearn_config().load(dirname)
#     tests.extend(diffeo2dds_learn.get_comptests())
#
#     return tests


def jobs_comptests(context):
    from comptests import jobs_registrar

    # get testing configuration directory
    from pkg_resources import resource_filename  # @UnresolvedImport
    dirname = resource_filename("diffeo2dds_sim", "configs")

    # load into relevant configs

    # 1 - for bootolympics
    from bootstrapping_olympics import get_boot_config
    boot_config = get_boot_config()
    boot_config.load(dirname)

    # 2 - for diffeo2dds_learn
    from diffeo2dds_learn import get_diffeo2ddslearn_config
    diffe2ddslearn_config = get_diffeo2ddslearn_config()
    diffe2ddslearn_config.load(dirname)

    # don't forget to trigger unittests
    import bootstrapping_olympics.unittests
    import diffeo2dds_learn.unittests

    j1 = jobs_registrar(context, boot_config)
    j2 = jobs_registrar(context, diffe2ddslearn_config)

    return j1, j2
