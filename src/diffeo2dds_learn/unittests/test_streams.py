from .test_generation import for_all_streams
from itertools import islice

@for_all_streams
def simple_check_stream(id_stream, stream):
    print('testing %r' % id_stream)

    n = 6
    for log_item in islice(stream.read_all(), n):
        y0 = log_item.y0
        u0 = log_item.u
        y1 = log_item.y1
        print u0
