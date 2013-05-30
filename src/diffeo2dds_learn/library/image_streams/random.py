from diffeo2dds_learn import ImageStream
from contracts import contract
import numpy as np
import warnings
# from procgraph_cv.opencv_utils import smooth

__all__ = ['RandomImageStream', 'CoherentRandomImageStream']

class RandomImageStream(ImageStream):
    
    @contract(shape='seq[2](int,>=1)', seed='int')
    def __init__(self, shape, seed):
        self.seed = seed
        warnings.warn('seed not implemented')
        self.shape = tuple(shape)
        
    def read_all(self):
        """ Yiels a sequence of random images. """
        while True:
            shape = (self.shape[0], self.shape[1], 3)
            y = np.random.rand(*shape) * 255
            y = y.astype('uint8') 
            yield y
      
      

class CoherentRandomImageStream(ImageStream):
    
    @contract(shape='seq[2](int,>=1)', seed='int')
    def __init__(self, shape, seed, level, sigma_rel=0.03):
        self.seed = seed
        warnings.warn('seed not implemented')
        self.shape = tuple(shape)
        self.level = level
        self.sigma = np.min(self.shape) * sigma_rel 
        
    def read_all(self):
        """ Yiels a sequence of random images. """
        while True:
            yield self.get_image()
    
    @contract(returns='array[HxWx3](float32,>=0,<=1)')
    def get_image(self):    
        shape = (self.shape[0], self.shape[1])
        y = np.random.rand(*shape)
        y = y >= self.level
        y = y.astype('float32')
        # print self.sigma
        y = scipy_smooth(y, gaussian_std=self.sigma)
        y -= y.min()
        ymax = y.max()
        if ymax > 0:
            y *= 1.0 / ymax
        y = np.dstack((y, y, y))
        return y
    
    
@contract(y='array[HxW]', returns='array[HxW]', gaussian_std='float,>0')
def scipy_smooth(y, gaussian_std):
    import scipy.ndimage
    y2 = scipy.ndimage.filters.gaussian_filter(y, sigma=gaussian_std,
                                          order=0, mode='nearest')
    
    return y2
    
    
