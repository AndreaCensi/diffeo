from abc import abstractmethod
from contracts import contract, ContractsMeta
from geometry import R2, TorusW
import numpy as np

__all__ = ['Topology', 'NoInverseAvailable', 'SymbolicDiffeo']


class Topology(object):
    PLANE = 'plane'
    TORUS = 'torus'
    KNOWN = {}
    KNOWN[PLANE] = R2 
    KNOWN[TORUS] = TorusW([2, 2], [-1, -1])


class NoInverseAvailable(Exception):
    pass

class SymbolicDiffeo(object):
    """ Interface for a symbolic diffeomorphism. """
    
    __metaclass__ = ContractsMeta
    
    def __init__(self, topology):
        self.topology_s = topology
        if not topology in Topology.KNOWN:
            raise ValueError('Unknown topology %r' % topology)
        self.topology = Topology.KNOWN[topology]

    def get_topology(self):
        """ Returns the topology under which this is a diffeomorphism """
        return self.topology
    
    @abstractmethod
    def get_inverse(self):
        """ 
            Returns the symbolic diffeomorphism that is the inverse 
            of this one. 
        """
         
    @abstractmethod
    @contract(p='array[2]', returns='array[2]')
    def apply(self, p):
        """ 
            Computes the diffeomorphism applied to a point. 
        """

    @contract(point='seq[2](number)|array[2](float32)')
    def __call__(self, point):
        return self.apply(np.array(point))
    
    def conjugate(self, g):
        """ 
            f.conjugate(g) =  f(g(f^-1))
        """
        from symdiffeo.library import SymDiffeoComposition
        chain = [self.get_inverse(), g, self]
        return SymDiffeoComposition(chain)

        
    
