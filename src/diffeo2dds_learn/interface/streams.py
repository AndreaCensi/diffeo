from abc import abstractmethod
from contracts import ContractsMeta, contract
from diffeo2dds.model.uncertain_image import any_image_to_rgb

class LogItem(object):

    @contract(y0='array,shape(x)', y1='array,shape(x)', u='array')
    def __init__(self, y0, u, y1, x0=None):
        self.y0 = y0
        self.u = u
        self.y1 = y1
        self.x0 = x0
        
    def display(self, report):
        f = report.figure()
        f.data_rgb('y0', any_image_to_rgb(self.y0))
        f.data_rgb('y1', any_image_to_rgb(self.y1))
        

class Stream(object):
    """ 
        Abstracts away the source of the data. 
        
        Implement your own if you want to use different log formats.
         
    """
   
    __metaclass__ = ContractsMeta
        
    @abstractmethod        
    def read_all(self):
        """ Yields a sequence of LogItems. """
        pass
    

class ImageStream(object):
    """ 
        Abtracts away a sequence of images.
    """
    
    __metaclass__ = ContractsMeta 

    @abstractmethod        
    def read_all(self):
        """ Yields a sequence of RGB images. """
    
    
