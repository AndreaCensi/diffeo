from contracts import contract
from .diffeomorphism2d import Diffeomorphism2D

__all__ = ['UncertainDiffeoDistance']

class UncertainDiffeoDistance(object):
    
    @contract(d1=Diffeomorphism2D, d2=Diffeomorphism2D)
    def distance(self, d1, d2):
        raise NotImplemented
    
