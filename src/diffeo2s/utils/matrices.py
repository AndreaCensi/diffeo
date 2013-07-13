import numpy as np
import itertools
from contracts import contract

__all__ = ['construct_matrix_iterators',
           'construct_matrix',
           'construct_distance_matrix',
           'iterate_indices',
           'coords_iterate']


def construct_matrix_iterators(iterators, function):
    
    elements = map(list, iterators)
    shape = map(len, elements)
    
    def element(*args):  # args is a tuple of indices = (i, j, k, ...)
        assert len(args) == len(shape)
        combination = [a[i] for a, i in zip(elements, args)]
        return function(*combination)
        
    return construct_matrix(shape, element)
    
@contract(shape='seq[2](int)', returns='distance_matrix')
def construct_distance_matrix(shape, function):
    return construct_matrix(shape, function)


def construct_matrix(shape, function):
    ndim = len(shape)
    if ndim != 2:
        msg = 'Sorry, not implemented for ndim != 2 (got %d).' % ndim
        raise NotImplementedError(msg)
    D = np.zeros(shape) 
    for indices in iterate_indices(shape):
        result = function(*indices)
        if not isinstance(result, float):
            raise ValueError('%s(%s) = %s' % 
                             (function.__name__, indices, result))
        D[indices] = result
    return D



def iterate_indices(shape):
    if len(shape) == 2:
        for i, j in itertools.product(range(shape[0]), range(shape[1])):
            yield i, j
    else:
        raise NotImplementedError
        assert(False)

@contract(size='valid_2d_shape')
def coords_iterate(size):
    for x in itertools.product(range(size[0]), range(size[1])):
        yield x
