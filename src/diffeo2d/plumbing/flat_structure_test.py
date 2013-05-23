import unittest
from diffeo2d.plumbing.flat_structure import FlatStructure
from diffeo2d.diffeo_basic import diffeo_identity
from numpy.testing import assert_allclose

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
        
