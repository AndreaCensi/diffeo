""" 
    Some examples of functions that can be used to create diffeomorphisms. 

    All these functions should be continuous maps from ``[-1,+1]x[-1,+1]``
    to itself. 
    
    Most of these assume toroidal topology of the domain.
    The function :py:function:`mod` is the one that makes sure
    the output has the right codomain, and it assumes a toroidal 
    topology.
    
"""

class DiffeoLibrary(object):
    """ 
        A list of all diffeomorphisms defined in this module. 
        This is legacy code, it has been superseded by ConfigMaster.
    """
    
    diffeos = {}

    @staticmethod
    def get_inverse(function):
        ''' Returns the inverse of a given function in the library. '''
        name_inv = '%s_inv' % function.__name__
        if name_inv in DiffeoLibrary.diffeos:
            return DiffeoLibrary.diffeos[name_inv]
        if '_inv' in function.__name__:
            name_inv = function.__name__.replace('_inv', '')
            if name_inv in DiffeoLibrary.diffeos:
                return DiffeoLibrary.diffeos[name_inv]
        raise ValueError('Cannot find inverse of %s' % function)

    @staticmethod
    def get_invertible_diffeos():
        ''' Returns tuples (f, f_inv) of invertible pairs. '''
        for f in DiffeoLibrary.diffeos.values():
            try:
                f_inv = DiffeoLibrary.get_inverse(f)
            except ValueError:
                pass  # not invertible
            else:
                yield (f, f_inv)

    @staticmethod
    def add(name, function):
        DiffeoLibrary.diffeos[name] = function
#         config = get_diffeo2s_config()
#         spec = {'id': name,
#                  'desc': 'diffeo %r' % name,
#                  'code': ['diffeo2s.DiffeoLibrary.get', {'name': name}]}
#         config.symdiffeos[spec['id']] = spec
        
        
    @staticmethod
    def get(name):
        return DiffeoLibrary.diffeos[name]
        

from .utils import *
from .simple import *
from .reflections import *
from .rotations import *
from .deformations import *

