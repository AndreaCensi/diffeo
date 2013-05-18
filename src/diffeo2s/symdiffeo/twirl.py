from . import SymbolicDiffeo, Topology, NoInverseAvailable
from diffeo2s.library import twirl

__all__ = ['Twirl']


class Twirl(SymbolicDiffeo):
    
    def __init__(self):
        SymbolicDiffeo.__init__(self, Topology.PLANE)
    
    def __repr__(self):
        return 'Twirl()'
    
    def get_inverse(self):
        raise NoInverseAvailable()
   
    def apply(self, p):
        return twirl(p)
