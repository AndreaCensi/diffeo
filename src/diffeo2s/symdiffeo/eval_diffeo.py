from . import SymbolicDiffeo
from contracts import contract
import geometry
import numpy as np


def rotdeg(p, deg):
    R = geometry.rot2d(np.deg2rad(deg))
    return np.dot(R, p)


class EvalDiffeo(SymbolicDiffeo):

    @contract(function='str', inverse='str', topology='str')
    def __init__(self, topology, function, inverse):
        self.topology_s = topology
        SymbolicDiffeo.__init__(self, topology)
        self.function = function
        self.inverse = inverse
            
    def get_inverse(self):
        return EvalDiffeo(topology=self.topology_s,
                          function=self.inverse,
                          inverse=self.function)
    
    @contract(point='array[2]', returns='array[2]')
    def apply(self, point):
        # These are the symbols that can be used 
        p = point  # @UnusedVariable
        x = point[0]  # @UnusedVariable
        y = point[1]  # @UnusedVariable
        dot = np.dot  # @UnusedVariable
        res = eval(self.function)
        res = np.array(res)
        return res
    
    def __repr__(self):
        return ("EvalDiffeo(%s,%s,%s)" % 
                 (self.function, self.inverse, self.topology_s))
    
