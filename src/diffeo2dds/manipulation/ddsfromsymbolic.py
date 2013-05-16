from .. import DiffeoAction, DiffeoSystem, logger
from contracts import contract
from diffeo2d import Diffeomorphism2D
from diffeo2s.configuration.config_master import get_diffeo2s_config
from diffeo2s.symdiffeo.square_domain import SquareDomain
from diffeo2s.symdiffeo.viewport import diffeo_from_function_viewport
import numpy as np
from diffeo2s.symdiffeo.compositions import make_chain

__all__ = ['DDSFromSymbolic']

@contract(resolution='int,>1', returns=DiffeoSystem)
def DDSFromSymbolic(resolution, actions, topology=None):  # @UnusedVariable
    """ 
        Creates a DiffeoSystem from synthetic diffeomorphisms. 
    """  
    config = get_diffeo2s_config()
    
    logger.info('Creating symbolic diffeomorphism (resolution = %d)' % 
                resolution)
    
    diffeoactions = []
    for _, action in enumerate(actions):
        
        id_diffeo, diffeo = parse_diffeo_spec(config, action['diffeo'])
        label = action.get('label', id_diffeo)
        
        original_cmd = np.array(action['original_cmd'])
        
        logger.info('Getting symbolic diffeomorphism %r' % id_diffeo)
        
        shape = (resolution, resolution)
        viewport = SquareDomain([[-1, +1], [-1, +1]])
        manifold = diffeo.get_topology()
        D, Dinfo = diffeo_from_function_viewport(diffeo, manifold, viewport, shape)    
        D2d = Diffeomorphism2D(D, Dinfo)
        
        diffeo_inv = diffeo.get_inverse()
        D_inv, Dinfo_inv = diffeo_from_function_viewport(diffeo_inv,
                                                          manifold, viewport, shape)    
        D2d_inv = Diffeomorphism2D(D_inv, Dinfo_inv) 

        action = DiffeoAction(label=label,
                              diffeo=D2d,
                              diffeo_inv=D2d_inv,
                              original_cmd=original_cmd)
        diffeoactions.append(action)
        
    dds = DiffeoSystem('%s' % actions, actions=diffeoactions)
    return dds

@contract(spec='str|list(str)')  
def parse_diffeo_spec(config, spec):
    if isinstance(spec, str):
        id_diffeo = spec
        diffeo = config.symdiffeos.instance(id_diffeo)
    elif isinstance(spec, list):
        diffeo = make_chain(spec)
        id_diffeo = '-'.join(spec)
    else:
        assert False
    return id_diffeo, diffeo

