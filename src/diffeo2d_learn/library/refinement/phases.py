from contracts import contract

import numpy as np


__all__ = ['PhaseInfo', 'get_phase_sequence']

class PhaseInfo():
    @contract(shape='array[2](int)',
              max_displ='array[2](float,>0,<=1)',
              grid='array[2](int)')
    def __init__(self, shape, max_displ, grid):
        self.shape = shape
        self.max_displ = max_displ
        self.grid = grid
        assert np.all(max_displ <= 1)
        assert np.all(max_displ >= 0)
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
    def get_cell_size(self):
        """ Returns the cell size in relative units """
        return self.max_displ / self.grid

            
    @contract(returns='array[2](float)')
    def get_displacement(self):
        return self.grid * 1.0 / self.shape
        
    def __str__(self):
        return ('Phase(shape=%s, displ=%s, grid=%s, cellsize=%s)' % 
                (self.shape, self.max_displ, self.grid, self.get_cell_size()))
        
@contract(orig_shape='seq[2](int)',
          min_shape='seq[2](int)',
          desired_resolution_factor='float,>0',
          search_grid='tuple((int,>=3),(int,>=3))',
          gamma='float,>1',
          max_displ='seq[2](float)')
def get_phase_sequence(orig_shape, desired_resolution_factor, search_grid, gamma,
                       max_displ, min_shape):
    max_displ = np.array(max_displ)
    search_grid = np.array(search_grid)
    orig_shape = np.array(orig_shape)
    min_shape = np.array(min_shape)
    
    # so, in the last phase, we will have:
    
    f = desired_resolution_factor
    last_shape = np.ceil(orig_shape * f).astype('int') 
    last_search_grid = search_grid 
    # for this to work, it means that the displacement is
    last_max_displ = last_search_grid * 1.0 / last_shape
    last_max_displ = np.minimum(last_max_displ, [1.0, 1.0])
    honor_min_shape = True
    
    last = PhaseInfo(grid=search_grid,
                     shape=np.array(last_shape),
                     max_displ=last_max_displ)
    
    phases = [last]
    
    while True:
        p = phases[-1]
        if np.all(p.max_displ >= max_displ):
            break
        p2_shape = np.floor(p.shape / gamma).astype('int')
        # make sure we are not undersampling too much
        if honor_min_shape: 
            p2_shape = np.maximum(p2_shape, min_shape)
        # now we know how much we want
        p2_max_displ = p.max_displ * gamma
        # this is only for very small grid sizes
        p2_max_displ = np.minimum(p2_max_displ, [1.0, 1.0])
        # so what would be the grid to realize it?
        p2_grid = np.ceil(p2_max_displ * p2_shape).astype('int') 
        
        assert np.all(p2_max_displ <= 1)
        assert np.all(p2_max_displ >= 0)
        p2 = PhaseInfo(grid=p2_grid, shape=p2_shape, max_displ=p2_max_displ)
        phases.append(p2)
        
    
        # TODO: make sure the resolution is increasing
#         
# - Phase(shape=[32 32], max_displ=[ 0.31864481  0.31864481], grid=[ 11.  11.] => solution discretization = [ 0.02896771  0.02896771])
# - Phase(shape=[32 32], max_displ=[ 0.24511139  0.24511139], grid=[ 8.  8.] => solution discretization = [ 0.03063892  0.03063892])
# - Phase(shape=[32 32], max_displ=[ 0.18854723  0.18854723], grid=[ 7.  7.] => solution discretization = [ 0.02693532  0.02693532])
# - Phase(shape=[33 33], max_displ=[ 0.14503633  0.14503633], grid=[ 5.  5.] => solution discretization = [ 0.02900727  0.02900727])
# - Phase(shape=[43 43], max_displ=[ 0.11156641  0.11156641], grid=[ 5.  5.] => solution discretization = [ 0.02231328  0.02231328])
# - Phase(shape=[57 57], max_displ=[ 0.08582031  0.08582031], grid=[ 5.  5.] => solution discretization = [ 0.01716406  0.01716406])
# - Phase(shape=[75 75], max_displ=[ 0.06601563  0.06601563], grid=[ 5.  5.] => solution discretization = [ 0.01320313  0.01320313])
# - Phase(shape=[98 98], max_displ=[ 0.05078125  0.05078125], grid=[ 5.  5.] => solution discretization = [ 0.01015625  0.01015625])
    
    phases = phases[::-1]
    
    if honor_min_shape:
        phases = fix_problems2(phases)
        
    
    return phases

def fix_problems(phases):
    # Let's fix some problems that might arise
    # basically it does not make sense to have the same shape 
    # but the discretization increases
    res = []
    for p in phases:
        if not res:
            res.append(p)
            continue
        
        prev = res[-1]
        # if two have the same shape
        if np.any(p.shape != prev.shape):
            res.append(p)
            continue
        
        # we require that the cell size is smaller 
        prev_size = prev.get_cell_size()
        p_size = p.get_cell_size()
        not_ok = np.all(p_size <= prev_size)
        
        if not_ok:
            continue
        else:
            res.append(p)
                    
    return res

def fix_problems2(phases):
    """ Here we ignore if the shape is the same """
    res = []
    for p in phases:
        if not res:
            res.append(p)
            continue
        
        prev = res[-1]
        # ignore if two have the same shape
        if np.any(p.shape != prev.shape):
            res.append(p)
                    
    return res
