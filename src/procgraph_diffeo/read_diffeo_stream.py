from diffeo2dds_learn import get_conftools_streams
from procgraph import Block
from procgraph.block_utils import IteratorGenerator
from procgraph.core.registrar_other import simple_block
import numpy as np
from reprep.graphics.filter_scale import scale

__all__ = ['ReadDiffeoStream']

class ReadDiffeoStream(IteratorGenerator):
    """ Reads a sequence of LogItems """
    
    Block.alias('read_diffeo_stream')
    Block.config('stream', 'Stream to read')
    Block.output('data')

    def init_iterator(self):
        """ Must return an iterator yielding signal, timestamp, values """
        return self.read_stream(self.config.stream)
    
    def read_stream(self, id_stream):
        stream = get_conftools_streams().instance(id_stream)
        for i, log_item in enumerate(stream.read_all()):
            signal = 'data'
            timestamp = i * 1.0
            yield signal, timestamp, log_item 

class ReadDiffeoStreamItems(IteratorGenerator):
    """ Reads a sequence of LogItems, separating in y0,u,y1 """
    
    Block.alias('read_diffeo_stream_components')
    Block.config('stream', 'Stream to read')
    
    Block.output('y0')
    Block.output('u')
    Block.output('y1')
    

    def init_iterator(self):
        """ Must return an iterator yielding signal, timestamp, values """
        return self.read_stream(self.config.stream)
    
    def read_stream(self, id_stream):
        stream = get_conftools_streams().instance(id_stream)
        for i, log_item in enumerate(stream.read_all()):
            timestamp = i * 1.0
            yield 'y0', timestamp, log_item.y0 
            yield 'y1', timestamp, log_item.y1 
            yield 'u', timestamp, log_item.u 
            

@simple_block
def diffeo_show_mismatch(y0, y1):
    e = np.abs(y0 - y1)
    if e.ndim == 3:
        e.sum(axis=2)
    return scale(e, min_color=[0, 0, 0], max_color=[1, 0, 0])




