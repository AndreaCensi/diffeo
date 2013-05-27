from diffeo2dds.unittests.generation import for_all_sym_diffeo_systems
from contracts import contract
from diffeo2dds.model.symdiffeo_system import SymDiffeoSystem

@for_all_sym_diffeo_systems
@contract(id_dds=str, dds=SymDiffeoSystem)
def check_simple(id_dds, dds):
    print('simple test of %r / %r ' % (id_dds, dds))
