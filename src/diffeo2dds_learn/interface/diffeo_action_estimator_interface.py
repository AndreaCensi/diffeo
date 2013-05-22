from abc import abstractmethod
from contracts import ContractsMeta, contract
from diffeo2d_learn import Diffeo2dEstimatorInterface
from diffeo2dds import DiffeoAction
from reprep import Report

__all__ = ['DiffeoActionEstimatorInterface']


class DiffeoActionEstimatorInterface(object):
    
    """ 
        Interface for a DiffeoAction estimator.  
    """ 
    
    __metaclass__ = ContractsMeta
        
    @abstractmethod
    @contract(y0='array[MxN]', y1='array[MxN]')
    def update(self, y0, y1):
        pass
    
    
    NotReady = Diffeo2dEstimatorInterface.NotReady
    
    @abstractmethod
    @contract(returns=DiffeoAction)
    def get_value(self):
        ''' 
            Returns the estimated DiffeoAction or raises NotReady.
        '''
        
    @contract(i='int,>=0,i', n='int,>=1,>=i')
    def parallel_process_hint(self, i, n):
        raise NotImplementedError()
    
    @abstractmethod    
    def merge(self, other):
        pass

    @abstractmethod
    @contract(report=Report)
    def display(self, report):
        """ Creates a report to show the internal state. """
        pass
