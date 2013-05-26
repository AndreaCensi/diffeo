from contracts import contract
from diffeo2dds.model.diffeo_action import DiffeoAction
from contracts import ContractsMeta
from abc import abstractmethod

__all__ = ['DiffeoActionDistance']


class DiffeoActionDistance(object):
    __metaclass__ = ContractsMeta
    
    @abstractmethod
    @contract(a1=DiffeoAction, a2=DiffeoAction, returns='>=0')
    def distance(self, a1, a2):
        pass
        
    @contract(a1=DiffeoAction, a2=DiffeoAction, returns='>=0')
    def __call__(self, a1, a2):
        return self.distance(a1, a2)
