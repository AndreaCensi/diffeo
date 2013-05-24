from .phases import get_phase_sequence
from bootstrapping_olympics import BootWithInternalLog
from bootstrapping_olympics.library.nuisances.shape import scipy_image_resample
from contracts import contract
from diffeo2c.resampling import diffeo_resample
from diffeo2d.diffeo_basic import diffeo_identity
from diffeo2d.plumbing import FlatStructure
from diffeo2d_learn import Diffeo2dEstimatorInterface
from diffeo2d_learn.library.fast.diffeo_estimator_fast import (
    DiffeomorphismEstimatorFaster)
import numpy as np
import warnings
warnings.warn('remove dependency')
 
__all__ = ['DiffeomorphismEstimatorDoubleRefine']


class DiffeomorphismEstimatorDoubleRefine(Diffeo2dEstimatorInterface, BootWithInternalLog):
    
    
    @contract(g='int,>1', gamma='float,>1',
              desired_resolution_factor='float',
              change_threshold='float,>=0')
    def __init__(self, g, gamma, desired_resolution_factor,
                 change_threshold, min_shape):
        '''
        
        :param max_displ:
        :param g:
        :param desired_resolution_factor: 1 = native resolution, >1 better
        '''
        # parameters
        self.desired_resolution_factor = desired_resolution_factor
        self.g = g
        self.gamma = gamma
        self.change_threshold = change_threshold
        self.min_shape = min_shape
        
        # variables
        self.estimators = None
        self.phases = None
        self.current_phase = None
        
    def set_max_displ(self, max_displ):
        self.max_displ = np.array(max_displ)

    def initialized(self):
        """ Returns true if the structures have already been initialized. """
        return self.current_phase is not None
    
    @contract(y_shape='seq[2](int)')
    def init_structures(self, y_shape):
        self.orig_shape = (y_shape[0], y_shape[1])
        
        print('max_displ: %s' % self.max_displ)
        
        search_grid = (self.g, self.g) 
        self.phases = get_phase_sequence(self.orig_shape,
                                    self.desired_resolution_factor,
                                    search_grid=search_grid,
                                    gamma=self.gamma,
                                    max_displ=self.max_displ,
                                    min_shape=self.min_shape)
        for p in self.phases:
            print('- %s' % p)
        
        self.estimators = []
        
        self.current_phase = 0
    
        phase = self.phases[self.current_phase]
        estimator = self._get_phase_estimator(phase.max_displ)
        estimator.set_guess(diffeo_identity(phase.shape))
        self.estimators.append(estimator)
        
        self.phase_obs = 0
        print('now using phase: %s' % phase)
        
        self.last_tmp_guess = None
        self.reached_end = False
        
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
        estimator = DiffeomorphismEstimatorFasterGuess(inference_method='order')
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

    def check_should_switch(self):
        check_every = 50
        if self.phase_obs % check_every != 0:
            return
        self.info('Checking at iteration %s' % self.phase_obs)
        estimator = self.estimators[self.current_phase]
        
        if self.last_tmp_guess is None:
            self.info('Creating first guess')
            self.last_tmp_guess = estimator.get_value()
            return
        
        # self.info('Creating new guess')
        cur_guess = estimator.get_value()

        
        mean_changes = np.mean(np.abs(cur_guess.d - self.last_tmp_guess.d))
        self.last_tmp_guess = cur_guess
        
        self.info('%d: Mean change since last guess: %f' 
                  % (self.phase_obs, mean_changes))
        
        # should_switch = self.phase_obs >= obs_per_phase
        should_switch = mean_changes <= self.change_threshold

        if should_switch:
            if self.current_phase < len(self.phases) - 1:
                self.info('Switching to next phase.')
                self.next_phase()
            else:
                self.info('Reached end of phases.')
                self.reached_end = True


    def display(self, report):
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

    def publish(self, pub):  # XXX
        return self.display(pub)    

    def merge(self, other):
        """ Merges the values obtained by "other" with ours. """
        raise ValueError()
    
class DiffeomorphismEstimatorFasterGuess(DiffeomorphismEstimatorFaster):
    
    @contract(guess='valid_diffeomorphism')
    def set_guess(self, guess):
        """ Sets the initial guess. """
        self.guess = guess
    
    def _create_flat_structure(self):
        fs = FlatStructure(shape=self.shape,
                           neighborarea=self.area, centers=self.guess)
        return fs
   



