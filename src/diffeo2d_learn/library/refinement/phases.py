from bootstrapping_olympics.library.nuisances.shape.resample import (
    scipy_image_resample)
from contracts import contract
from diffeo2d import (Diffeomorphism2D, flat_structure_cache, add_border, togrid,
    diffeo_identity, diffeo_text_stats, diffeomorphism_to_rgb, diffeo_to_rgb_angle,
    diffeo_to_rgb_norm, diffeo_to_rgb_curv, angle_legend)
from diffeo2d_learn import Diffeo2dEstimatorInterface, logger
from diffeo2d_learn.library.fast.diffeo_estimator_fast import (
    DiffeomorphismEstimatorFaster)
from reprep.plot_utils import plot_vertical_line
import numpy as np
import time


class PhaseInfo():
    @contract(shape='array[2](int)',
              max_displ='array[2](float)',
              grid='array[2](int)')
    def __init__(self, shape, max_displ, grid):
        self.shape = shape
        self.max_displ = max_displ
        self.grid = grid
        
        # check that these are coherent
        identifiable = self.get_displacement() 
        ok = identifiable >= self.max_displ
        coherent = np.all(ok)
        if not coherent:
            msg = 'Combination not ok:\n'
            msg += ' - max_displ req: %s\n' % str(self.max_displ)
            msg += ' - identifiable: %s\n' % str(identifiable)
            msg += ' - shape: %s\n' % str(self.shape)
            msg += ' - grid: %s\n' % str(self.grid)
            
            raise ValueError(msg)
        
    @contract(returns='array[2](float)')
    def get_displacement(self):
        return self.grid * 1.0 / self.shape
        
    def __str__(self):
        return ('Phase(shape=%s, max_displ=%s, grid=%s)' % 
                (self.shape, self.max_displ, self.grid))
        
@contract(orig_shape='seq[2](int)',
          desired_resolution_factor='float,>0',
          search_grid='tuple((int,>=3),(int,>=3))',
          gamma='float,>1',
          max_displ='seq[2](float)')
def get_phase_sequence(orig_shape, desired_resolution_factor, search_grid, gamma,
                       max_displ):
    max_displ = np.array(max_displ)
    search_grid = np.array(search_grid)
    # so, in the last phase, we will have:
    orig_shape = np.array(orig_shape)
    f = desired_resolution_factor
    last_shape = np.ceil(orig_shape * f).astype('int') 
    last_search_grid = search_grid 
    # for this to work, it means that the displacement is
    last_max_displ = last_search_grid * 1.0 / last_shape
    
    last = PhaseInfo(grid=search_grid,
                     shape=np.array(last_shape),
                     max_displ=last_max_displ)
    
    phases = [last]
    
    while True:
        p = phases[-1]
        if np.all(p.max_displ >= max_displ):
            break
        p2_grid = search_grid
        p2_shape = np.floor(p.shape / gamma).astype('int') 
        p2_max_displ = p.max_displ * gamma
        p2 = PhaseInfo(grid=p2_grid, shape=p2_shape, max_displ=p2_max_displ)
        phases.append(p2)
    
    phases = phases[::-1]
    
    return phases
