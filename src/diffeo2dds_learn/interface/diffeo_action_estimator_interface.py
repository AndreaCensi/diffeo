from abc import abstractmethod
from contracts import ContractsMeta, contract
from decent_logs import WithInternalLog
from diffeo2d_learn import Diffeo2dEstimatorInterface
from diffeo2dds import DiffeoAction
from reprep import Report

__all__ = ['DiffeoActionEstimatorInterface']


class DiffeoActionEstimatorInterface(WithInternalLog):
    
    """ 
        Interface for a DiffeoAction estimator.  
    """ 
    
    __metaclass__ = ContractsMeta
    
    @abstractmethod
    @contract(max_displ='seq[2](float,>0,<=1)')
    def set_max_displ(self, max_displ):
        """ 
            Sets the maximum displacement to be used, in resolution-independent
            units.  Must be called before any call to update().
        """
    
    class LearningConverged(Exception):
        """ 
            Thrown by update() to signal that they do not need 
            more data to converge. 
        """
        pass

    @abstractmethod
    @contract(y0='array[MxN]|array[MxNx3]', y1='array[MxN]|array[MxNx3]')
    def update(self, y0, y1):
        """ 
            Might throw DiffeoActionEstimatorInterface.LearningConverged 
            to signal that no more data is necessary. 
        """
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
