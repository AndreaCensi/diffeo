from .test_generation import for_all_imagestreams
from itertools import islice

@for_all_imagestreams
def simple_check_imagestream(id_image_stream, image_stream):
    print('testing %r' % id_image_stream)

    n = 3
    for image in islice(image_stream.read_all(), n):
        print image.shape
