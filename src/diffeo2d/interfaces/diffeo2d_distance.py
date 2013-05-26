from .diffeomorphism2d import Diffeomorphism2D
from abc import abstractmethod
from contracts import ContractsMeta, contract

__all__ = ['Diffeo2dDistance']


class Diffeo2dDistance(object):
    __metaclass__ = ContractsMeta
    
    @abstractmethod
    @contract(d1=Diffeomorphism2D, d2=Diffeomorphism2D, returns='>=0')
    def distance(self, d1, d2):
        pass
        
    @contract(d1=Diffeomorphism2D, d2=Diffeomorphism2D, returns='>=0')
    def __call__(self, d1, d2):
        return self.distance(d1, d2)
