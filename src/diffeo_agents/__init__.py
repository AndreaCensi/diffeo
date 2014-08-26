
from .library import *

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
