import unittest
from diffeo2d.plumbing.flat_structure import FlatStructure
from diffeo2d.diffeo_basic import diffeo_identity
from numpy.testing import assert_allclose
import numpy as np

class FlatStructureTest(unittest.TestCase):
    
    def flat_test1(self):
        """ Same if we give the identity as centers """
        shape = (10, 15)
        area = (4, 4)
        fs1 = FlatStructure(shape, area, None)

        centers = diffeo_identity(shape)
        fs2 = FlatStructure(shape, area, centers)
        
        n1 = fs1.neighbor_indices_flat
        n2 = fs2.neighbor_indices_flat
        
        assert_allclose(n1, n2)
        
    def flat_test_plane(self):
        """ Same if we give the identity as centers """
        shape = (10, 15)
        area = (4, 4)
        fs1 = FlatStructure(shape, area)
        fs2 = FlatStructure(shape, area, topology='plane')
        # default is plane
        assert_allclose(fs1.neighbor_indices_flat, fs2.neighbor_indices_flat)
        
        # torus is different
        fs3 = FlatStructure(shape, area, topology='torus')
        assert np.any(fs3.neighbor_indices_flat != fs2.neighbor_indices_flat)
        
        self.assertRaises(ValueError, FlatStructure, shape, area, topology='invalid')

    def flat_test_strange(self):
        shape = (4, 4)
        centers = np.floor(np.random.rand(shape[0], shape[1], 2) * 4)
        fs = FlatStructure(shape, neighborarea=(5, 5), centers=centers)
        y = np.zeros(shape)
        v = fs.values2unrolledneighbors(y)


    def flat_test_slow(self):
        shape = (10, 15)
        area = (4, 4)
        fs = FlatStructure(shape, area)
        x1 = fs.get_distances_to_area_center_slow()
        x2 = fs.get_distances_to_area_center()
        assert_allclose(x1, x2)
        
#     def flat_test_slow2(self):
#         shape = (10, 15)
#         area = (4, 4)
#         fs = FlatStructure(shape, area)
#         x1 = fs.get_distances_to_area_border()
#         x2 = fs.get_distances_to_area_border_slow()
#         assert_allclose(x1, x2)
        
    
    def flat_test_slow2(self):
        shape = (10, 11)
        area = (3, 3)
        fs = FlatStructure(shape, area)
        x1 = fs.get_distances_to_area_border()
        assert_allclose(x1[0, :], [0, 0, 0, 0, 1, 0, 0, 0, 0])
        assert_allclose(x1[10, :], [0, 0, 0, 0, 1, 0, 0, 0, 0])
        

    def flat_test_slow3(self):
        shape = (10, 11)
        area = (4, 4)
        fs = FlatStructure(shape, area)
        y = fs.unrolled2multidim(fs.get_distances_to_area_border())
        first = y[0, 0, ...]
        assert_allclose(first,
                        [[0., 0., 0., 0., 0.],
                         [0., 1., 1., 1., 0.],
                        [0., 1., 2., 1., 0.],
                         [0., 1., 1., 1., 0.],
                         [0., 0., 0., 0., 0.]])
                                
        
        
