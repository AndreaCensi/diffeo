from . import np
from . import assert_allclose
from ..misc_utils import cmap

def cmap_test():
    a = cmap(np.array([5, 5]))
    # print a[:, :, 0]
    # print a[:, :, 1]
    assert a.shape == (5, 5, 2)
    assert_allclose(a[2, 2, 0], 0)
    assert_allclose(a[2, 2, 1], 0)


def cmap_test2():
    a = cmap(np.array([4, 4]))
    assert a.shape == (5, 5, 2)
