from procgraph_pil.imread_imp import imread
from contracts import contract
from diffeo2dds.model.uncertain_image import UncertainImage

__all__ = ['load_image']


@contract(returns=UncertainImage)
def load_image(filename):
    """ Reads an image file as an UncertainImage. """
    rgb = imread(filename)
    return UncertainImage(rgb)
