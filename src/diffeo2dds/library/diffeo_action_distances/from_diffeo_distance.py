from contracts import contract
from diffeo2d import Diffeo2dDistance, get_conftools_diffeo2d_distances
from diffeo2dds import DiffeoActionDistance

__all__ = ['SymmetricDiffeoDistance']


class SymmetricDiffeoDistance(DiffeoActionDistance):
        
    @contract(diffeo2d_distance=Diffeo2dDistance)
    def __init__(self, diffeo2d_distance):
        self.diffeo2d_distance = diffeo2d_distance
        
    def distance(self, a1, a2):
        # Note:  forward, forward
        d = self.diffeo2d_distance(a1.diffeo, a2.diffeo)
        # Note: backward, backward
        d_inv = self.diffeo2d_distance(a1.diffeo_inv, a2.diffeo_inv)
        return 0.5 * d + 0.5 * d_inv

    @staticmethod
    def from_yaml(diffeo2d_distance):
        library = get_conftools_diffeo2d_distances()
        _, distance = library.instance_smarter(diffeo2d_distance)
        return SymmetricDiffeoDistance(distance)
        
