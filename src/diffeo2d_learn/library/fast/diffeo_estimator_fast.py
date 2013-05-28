from contracts import contract
from diffeo2d import (Diffeomorphism2D, flat_structure_cache, add_border, togrid,
    diffeo_identity, diffeo_text_stats, diffeomorphism_to_rgb, diffeo_to_rgb_angle,
    diffeo_to_rgb_norm, diffeo_to_rgb_curv, angle_legend)
from diffeo2d_learn import Diffeo2dEstimatorInterface, logger
from reprep import rgb_zoom, scale
from reprep.plot_utils import plot_vertical_line
import numpy as np
import time

__all__ = ['DiffeomorphismEstimatorFaster']
    
class DiffeomorphismEstimatorFaster(Diffeo2dEstimatorInterface):
    ''' 
        This faster version uses vector operations. The meat of
        the flattingeing is in the FlatStructure class.
    '''

    Order = 'order'
    Similarity = 'sim'
    
    @contract(inference_method='str')
    def __init__(self, inference_method):
        """ 
            :param max_displ: Maximum displacement  
            :param inference_method: order, sim
        """
        self.shape = None
        self.last_y0 = None
        self.last_y1 = None
        self.inference_method = inference_method
        
        accepted = [DiffeomorphismEstimatorFaster.Order,
                    DiffeomorphismEstimatorFaster.Similarity]
        if self.inference_method not in accepted:
            msg = ('I need one of %s; found %s' % 
                   (accepted, inference_method))
            raise ValueError(msg)
        
        self.num_samples = 0

        self.buffer_NA = None
    
        self.max_displ = None
    
    def set_max_displ(self, max_displ):
        self.max_displ = np.array(max_displ)
        
    def __str__(self):
        return '%s(max_displ=%s)' % (type(self).__name__, self.max_displ)


    def initialized(self):
        """ Returns true if the structures have already been initialized. """
        return self.shape is not None
             
    @contract(y0='array[MxN]', y1='array[MxN]')
    def update(self, y0, y1):
        if y0.dtype == np.uint8:
            y0 = (y0 / 255.0).astype('float32')
            y1 = (y1 / 255.0).astype('float32')
        self.num_samples += 1

        # init structures if not already
        if not self.initialized():
            self.init_structures(y0.shape)

        # check shape didn't change
        if self.shape != y0.shape:
            msg = 'Shape changed from %s to %s.' % (self.shape, y0.shape)
            raise ValueError(msg)

        # remember last images
        self.last_y0 = y0
        self.last_y1 = y1
        
        # The _update_scalar function is typically faster
        check_times = False
        ts = []
        ts.append(time.time())
        if check_times:
            self._update_vectorial(y0, y1)
        ts.append(time.time())
        self._update_scalar(y0, y1)
        ts.append(time.time())
        if check_times:
            delta = np.diff(ts)
            msg = 'Update times: vect %5.3f scal %5.3f seconds' % (delta[0], delta[1])
            logger.info(msg)
        
    def _update_scalar(self, y0, y1):
        # unroll the Y1 image
        Y1 = self.flat_structure.values2unrolledneighbors(y1, out=self.buffer_NA)
        y0_flat = self.flat_structure.flattening.rect2flat(y0)
        
        order_comp = np.array(range(self.area_size), dtype='float32')
        
        for k in xrange(self.nsensels):
            diff = np.abs(y0_flat[k] - Y1[k, :])
            
            if self.inference_method == DiffeomorphismEstimatorFaster.Order:
                order = np.argsort(diff)
                # this variant was actually quite slower:
                # diff_order = scale_score(diff, kind='quicksort')
                self.neig_eord_score[k, order] += order_comp 
            elif self.inference_method == DiffeomorphismEstimatorFaster.Similarity:
                self.neig_esim_score[k, :] += diff
            else:
                msg = 'Unknown inference method %r' % self.inference_method
                raise ValueError(msg)
                
            self.neig_esimmin_score[k] += np.min(diff)
            
            
    def _update_vectorial(self, y0, y1):
        Y0 = self.flat_structure.values2repeated(y0)
        Y1 = self.flat_structure.values2unrolledneighbors(y1, out=self.buffer_NA)
        
        difference = np.abs(Y0 - Y1)
        
        if self.inference_method == DiffeomorphismEstimatorFaster.Order:
            # Yes, double argsort(). This is correct.
            # (but slow; seee update_scalar above)
            simorder = np.argsort(np.argsort(difference, axis=1), axis=1)
            self.neig_eord_score += simorder
        
        elif self.inference_method == DiffeomorphismEstimatorFaster.Similarity:
            self.neig_esim_score += difference
        else:
            msg = 'Unknown inference method %r' % self.inference_method
            raise ValueError(msg)

                    
        self.neig_esimmin_score += np.min(difference, axis=1)
        
    @contract(y_shape='seq[2](int)')
    def init_structures(self, y_shape):
        self.shape = (y_shape[0], y_shape[1])
        self.nsensels = self.shape[0] * self.shape[1]
        # for each sensel, create an area
        self.area = np.ceil(self.max_displ * np.array(self.shape)).astype('int32')
        
        # ensure it's an odd number of pixels
        for i in range(2):
            if self.area[i] % 2 == 0:
                self.area[i] += 1
        self.area = (int(self.area[0]), int(self.area[1]))
        self.area_size = self.area[0] * self.area[1]

        logger.debug(' Field Shape: %s' % str(self.shape))
        logger.debug('    Fraction: %s' % str(self.max_displ))
        logger.debug(' Search area: %s' % str(self.area))
        # logger.debug('Creating FlatStructure...')
        self.flat_structure = self._create_flat_structure()
        # logger.debug('done creating')

        buffer_shape = (self.nsensels, self.area_size)
        if self.inference_method == DiffeomorphismEstimatorFaster.Similarity:   
            self.neig_esim_score = np.zeros(buffer_shape, 'float32')
        elif self.inference_method == DiffeomorphismEstimatorFaster.Order:
            self.neig_eord_score = np.zeros(buffer_shape, 'float32')
        else:
            assert False
              
        self.neig_esimmin_score = np.zeros(self.nsensels)
        
        # initialize a buffer of size NxA
        self.buffer_NA = np.zeros(buffer_shape, 'float32') 
    
    def _create_flat_structure(self):
        """ It is a method so it can be redefined. """
        return flat_structure_cache(self.shape, self.area)
        
    def display(self, report):
        if not self.initialized():
            report.text('notice', 'Cannot display() because not initialized.')
            return
        
        report.text('estimator', type(self).__name__)
        report.data('num_samples', self.num_samples)
        
        score = self._get_score()
        flattening = self.flat_structure.flattening
        min_score = flattening.flat2rect(np.min(score, axis=1))
        max_score = flattening.flat2rect(np.max(score, axis=1))
        caption = 'minimum and maximum score per pixel across neighbors'
        f = report.figure('scores', caption=caption)
        f.data('min_score', min_score).display('scale')
        f.data('max_score', max_score).display('scale')
        
        f = report.figure(cols=4)
        
        def make_best(x):
            return x == np.min(x, axis=1)
    
        max_d = int(np.ceil(np.hypot(np.floor(self.area[0] / 2.0),
                                     np.floor(self.area[1] / 2.0))))
        safe_d = int(np.floor(np.min(self.area) / 2.0))
        
        
        def plot_safe(pylab):
            plot_vertical_line(pylab, safe_d, 'g--')
            plot_vertical_line(pylab, max_d, 'r--')
            
        if self.shape[0] <= 64: 
            as_grid = self.make_grid(score)
            f.data_rgb('grid', rgb_zoom(scale(as_grid), 4))
        else:
            report.text('warn', 'grid visualization not done because too big')
            
        distance_to_border = distance_to_border_for_best(self.flat_structure, score) 
        distance_to_center = distance_from_center_for_best(self.flat_structure, score)
        
        bdist_scale = dict(min_value=0, max_value=max_d, max_color=[0, 1, 0])
        d = report.data('distance_to_border', distance_to_border).display('scale', **bdist_scale)
        d.add_to(f, caption='Distance to border of best guess, white=0, green=%d' % max_d)
        
        cdist_scale = dict(min_value=0, max_value=max_d, max_color=[1, 0, 0])
        d = report.data('distance_to_center', distance_to_center).display('scale', **cdist_scale)
        d.add_to(f, caption='Distance to center of best guess, white=0, red=%d' % max_d)
        
        bins = np.array(range(max_d + 2))
        # values will be integers (0, 1, 2, ...), center bins appropriately
        bins = bins - 0.5
        with f.plot('distance_to_border_hist') as pylab:
            pylab.hist(distance_to_border.flat, bins)
        
        caption = 'Red line: on border; Green line (red-1): safe to be here.'
        with f.plot('distance_to_center_hist', caption=caption) as pylab:
            pylab.hist(distance_to_center.flat, bins)
            plot_safe(pylab)
    
    def _get_score(self):
        if self.inference_method == DiffeomorphismEstimatorFaster.Order:
            return self.neig_eord_score

        if self.inference_method == DiffeomorphismEstimatorFaster.Similarity:
            return self.neig_esim_score
        
        assert False
    
        
    @contract(score='array[NxA]', returns='array[UxV]')  # ,U*V=N*A') not with border
    def make_grid(self, score):
        fourd = self.flat_structure.unrolled2multidim(score)  # HxWxXxY
        return togrid(add_border(fourd))
        
    def get_value(self):
        ''' 
            Find maximum likelihood estimate for diffeomorphism looking 
            at each pixel singularly. 
            
            Returns a Diffeomorphism2D.
        '''
        if not self.initialized():
            msg = 'Cannot summarize() because not initialized yet.'
            raise Diffeo2dEstimatorInterface.NotReady(msg)
        certainty = np.zeros(self.shape, dtype='float32')
        certainty.fill(np.nan)
        
        dd = diffeo_identity(self.shape)
        dd[:] = -1
        for i in range(self.nsensels):
            
            if self.inference_method == DiffeomorphismEstimatorFaster.Order:
                eord_score = self.neig_eord_score[i, :]
                best = np.argmin(eord_score)
            
            if self.inference_method == DiffeomorphismEstimatorFaster.Similarity:
                esim_score = self.neig_esim_score[i, :]
                best = np.argmin(esim_score)
                
            jc = self.flat_structure.neighbor_cell(i, best)
            ic = self.flat_structure.flattening.index2cell[i]
            
            if self.inference_method == DiffeomorphismEstimatorFaster.Order:
                certain = -np.min(eord_score) / np.mean(eord_score)
                
            if self.inference_method == DiffeomorphismEstimatorFaster.Similarity:
                first = np.sort(esim_score)[:10]
                certain = -(first[0] - np.mean(first[1:]))
                # certain = -np.min(esim_score) / np.mean(esim_score)
