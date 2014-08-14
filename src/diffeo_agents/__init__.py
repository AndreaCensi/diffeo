from . import library


#
# def get_comptests():
#     # get testing configuration directory
#     from pkg_resources import resource_filename  # @UnresolvedImport
#     dirname = resource_filename("diffeo_agents", "configs")
#
#     # load into bootstrapping_olympics
#     from comptests import get_comptests_app
#     from bootstrapping_olympics import get_boot_config
#     boot_config = get_boot_config()
#     boot_config.load(dirname)
#
#     import bootstrapping_olympics
#     return bootstrapping_olympics.get_comptests()


def jobs_comptests(context):
    from pkg_resources import resource_filename  # @UnresolvedImport
    dirname = resource_filename("diffeo_agents", "configs")

    from bootstrapping_olympics.configuration import get_boot_config
    from comptests.registrar import jobs_registrar

    boot_config = get_boot_config()
    boot_config.load(dirname)

    # unittests for boot olympics
    import bootstrapping_olympics.unittests
    j1 = jobs_registrar(context, boot_config)

    return j1
