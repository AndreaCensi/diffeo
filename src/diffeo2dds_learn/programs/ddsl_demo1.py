from .ddsl import DDSL
from .ddsl_learn_parallel import DDSLLearnParallel
from diffeo2dds_learn import get_diffeo2ddslearn_config
from quickapp import QuickApp, iterate_context_names_pair


__all__ = ['DDSLDemo1']


class DDSLDemo1(DDSL.sub, QuickApp):  # @UndefinedVariable
    """ A demo that runs parallel learning on many of the estimators defined here. """
    
    cmd = 'demo1'
    
    streams = [
        'test_random_dpx1_30_15',
        'test_random_drob1_30_15'
    ] 
    
    estimators = [
     'test_ddsest_reg_fast_order',
     'test_ddsest_reg_fast_sim',
     'test_ddsest_reg_simple_cont',
     'test_ddsest_reg_simple_bin',
     'test_ddsest_reg_refine1',
     'test_ddsest_unc_fast_order',
     'test_ddsest_unc_fast_sim',
     'test_ddsest_unc_simple_cont',
     'test_ddsest_unc_simple_bin',
     'test_ddsest_unc_refine1'
    ]
    
    def define_options(self, params):
        pass
        
    def define_jobs_context(self, context): 
        get_diffeo2ddslearn_config().load('default')
        
        estimators = DDSLDemo1.estimators
        streams = DDSLDemo1.streams
        
        children = iterate_context_names_pair(context, streams, estimators)
        for c, stream, estimator in children:
            c.subtask(DDSLLearnParallel, stream=stream, estimator=estimator,
                      max_displ=0.24)


            
