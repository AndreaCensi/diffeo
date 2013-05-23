from diffeo2c.resampling import diffeou_from_diffeoc, diffeoc_from_diffeou, \
    diffeo_resample
from diffeo2d.diffeo_basic import diffeo_identity
from numpy.testing.utils import assert_allclose


def test_resampling_1():
    shape = (10, 10)
    d = diffeo_identity(shape)
    dc = d.astype('float32')
    
    du = diffeou_from_diffeoc(dc)
    d2 = diffeoc_from_diffeou(du)
    assert_allclose(dc, d2)
    


def test_resampling_2():
    shape = (10, 10)
    shape2 = (20, 20)
    d = diffeo_identity(shape)
    dc = d.astype('float32')
    order = 0  # invertible only for linear
    ec = diffeo_resample(dc, shape2, order=order)
    dc2 = diffeo_resample(ec, shape, order=order)
    print "first line"
    print dc[0, :, 0]
    print dc2[0, :, 0]
    print "last line"
    print dc[-1, :, 0]
    print dc2[-1, :, 0]
    assert_allclose(dc, dc2)
    
