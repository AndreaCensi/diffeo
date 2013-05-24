from contracts import contract
from diffeo2d_learn import get_diffeo2dlearn_config
from diffeo2dds import DiffeoAction
from diffeo2dds_learn import DiffeoActionEstimatorInterface

__all__ = ['DiffeoActionEstimatorSimple']


class DiffeoActionEstimatorSimple(DiffeoActionEstimatorInterface):

    @contract(diffeo2d_estimator='str|code_spec')
    def __init__(self, diffeo2d_estimator): 
        self.diffeo2d_estimator = diffeo2d_estimator
       
    def set_max_displ(self, max_displ):
        self.max_displ = max_displ
    
        self.est = self._new_estimator() 
        self.est_inv = self._new_estimator()

    def _new_estimator(self):
        """ Instances a new estimator. """
        config = get_diffeo2dlearn_config()
        _, estimator = \
           config.diffeo2d_estimators.instance_smarter(self.diffeo2d_estimator)
        estimator.set_max_displ(self.max_displ)
        return estimator            

    def update(self, y0, y1):
        est = self.est
        est_inv = self.est_inv
        
        # XXX: cleaning up with state or not
        if y0.ndim == 3:
            # if there are 3 channels...
            for ch in range(3):
                est.update(y0[:, :, ch], y1[:, :, ch])
                est_inv.update(y1[:, :, ch], y0[:, :, ch])
        else:
            assert y0.ndim == 2
            est.update(y0, y1)
            est_inv.update(y1, y0)
            
    @contract(returns=DiffeoAction)
    def get_value(self):
        ''' 
            Returns the estimated DiffeoAction.
        '''
        diffeo = self.est.get_value()
        diffeo_inv = self.est_inv.get_value()
                
        name = 'uninterpreted'
        action = DiffeoAction(name, diffeo, diffeo_inv, original_cmd=None)
        return action

    def display(self, report): 
        with report.subsection('forward') as sub:
            self.est.display(sub)
        with report.subsection('backward') as sub:
            self.est_inv.display(sub)
            
    def merge(self, other):
        self.est.merge(other.est)
        self.est_inv.merge(other.est_inv)
        
        
