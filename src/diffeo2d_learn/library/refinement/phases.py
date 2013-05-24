from contracts import contract
import numpy as np

__all__ = ['PhaseInfo', 'get_phase_sequence']

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
        resolution = self.max_displ / self.grid
        return ('Phase(shape=%s, max_displ=%s, grid=%s => solution discretization = %s)' % 
                (self.shape, self.max_displ, self.grid, resolution))
        
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
        p2_shape = np.floor(p.shape / gamma).astype('int')
        # make sure we are not undersampling too much 
        p2_shape = np.maximum(p2_shape, min_shape)
        # now we know how much we want
        p2_max_displ = p.max_displ * gamma
        # so what would be the grid to realize it?
        p2_grid = np.ceil(p2_max_displ * p2_shape) 
        
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
    
    return phases
