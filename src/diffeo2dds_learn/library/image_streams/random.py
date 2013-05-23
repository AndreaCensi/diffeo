from diffeo2dds_learn import ImageStream
from contracts import contract
import numpy as np
import warnings

__all__ = ['RandomImageStream']

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
            
