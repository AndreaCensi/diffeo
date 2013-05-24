from diffeo2dds_learn import ImageStream
from contracts import contract
import numpy as np
import warnings
from procgraph_cv.opencv_utils import smooth

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
    
    @contract(returns='array[HxWx3](float32)')
    def get_image(self):    
        shape = (self.shape[0], self.shape[1])
        y = np.random.rand(*shape)
        y = y >= self.level
        y = y.astype('float32')
        # print self.sigma
        y = smooth(y, gaussian_std=self.sigma)
        y = np.dstack((y, y, y))
        y -= y.min()
        y *= 1.0 / y.max()
        return y
    
    
    
