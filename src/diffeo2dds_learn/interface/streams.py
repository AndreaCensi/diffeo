from abc import abstractmethod, ABCMeta
from collections import namedtuple


LogItem = namedtuple('LogItem', 'y0 u y1 x0')


class Stream(object):
    """ 
        Abstracts away the source of the data. 
        
        Implement your own if you want to use different log formats.
         
    """
   
    __metaclass__ = ABCMeta
        
    @abstractmethod        
    def read_all(self):
        pass
    

class ImageStream(object):
    """ 
        Abtracts away a sequence of images.
    """
    
    __metaclass__ = ABCMeta 

    @abstractmethod        
    def read_all(self):
        """ Yields a sequence of RGB images. """
    
    
