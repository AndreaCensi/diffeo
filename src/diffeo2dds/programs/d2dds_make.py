from ..configuration import get_diffeo2dds_config
from ..model import DiffeoSystem, ds_dump
from .d2dds import Diffeo2dds
from conf_tools.utils import raise_x_not_found
from contracts import describe_type
import os

__all__ = ['MakeDDS']


class MakeDDS(Diffeo2dds.get_sub()):
    """ Creates synthetic DDS from the functions symbolically defined. """
    
    cmd = 'makedds'
    usage = 'makedds [<dds1> <dds2> ...]s '
    
    def define_program_options(self, params):
        params.accept_extra()
        params.add_string('output', short='o', default='out/d2dds_makedds')
        params.add_flag('verbose', help='Instances all configuration')     
        
    def go(self):
        outdir = self.options.output
        which = self.options.get_extra()
        
        config = get_diffeo2dds_config()
        if not which:
            which = sorted(config.symdds.keys())
        
        make_all_dds(config, which, outdir)
        
         
def make_all_dds(config, which, outdir):
    if not os.path.exists(outdir):
        os.makedirs(outdir) 
        
    for id_symdds in which:
        if not id_symdds in config.symdds:
            raise_x_not_found('symdds', id_symdds, config.symdds)
                
    for id_symdds in which:
        make_dds(config, id_symdds, outdir)
        
def make_dds(config, id_symdds, outdir):
    dds = instance_dds(config, id_symdds)

    ds_dump(dds,
            path=outdir,
            name=id_symdds,
            desc='Synthetically generated from symbolic DDS %r.' % id_symdds)
        
        
def instance_dds(config, id_symdds): 
    dds = config.symdds.instance(id_symdds)  # @UndefinedVariable
    if not isinstance(dds, DiffeoSystem):
        msg = 'I expect to find a DiffeoSystem, not %r' % describe_type(dds)
        raise ValueError(msg)
    dds.label = id_symdds
    return dds
    
