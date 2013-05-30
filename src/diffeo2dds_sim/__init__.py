""" 
    This module contains a simulator of a diffeo system
    as a boot_olympics RobotInterface. 
""" 

from . import library


def get_comptests():
    # get testing configuration directory 
    from pkg_resources import resource_filename  # @UnresolvedImport
    dirname = resource_filename("diffeo2dds_sim", "configs")
    
    tests = []
    
    import bootstrapping_olympics
    bootstrapping_olympics.get_boot_config().load(dirname)
    tests.extend(bootstrapping_olympics.get_comptests())
    
    import diffeo2dds_learn
    diffeo2dds_learn.get_diffeo2ddslearn_config().load(dirname)
    tests.extend(diffeo2dds_learn.get_comptests())
    
    return tests
