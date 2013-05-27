from contracts import contract
from diffeo2dds.interfaces.diffeo_action_distance import DiffeoActionDistance
from diffeo2dds.unittests.generation import for_all_diffeo_action_distances, \
    for_all_pairs_discdds_distances
from diffeo2dds.model.diffeo_system import DiffeoSystem

@for_all_diffeo_action_distances
@contract(id_ob=str, d=DiffeoActionDistance)
def check_simple(id_ob, d):
    pass

@for_all_pairs_discdds_distances
@contract(id_discdds=str, dds=DiffeoSystem, id_distance=str, distance=DiffeoActionDistance)
def check_pair(id_discdds, dds, id_distance, distance):
    pass
