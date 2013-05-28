from contracts import contract
from diffeo2s import SymbolicDiffeo, get_diffeo2s_config

__all__ = ['SymDiffeoComposition', 'make_chain', 'make_inverse', 'repeat']

class SymDiffeoComposition(SymbolicDiffeo):
    
    @contract(chain='list[>=1]')
    def __init__(self, chain):
        self.chain = chain
        # TODO: check same topology
        topos = [x.topology_s for x in chain]
        if len(set(topos)) > 1:
            msg = 'Incompatible topologies for %s: %s' % (chain, topos)
            raise ValueError(msg)
        SymbolicDiffeo.__init__(self, topos[0])

    def get_inverse(self):
        chain = [x.get_inverse() for x in self.chain[::-1]]
        return SymDiffeoComposition(chain)
    
    def apply(self, p):
        for d in self.chain:
            p = d.apply(p)
        p = self.topology.normalize(p)
        return p
        
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
    
    
    

