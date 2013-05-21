from abc import abstractmethod, ABCMeta
from contracts import contract
from diffeo2dds import DiffeoSystem
from reprep import Report

__all__ = ['DiffeoSystemEstimatorInterface']


class DiffeoSystemEstimatorInterface(object):
    
    """ 
        Interface for a DiffeoSystem estimator. It integrates the information
        in pairs of images and returns a DiffeoSystem from get_value()
        when requested.
    """ 
    
    __metaclass__ = ABCMeta
        
    @abstractmethod
    @contract(y0='array[MxN]', u0='array[K]', y1='array[MxN]')
    def update(self, y0, u0, y1):
        pass

    @abstractmethod
    @contract(returns=DiffeoSystem)
    def get_value(self):
        ''' 
            Returns the estimated DiffeoSystem.
        '''
        
    @contract(i='int,>=0,i', n='int,>=1,>=i')
    def parallel_process_hint(self, i, n):
        """ 
            Hint for parallel processing. It tells this instance that
            it is instance "i" of "n" that sees the same data.
            
            
            Learning modality: 
            1) N copies of the same thing that looks at the same data
               Then parallel_process_hint(i, N) is called for each one.
               
            2) Different learners look at the same thing.
                Then parallel_process_hint(0, 1) is called for all learners.
        """
        raise NotImplementedError()
        
    def merge(self, other):
        """ 
            Support for parallel processing; merges the information 
            in another copy of itself that 
        """
        raise NotImplementedError()


    @abstractmethod
    @contract(report=Report)
    def display(self, report):
        """ Creates a report to show the internal state. """
        pass
