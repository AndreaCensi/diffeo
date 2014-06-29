from contracts import contract

from diffeo2dds import UncertainImage


__all__ = ['load_image']


@contract(returns=UncertainImage)
def load_image(filename):
    """ Reads an image file as an UncertainImage. """
    from procgraph_pil import imread

    rgb = imread(filename)
    return UncertainImage(rgb)
