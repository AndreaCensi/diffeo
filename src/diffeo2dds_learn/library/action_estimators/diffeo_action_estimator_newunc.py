from . import DiffeoActionEstimatorSimple
from conf_tools.utils import check_is_in
from contracts import contract
from diffeo2dds import DiffeoAction
import itertools
import numpy as np
import pdb

__all__ = ['DiffeoActionEstimatorNewUnc']


def length_score_norm(v, v_inv):
    return np.linalg.norm(np.array(v) + v_inv) 

def length_score_norm_relative(v, v_inv):
    l = np.linalg.norm(v)
    l_inv = np.linalg.norm(v_inv)
    l_mean = 0.5 * (l + l_inv)
    if l_mean == 0:
        return 0
    else:
        return np.linalg.norm(np.array(v) + v_inv) / l_mean
    

class DiffeoActionEstimatorNewUnc(DiffeoActionEstimatorSimple):
    """ This implements the new consistency-based uncertainty detection. """

    scores = {'norm': length_score_norm,
              'normrel': length_score_norm_relative}
        
    def __init__(self, score, **kwargs):
        DiffeoActionEstimatorSimple.__init__(self, **kwargs)
        self.score = score
        check_is_in('score function', score, DiffeoActionEstimatorNewUnc.scores)
        
    @contract(returns=DiffeoAction)
    def get_value(self):
        action = DiffeoActionEstimatorSimple.get_value(self)
        score_function = DiffeoActionEstimatorNewUnc.scores[self.score]
        consistency_based_uncertainty(action, score_function)
        return action


def consistency_based_uncertainty(action, length_score):
    '''
    Update the uncertainties for the action by the improved uncertainty 
    classification based on comparing the diffeomorphism with its inverse. 
    '''
    # print('Using length score function %s' % length_score)
    field = action.diffeo.d
    field_inv = action.diffeo_inv.d
    
    Y, X = np.meshgrid(range(field.shape[1]), range(field.shape[0]))
    
    D = np.zeros(X.shape + (2,))
    D[:, :, 0] = field[:, :, 0] - X
    D[:, :, 1] = field[:, :, 1] - Y
    
    D_inv = np.zeros(X.shape + (2,))
    D_inv[:, :, 0] = field_inv[:, :, 0] - X
    D_inv[:, :, 1] = field_inv[:, :, 1] - Y
    
    E = np.zeros(X.shape)
    E_inv = np.zeros(X.shape)
    
    for c in itertools.product(range(X.shape[0]), range(X.shape[1])):
        v = D[c]
        v_inv = D_inv[tuple(D[c])]
        # Length score
        score = length_score(v, v_inv)
        
        if np.isnan(score):
            print('Debugger break, something unexpected happened')
            pdb.set_trace()
        E[tuple(c)] = score
        
        v = D_inv[c]
        v_inv = D[tuple(D_inv[c])]
        # Length score
        score = length_score(v, v_inv)
        if np.isnan(score):
            pdb.set_trace()
        E_inv[tuple(c)] = score
        
    action.diffeo.variance = 1 - E / np.max(E)
    action.diffeo.variance_max = np.max(E)
    action.diffeo_inv.variance = 1 - E_inv / np.max(E_inv)
    action.diffeo_inv.variance_max = np.max(E_inv)
