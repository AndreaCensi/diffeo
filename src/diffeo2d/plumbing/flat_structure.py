from .flattening import Flattening, coords_iterate
from compmake.utils import memoize_simple
from contracts import contract
from diffeo2d import diffeo_identity
from numpy.testing import assert_allclose
import numpy as np
import warnings
from diffeo2d.misc_utils import cmap
from diffeo2d.diffeo_basic import dmod
from conf_tools.utils import check_is_in

__all__ = ['FlatStructure', 'flat_structure_cache', 'add_border', 'togrid']

class FlatStructure(object):
    """ 
        This structure describes the topology of the image.
        It allows to associate an area (subset of pixels) to each pixel. 
        
        There are two main modes: plane and torus.
        
        One strong limitation is that each pixel is associated to the same
        number of neighbors.
    """
          
    @contract(shape='tuple((H,int,>=1),(W,int,>=1))',
              neighborarea='tuple((int,>=1),(int,>=1))',
              centers='None|(array[HxWx2],valid_diffeomorphism)',
              topology='str')
    def __init__(self, shape, neighborarea, centers=None, topology='plane'):
        '''
        :param shape:
        :param neighborarea:
        :param centers: if not None, area around centers
            
            Suppose 
                shape = (H, W)
                nighborarea = (X, Y)
                A = X * Y
                N = H * W
            Then 
                self.neighbor_indices_flat  
            is a K x N array.

        '''
        # for each sensel, create an area 
        cmg = cmap(np.array(neighborarea))
        
        # if the area size is even, it is bumbed to the next integer
        assert cmg.shape[0] >= neighborarea[0]
        assert cmg.shape[1] >= neighborarea[1]
        
        self.area_shape = cmg.shape[0], cmg.shape[1]
        self.shape = shape
        self.H, self.W = shape
        self.X = self.area_shape[0]
        self.Y = self.area_shape[1]
        self.N = self.H * self.W
        self.A = self.X * self.Y
        
        self.topology = topology
        check_is_in(topology, self.topology, ['torus', 'plane'])
        
        # this is the important state
        self.neighbor_indices_flat = np.zeros((self.N, self.A), 'int32')
    
        # logger.info('Creating Flattening..')
        self.flattening = Flattening.by_rows(tuple(shape))
        # logger.info('..done')
        
        if centers is None:
            self.centers = diffeo_identity(shape)
        else:
            if centers.dtype == 'float':
                # continuous diffeo
                centers = np.round(centers).astype('int')
            self.centers = centers
            
        for coord in coords_iterate(shape):
            k = self.flattening.cell2index[coord]
            cm = cmg.copy()
            
            center = self.centers[coord]      
            cm[:, :, 0] += center[0]
            cm[:, :, 1] += center[1]
            # torus topology here
            if self.topology == 'torus':
                cm[:, :, 0] = cm[:, :, 0] % shape[0]  
                cm[:, :, 1] = cm[:, :, 1] % shape[1]
            elif self.topology == 'plane':
                for i in range(2):
                    # move to the border
                    cmin = cm[:, :, i].min()
                    cmax = cm[:, :, i].max()
                    if cmin < 0:
                        cm[:, :, i] -= cmin
                    if cmax >= shape[i]:
                        cm[:, :, i] -= (cmax - (shape[i] - 1))                    
            else:
                assert False

            for i in range(2):
                assert cm[:, :, i].min() >= 0
                assert cm[:, :, i].max() < shape[i]

                
            indices = np.zeros(self.area_shape, 'int32')
            for a, b in coords_iterate(self.area_shape):
                c = tuple(cm[a, b, :])
                indices[a, b] = self.flattening.cell2index[c]
    
            # XXX using numpy's flattening 
            indices = np.array(indices.flat)
            # warnings.warn('remove bias due to ordering')
            # indices = np.random.permutation(indices)
            self.neighbor_indices_flat[k, :] = indices  

    # k < N, index < A
    @contract(k='int,>=0', neighbor_index='int,>=0', returns='seq[2](int)')
    def neighbor_cell(self, k, neighbor_index):
        j = self.neighbor_indices_flat[k][neighbor_index]
        return self.flattening.index2cell[j]
    
    @contract(value='array[HxW]|array[HxWxC]', returns='array[NxA]|array[NxAxC]')
    def ndvalues2unrolledneighbors(self, value):
        if value.ndim == 3:
            return self.image2unrolledneighbors(value)
        if value.ndim == 2:
            return self.values2unrolledneighbors(value)
        raise NotImplemented
    
    @contract(value='array[HxW]|array[HxWxC]', returns='array[NxA]|array[NxAxC]')
    def ndvalues2repeated(self, value):
        if value.ndim == 3:
            return self.image2repeated(value)
        if value.ndim == 2:
            return self.values2repeated(value)
        raise NotImplemented
        
    @contract(value='array[HxW]', returns='array[NxA]')
    def values2unrolledneighbors(self, value, out=None):
        # first convert the array to unrolled N
        valueflat = self.flattening.rect2flat(value)
        warnings.warn('Not tested yet')
        # Alternative:
        #  return valueflat[self.neighbor_indices_flat]
        return valueflat.take(self.neighbor_indices_flat, out=out)

    @contract(value='array[HxW]', returns='array[NxA]')
    def values2repeated(self, value):
        valueflat = self.flattening.rect2flat(value)
        N, A = self.neighbor_indices_flat.shape
        return np.repeat(valueflat.reshape((N, 1)), A, axis=1)
        
    @contract(value='array[HxWxC]', returns='array[NxAxC]')
    def image2unrolledneighbors(self, value):
        _, _, C = value.shape
        N, A = self.neighbor_indices_flat.shape
        valueflat = np.zeros((N, A, C), value.dtype)
        for c in range(C):
            valueflat[:, :, c] = self.values2unrolledneighbors(value[:, :, c])
        return valueflat

    @contract(value='array[HxWxC]', returns='array[NxAxC]')
    def image2repeated(self, value):
        _, _, C = value.shape
        res = np.zeros((self.N, self.A, C), value.dtype)
        for c in range(C):
            res[:, :, c] = self.values2repeated(value[:, :, c])
        return res

    @memoize_simple
    @contract(returns='array[NxA]')
    def get_distances(self):
        """ This returns the distance of each neighbor to the pixel """
        D = np.zeros((self.N, self.A))
        for i in xrange(self.N):
            pi = self.flattening.index2cell[i]
            for jj in xrange(self.A):
                j = self.neighbor_indices_flat[i, jj]
                pj = self.flattening.index2cell[j]
                dx = pi[0] - pj[0]
                dy = pi[1] - pj[1]
                dxn = dmod(dx, self.shape[0] / 2)
                dyn = dmod(dy, self.shape[1] / 2)
                d = np.hypot(dxn, dyn)
                D[i, jj] = d
        return D 
    
    @memoize_simple
    @contract(returns='array[NxA]')
    def get_distances_to_area_center(self):
        """ 
            This returns the distance of each neighbor to the center 
            of the area border. This is the same thing as get_distances()
            only if the area center is on the nominal pixel. 
        """
        D = np.zeros((self.N, self.A))
        for i in xrange(self.N):
            pi = self.flattening.index2cell[i]
            area_center = self.get_center_for_cell_area(pi)
            for jj in xrange(self.A):
                j = self.neighbor_indices_flat[i, jj]
                pj = self.flattening.index2cell[j]
                dx = area_center[0] - pj[0]
                dy = area_center[1] - pj[1]
                dxn = dmod(dx, self.shape[0] / 2)
                dyn = dmod(dy, self.shape[1] / 2)
                d = np.hypot(dxn, dyn)
                D[i, jj] = d
        return D 
    
    @contract(cell='seq[2](int)', returns='seq[2](int)')
    def get_center_for_cell_area(self, cell):
        res = self.centers[tuple(cell)]
        return res.astype('int')
        
    @memoize_simple
    @contract(returns='array[NxA]')
    def get_distances_to_area_border(self):
        """ This returns the distance of each neighbor to the border of the area """
        D = np.zeros((self.N, self.A))
        Xd = np.floor(self.X / 2.0)
        Yd = np.floor(self.Y / 2.0)
        for i in xrange(self.N):
            pi = self.flattening.index2cell[i]
            area_center = self.get_center_for_cell_area(pi)

            for jj in xrange(self.A):
                j = self.neighbor_indices_flat[i, jj]
                pj = self.flattening.index2cell[j]
                dx = area_center[0] - pj[0]
                dy = area_center[1] - pj[1]
                dxn = dmod(dx, self.shape[0] / 2)
                dyn = dmod(dy, self.shape[1] / 2)
                d_up = np.abs((-Yd) - dyn)
                d_down = np.abs((+Yd) - dyn)
                d_left = np.abs((-Xd) - dxn)
                d_right = np.abs((+Xd) - dxn)
                D[i, jj] = np.min([d_up, d_down, d_left, d_right])
        return D 
        
    @contract(v='array[NxA]', returns='array[HxWxXxY],N=H*W,A=X*Y')
    def unrolled2multidim(self, v):
        """ De-unrolls both dimensions to obtain a 4d vector. """
        # Let's make sure we understand what's going on...
        assert_allclose((self.N, self.A), v.shape)
        res = np.zeros((self.H, self.W, self.X, self.Y), v.dtype)
        for i, j in coords_iterate((self.H, self.W)):
            k = self.flattening.cell2index[i, j]
            res[i, j, :, :] = self.neighbor2area(int(k), v[k, :])
        return res
        
    @contract(k='int', x='array[A]', returns='array[HxW]')
    def neighbor2area(self, k, x):
        assert 0 <= k < self.N
        assert x.size == self.A
        # Using numpy's flattening convention (see also above)
        return np.reshape(x, self.area_shape)
        

@contract(x='array[HxWxXxY]', returns='array[(H*X)x(W*Y)]')
def togrid(x):
    H, W, X, Y = x.shape
    U = H * X
    V = W * Y
    res = np.zeros((U, V), x.dtype)
    for i, j in coords_iterate((H, W)):
        rect = x[i, j, :, :]
        ust = i * X
        vst = j * Y
        res[ust:ust + X, vst:vst + Y] = rect
    return res
    
@contract(x='array[HxWxXxY]', returns='array[HxWx(X+2)x(Y+2)]')
def add_border(x, fill=np.nan):
    H, W, X, Y = x.shape
    res = np.zeros((H, W, X + 2, Y + 2), x.dtype)
    res.fill(fill)
    for i, j in coords_iterate((H, W)):
        res[i, j, 1:-1, 1:-1] = x[i, j, :, :] 
    return res 

@memoize_simple
def flat_structure_cache(*args, **kwargs):
    return FlatStructure(*args, **kwargs)
