from .diffeo_action_estimator_simple import DiffeoActionEstimatorSimple
from conf_tools.utils import check_is_in
from contracts import contract
from diffeo2d import (diffeo_compose, diffeo_identity,
    diffeo_local_differences_L2, Diffeomorphism2D)
from diffeo2dds import DiffeoAction
import numpy as np
import warnings


__all__ = ['DiffeoActionEstimatorNewUnc']

# 
# def length_score_norm(v, v_inv):
#     return np.linalg.norm(np.array(v) + v_inv) 
# 
# def length_score_norm_relative(v, v_inv):
#     l = np.linalg.norm(v)
#     l_inv = np.linalg.norm(v_inv)
#     l_mean = 0.5 * (l + l_inv)
#     if l_mean == 0:
#         return 0
#     else:
#         return np.linalg.norm(np.array(v) + v_inv) / l_mean
#     

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


@contract(d1='valid_diffeomorphism,array[HxW]',
          d2='valid_diffeomorphism,array[HxW]',
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
     
     
# 
# def consistency_based_uncertainty2(field, field_inv, length_score):
#     
#     Y, X = np.meshgrid(range(field.shape[1]), range(field.shape[0]))
#     
#     D = np.zeros(X.shape + (2,))
#     D[:, :, 0] = field[:, :, 0] - X
#     D[:, :, 1] = field[:, :, 1] - Y
#     
#     D_inv = np.zeros(X.shape + (2,))
#     D_inv[:, :, 0] = field_inv[:, :, 0] - X
#     D_inv[:, :, 1] = field_inv[:, :, 1] - Y
#     
#     E = np.zeros(X.shape)
#     E_inv = np.zeros(X.shape)
#     
#     for c in itertools.product(range(X.shape[0]), range(X.shape[1])):
#         v = D[c]
#         v_inv = D_inv[tuple(D[c])]
#         # Length score
#         score = length_score(v, v_inv)
#         
#         if np.isnan(score):
#             print('Debugger break, something unexpected happened')
#             pdb.set_trace()
#         E[tuple(c)] = score
#         
#         v = D_inv[c]
#         v_inv = D[tuple(D_inv[c])]
#         # Length score
#         score = length_score(v, v_inv)
#         if np.isnan(score):
#             pdb.set_trace()
#         E_inv[tuple(c)] = score
#         
#     action.diffeo.variance = 1 - E / np.max(E)
#     action.diffeo.variance_max = np.max(E)
#     action.diffeo_inv.variance = 1 - E_inv / np.max(E_inv)
#     action.diffeo_inv.variance_max = np.max(E_inv)