#            certain = np.min(esim_score) / self.num_samples
#            certain = -np.mean(esim_score) / np.min(esim_score)
            
            dd[ic[0], ic[1], 0] = jc[0]
            dd[ic[0], ic[1], 1] = jc[1]
            certainty[ic[0], ic[1]] = certain
        
        certainty = certainty - certainty.min()
        vmax = certainty.max()
        if vmax > 0:
            certainty *= (1.0 / vmax)
            
        return Diffeomorphism2D(dd, certainty)
    
    def publish(self, pub):
        diffeo = self.summarize() 
        
        pub.array_as_image('mle', diffeomorphism_to_rgb(diffeo.d))
        pub.array_as_image('angle', diffeo_to_rgb_angle(diffeo.d))
        pub.array_as_image('norm', diffeo_to_rgb_norm(diffeo.d, max_value=10))
        pub.array_as_image('curv', diffeo_to_rgb_curv(diffeo.d))
        pub.array_as_image('variance', diffeo.variance, filter='scale')

        pub.text('num_samples', self.num_samples)
        pub.text('statistics', diffeo_text_stats(diffeo.d))
        pub.array_as_image('legend', angle_legend((50, 50)))

        n = 20
        M = None
        for i in range(n):  # @UnusedVariable
            c = self.flattening.random_coords()
            Mc = self.get_similarity(c)
            if M is None:
                M = np.zeros(Mc.shape)
                M.fill(np.nan)

            ok = np.isfinite(Mc)
            Mmax = np.nanmax(Mc)
            if Mmax < 0:
                Mc = -Mc
                Mmax = -Mmax
            if Mmax > 0:
                M[ok] = Mc[ok] / Mmax

        pub.array_as_image('coords', M, filter='scale')

        if self.last_y0 is not None:
            y0 = self.last_y0
            y1 = self.last_y1
            none = np.logical_and(y0 == 0, y1 == 0)
            x = y0 - y1
            x[none] = np.nan
            pub.array_as_image('motion', x, filter='posneg')

    def merge(self, other):
        """ Merges the values obtained by "other" with ours. """
        if not other.initialized():
            # nothing to do
            return
        if not self.initialized() and other.initialized():
            # Let's initialized like the other
            self.init_structures(other.shape)
            self.num_samples = other.num_samples
            self.neig_esimmin_score = other.neig_esimmin_score
            if self.inference_method == DiffeomorphismEstimatorFaster.Similarity:
                self.neig_esim_score = other.neig_esim_score
            if self.inference_method == DiffeomorphismEstimatorFaster.Order:
                self.neig_eord_score = other.neig_eord_score
            return
        
        if self.inference_method != other.inference_method:
            raise ValueError()
            
        assert other.initialized(), "Can only merge initialized structures"
        logger.info('merging %s + %s samples' % (self.num_samples, other.num_samples))

        self.num_samples += other.num_samples
        self.neig_esimmin_score += other.neig_esimmin_score

        if self.inference_method == DiffeomorphismEstimatorFaster.Order:
            self.neig_eord_score += other.neig_eord_score
        elif self.inference_method == DiffeomorphismEstimatorFaster.Similarity:
            self.neig_esim_score += other.neig_esim_score
        else:
            assert False

@contract(score='array[NxA]', returns='array[HxW],H*W=N')
def distance_to_border_for_best(flat_structure, score):
    N, _ = score.shape
    best = np.argmin(score, axis=1)
    assert best.shape == (N,)
    D = flat_structure.get_distances_to_area_border()
    res = np.zeros(N)
    for i in range(N):
        res[i] = D[i, best[i]]
    return flat_structure.flattening.flat2rect(res)

@contract(score='array[NxA]', returns='array[HxW],H*W=N')
def distance_from_center_for_best(flat_structure, score):
    N, _ = score.shape
    best = np.argmin(score, axis=1)
    assert best.shape == (N,)
    D = flat_structure.get_distances_to_area_center()
    res = np.zeros(N)
    for i in range(N):
        res[i] = D[i, best[i]]
    return flat_structure.flattening.flat2rect(res)
