from diffeo2dds.unittests.generation import for_all_uncertain_images_distances
from contracts import contract
from diffeo2dds.model.uncertain_image import UncertainImageDistance

@for_all_uncertain_images_distances
@contract(id_ob=str, d=UncertainImageDistance)
def check_simple(id_ob, d):
    pass
