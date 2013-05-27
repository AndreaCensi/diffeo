from contracts import contract
from diffeo2dds.model.diffeo_system import DiffeoSystem
from diffeo2dds.unittests.generation import for_all_diffeo_systems

@for_all_diffeo_systems
@contract(id_dds=str, dds=DiffeoSystem)
def comptest_discdds_simple(id_dds, dds):
    print('simple test of %r / %r ' % (id_dds, dds))
