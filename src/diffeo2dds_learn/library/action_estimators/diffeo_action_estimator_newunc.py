from .diffeo_action_estimator_simple import DiffeoActionEstimatorSimple
from conf_tools.utils import check_is_in
from contracts import contract
from diffeo2d import (diffeo_compose, diffeo_identity,
    diffeo_local_differences_L2, Diffeomorphism2D)
from diffeo2dds import DiffeoAction
import numpy as np
import warnings


__all__ = ['DiffeoActionEstimatorNewUnc', 'consistency_based_uncertainty2',
           'consistency_based_uncertainty']


class DiffeoActionEstimatorNewUnc(DiffeoActionEstimatorSimple):
    """ This implements the new consistency-based uncertainty detection. """

    scores = ['norm', 'normrel']
        
    def __init__(self, score, **kwargs):
        DiffeoActionEstimatorSimple.__init__(self, **kwargs)
        self.score = score
        check_is_in('score function', score, DiffeoActionEstimatorNewUnc.scores)
    
    def __repr__(self):
        return 'DAENewUnc(score=%s;%s;%s)' % (self.score, self.est, self.est_inv)  
      
    @contract(returns=DiffeoAction)
    def get_value(self):
        action = DiffeoActionEstimatorSimple.get_value(self)
        warnings.warn('remove this debugging thing')
        self.score = 'norm'
        if self.score == 'normrel':
            normalize_distance = True
        elif self.score == 'norm':
            normalize_distance = False
        else:
            assert False
        action2 = consistency_based_uncertainty(action,
                                      normalize_distance=normalize_distance)
        return action2

@contract(action=DiffeoAction, normalize_distance=bool, returns=DiffeoAction)
def consistency_based_uncertainty(action, normalize_distance):
    '''
    Update the uncertainties for the action by the improved uncertainty 
    classification based on comparing the diffeomorphism with its inverse. 
    '''
    # print('Using length score function %s' % length_score)
    d1 = action.diffeo.d
    d2 = action.diffeo_inv.d
    v1, v2 = consistency_based_uncertainty2(d1, d2, normalize_distance)
    D1 = Diffeomorphism2D(d1, v1)
    D2 = Diffeomorphism2D(d2, v2)
    a = DiffeoAction(label=action.label, diffeo=D1, diffeo_inv=D2,
                     original_cmd=action.original_cmd)
    return a


@contract(d1='valid_diffeomorphism,array[HxWx2]',
          d2='valid_diffeomorphism,array[HxWx2]',
          returns='seq[2](array[HxW](>=0,<=1))')
def consistency_based_uncertainty2(d1, d2, normalize_distance=True):
    """ Returns the assigned uncertainty field for the two diffeomorphisms. """
    d12 = diffeo_compose(d1, d2)
    d21 = diffeo_compose(d2, d1)
    shape = d1.shape[:2]
    
    # compute the distance of each point to the identity
    identity = diffeo_identity(shape)
    e2 = diffeo_local_differences_L2(d12, identity)
    e1 = diffeo_local_differences_L2(d21, identity)
    
    if normalize_distance:
        d1n = diffeo_local_differences_L2(d1, identity)
        d2n = diffeo_local_differences_L2(d2, identity)
        d1n[d1n == 0] = 1
        d2n[d2n == 0] = 1
        e2 = e2 / d2n
        e1 = e1 / d1n
        
    # normalize fields in [0, 1]
    def normalize(e):
        m = np.max(e)
        if m > 0:
            e = e / m
        v = 1 - e
        return v
    
    v1 = normalize(e1)
    v2 = normalize(e2)
    return v1, v2
     
