from contracts import contract
from diffeo2dds.model.uncertain_image import UncertainImage
from diffeo2dds.unittests.generation import (for_all_sym_diffeo_systems,
    for_all_uncertain_images)


@for_all_uncertain_images
@contract(id_ob=str, ui=UncertainImage)
def check_simple(id_ob, ui):
    print('simple test of %r / %r ' % (id_ob, ui))
