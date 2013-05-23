from .. import (coords_iterate, coords_to_X, X_to_coords)
from numpy.testing import assert_allclose

def X_to_coords_test():
    shape = (40, 50)
    for coords in coords_iterate(shape):
        X = coords_to_X(coords, shape)
        coords2 = X_to_coords(X, shape)
        msg = 'coords: %s  X: %s  coords2: %s' % (coords, X, coords2)
        assert_allclose(coords2, coords, err_msg=msg)



def X_to_coords_test2():
    shape = (20, 20)
    for coords in coords_iterate(shape):
        X = coords_to_X(coords, shape)
        coords2 = X_to_coords(X, shape)
        msg = 'coords: %s  X: %s  coords2: %s' % (coords, X, coords2)
        assert_allclose(coords2, coords, err_msg=msg)


def X_to_coords_test3():
    shape = (20, 21)
    x1 = coords_to_X((0, 0), shape)
    c1 = X_to_coords(x1, shape)
    print 'x1', x1
    print 'c1', c1
