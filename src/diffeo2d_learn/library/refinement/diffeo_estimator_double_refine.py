from .phases import get_phase_sequence
from bootstrapping_olympics.library.nuisances import scipy_image_resample
from contracts import contract
from diffeo2c import diffeo_resample
from diffeo2d import FlatStructure, diffeo_identity
from diffeo2d_learn import Diffeo2dEstimatorInterface
from diffeo2d_learn.library import DiffeomorphismEstimatorFaster
import numpy as np
import warnings
from numpy.testing.utils import assert_allclose
warnings.warn('remove dependency')
 
__all__ = ['DiffeomorphismEstimatorDoubleRefine']


class DiffeomorphismEstimatorDoubleRefine(Diffeo2dEstimatorInterface):
    
    """ Does not support parallel merging yet. """
    
    @contract(g='int,>1', gamma='float,>1',
              desired_resolution_factor='float',
              change_threshold='float,>=0')
    def __init__(self, g, gamma, desired_resolution_factor,
                 change_threshold, min_shape, inference_method='order'):
        '''
        
        :param max_displ:
        :param g:
        :param desired_resolution_factor: 1 = native resolution, >1 better
        '''
        # parameters
        self.inference_method = inference_method
        self.desired_resolution_factor = desired_resolution_factor
        self.g = g
        self.gamma = gamma
        self.change_threshold = change_threshold
        self.min_shape = min_shape
        
        # variables
        self.estimators = None
        self.phases = None
        self.current_phase = None
        
        self.total_obs = 0
        
    def set_max_displ(self, max_displ):
        self.max_displ = np.array(max_displ)

    def initialized(self):
        """ Returns true if the structures have already been initialized. """
        return self.current_phase is not None
    
    @contract(y_shape='seq[2](int)')
    def init_structures(self, y_shape):
        self.orig_shape = (y_shape[0], y_shape[1])
        
        self.info('max_displ: %s' % self.max_displ)
        
        search_grid = (self.g, self.g) 
        self.phases = get_phase_sequence(self.orig_shape,
                                    self.desired_resolution_factor,
                                    search_grid=search_grid,
                                    gamma=self.gamma,
                                    max_displ=self.max_displ,
                                    min_shape=self.min_shape)
        for p in self.phases:
            self.info('- %s' % p)
        
        self.estimators = []
        
        self.current_phase = 0
    
        phase = self.phases[self.current_phase]
        estimator = self._get_phase_estimator(phase.max_displ)
        estimator.set_guess(diffeo_identity(phase.shape))
        self.estimators.append(estimator)
        
        self.phase_obs = 0
        self.info('now using phase: %s' % phase)
        
        self.last_tmp_guess = None
        self.reached_end = False
        
    def __str__(self):
        if self.current_phase is None:
            return 'DERefine(not-initialized)'
        # phase = self.phases[self.current_phase]
        return 'DERefine(phase=%s,obs=%s;%s)' % (self.current_phase, self.phase_obs, self.estimators[-1])
    
    def next_phase(self):
        """ Switches to the next phase. """
        cur_estimator = self.estimators[self.current_phase]
        cur_diffeo = cur_estimator.get_value()
        
        next_phase = self.phases[self.current_phase + 1]
        next_estimator = self._get_phase_estimator(next_phase.max_displ)
        # resample
        cur_diffeo_upsampled = diffeo_resample(cur_diffeo.d, next_phase.shape) 

        next_estimator.set_guess(cur_diffeo_upsampled)
        self.estimators.append(next_estimator)
        
        self.current_phase += 1
        self.phase_obs = 0
        
        self.last_tmp_guess = None
        
    @contract(max_displ='seq[2](>0,<1)')
    def _get_phase_estimator(self, max_displ):
        estimator = DiffeomorphismEstimatorFasterGuess(inference_method=self.inference_method)
        estimator.set_max_displ(max_displ)
        return estimator
    
    @contract(y0='array[MxN]', y1='array[MxN]')
    def update(self, y0, y1):
        # init structures if not already
        if not self.initialized():
            self.init_structures(y0.shape)

        phase = self.phases[self.current_phase]
        estimator = self.estimators[self.current_phase]
        target_shape = phase.shape 

        y0 = scipy_image_resample(y0, target_shape)
        y1 = scipy_image_resample(y1, target_shape)
        
        estimator.update(y0, y1)
        
        self.phase_obs += 1
        self.check_should_switch()

        self.total_obs += 1        

    def info(self, s):
        if self.current_phase is None:
            prefix = 'not initialized'
        else:
            phase = self.phases[self.current_phase]
            prefix = ('obs %d phase #%d shape %s it %5d' % 
                      (self.total_obs, self.current_phase,
                        phase.shape, self.phase_obs))
        Diffeo2dEstimatorInterface.info(self, prefix + ':' + s)
        
    def check_should_switch(self):
        check_every = 50
        if self.phase_obs % check_every != 0:
            return
        
        estimator = self.estimators[self.current_phase]
        
        if self.last_tmp_guess is None:
            self.info('Creating first guess')
            self.last_tmp_guess = estimator.get_value()
            return
        
        # self.info('Creating new guess')
        cur_guess = estimator.get_value()

        changes = np.abs(cur_guess.d - self.last_tmp_guess.d)
        bins = np.array(range(10)) - 0.5
        h_changes, _ = np.histogram(changes, bins=bins, density=True)
        assert_allclose(np.sum(h_changes), 1.0)
        h_changes_desc = ' '.join(['%d=%.5f' % x for x in enumerate(h_changes)])
        self.info('changes:\n%s' % h_changes_desc)
        # self.info('change\npercentile: %s\n%s' % (p, np.percentile(changes, p)))
        self.last_tmp_guess = cur_guess
        frac_stable = h_changes[0]
        self.info('Fraction stable: %s' % h_changes[0])
        mean_changes = np.mean(changes)
        self.info('Mean change since last guess: %f' % (mean_changes))
        # should_switch = self.phase_obs >= obs_per_phase
        should_switch = mean_changes <= self.change_threshold
        should_switch = frac_stable >= 0.8
        
        if should_switch:
            if self.current_phase < len(self.phases) - 1:
                self.info('Switching to next phase.')
                self.next_phase()
            else:
                self.info('Reached end of phases.')
                self.reached_end = True


    def display(self, report):
        if not self.initialized():
            report.text('warning', 'Estimator not initialized')
            return
        for i, e in enumerate(self.estimators):
            with report.subsection('phase%d' % i) as sub:
                e.display(sub) 
        
    def get_value(self):
        if not self.initialized():
            msg = 'Cannot summarize() because not initialized yet.'
            raise Diffeo2dEstimatorInterface.NotReady(msg)
        
        # here we should not necessarily choose the last
        if len(self.estimators) >= 2:
            if self.reached_end:
                last = self.estimators[-1]
            else:
                # the last one completed
                last = self.estimators[-2]
        else:
            last = self.estimators[-1]
        est = last.get_value()
        ests = est.resample(self.orig_shape) 
        return ests

    def publish(self, pub):
        return self.display(pub)    

    def merge(self, other):  # @UnusedVariable
        """ Merges the values obtained by "other" with ours. """
        msg = 'DiffeomorphismEstimatorDoubleRefine does not allow merging.'
        raise NotImplementedError(msg)
    
class DiffeomorphismEstimatorFasterGuess(DiffeomorphismEstimatorFaster):
    
    @contract(guess='valid_diffeomorphism')
    def set_guess(self, guess):
        """ Sets the initial guess. """
        self.guess = guess
    
    def _create_flat_structure(self):
        fs = FlatStructure(shape=self.shape,
                           neighborarea=self.area, centers=self.guess)
        return fs
   



