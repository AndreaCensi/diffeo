from contracts import contract, new_contract
import numpy as np
import itertools
from diffeo2d import logger

new_contract('valid_2d_shape', 'seq[2](>0)')

__all__ = ['coords_iterate', 'cmap']


@contract(size='valid_2d_shape')
def coords_iterate(size):
    for x in itertools.product(range(size[0]), range(size[1])):
        yield x

@contract(size='array[2]((int32|int64),>=1)', max_shape='None|seq[2](int)')
def cmap(size, max_shape=None):
    for k in [0, 1]:
        if size[k] % 2 == 0:
            logger.warning('cmap must be given odd numbers, got %s' % str(size))
            size[k] = size[k] + 1
            if max_shape is not None:
                size[k] = np.minimum(size[k], max_shape[k])
                
    r = np.zeros(shape=(size[0], size[1], 2), dtype='int32')
    for i, j in coords_iterate(size):
        r[i, j, 0] = i - (size[0] - 1) / 2
        r[i, j, 1] = j - (size[1] - 1) / 2
    return r

