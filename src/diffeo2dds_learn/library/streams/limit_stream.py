from contracts import contract
from diffeo2dds_learn import Stream, get_diffeo2ddslearn_config

__all__ = ['LimitStream']

class LimitStream(Stream):
    """ Limits the stream to the first elements. """ 
    
    @contract(n='int,>=0')
    def __init__(self, stream, n):
        config = get_diffeo2ddslearn_config()
        _, self.stream = config.streams.instance_smarter(stream)
        self.n = n
        
    def read_all(self):
        """ Yiels a sequence of random images. """
        i = 0
        for x in self.stream.read_all():
            if i > self.n:
                break
            yield x
        
            if i % 30 == 0:
                print('read: %r' % i)
         
            i += 1 
            
