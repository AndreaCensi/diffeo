from . import SymbolicDiffeo
from contracts import contract
from ..configuration import get_diffeo2s_config


class SymDiffeoComposition(SymbolicDiffeo):
    
    @contract(chain='list[>=1]')
    def __init__(self, chain):
        self.chain = chain
        # TODO: check same topology
        SymbolicDiffeo.__init__(self, chain[0].topology_s)

    def get_inverse(self):
        chain = [x.get_inverse() for x in self.chain[::-1]]
        return SymDiffeoComposition(chain)
    
    def apply(self, point):
        for d in self.chain:
            point = d.apply(point)
        return point
        
    def __repr__(self):
        return ("Comp(%s)" % self.chain)

    
def make_chain(diffeos):
    symdiffeos = get_diffeo2s_config().symdiffeos
    chain = map(symdiffeos.instance, diffeos) 
    return SymDiffeoComposition(chain)     

def make_inverse(id_diffeo):
    symdiffeos = get_diffeo2s_config().symdiffeos 
    return symdiffeos.instance(id_diffeo).get_inverse()     


@contract(times='>=1')
def repeat(id_diffeo, times):
    symdiffeos = get_diffeo2s_config().symdiffeos 
    diffeo = symdiffeos.instance(id_diffeo)
    chain = [diffeo] * times
    return SymDiffeoComposition(chain)
    
    
    

