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
