from comptests.registrar import comptests_for_all, comptests_for_all_pairs
from diffeo2dds.configuration.config_master import (get_conftools_discdds,
    get_conftools_symdds, get_conftools_uncertain_image_distances,
    get_conftools_uncertain_images, get_conftools_diffeo_action_distances)


for_all_diffeo_systems = comptests_for_all(get_conftools_discdds())
for_all_sym_diffeo_systems = comptests_for_all(get_conftools_symdds())
for_all_uncertain_images = comptests_for_all(get_conftools_uncertain_images())
for_all_uncertain_images_distances = comptests_for_all(get_conftools_uncertain_image_distances())
for_all_diffeo_action_distances = comptests_for_all(get_conftools_diffeo_action_distances())

dad = get_conftools_diffeo_action_distances()
discdds = get_conftools_discdds() 

for_all_pairs_discdds_distances = comptests_for_all_pairs(discdds, dad)

