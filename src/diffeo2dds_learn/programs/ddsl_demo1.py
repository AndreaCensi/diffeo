from .ddsl import DDSL
from .ddsl_learn_parallel import DDSLLearnParallel
from diffeo2dds_learn import get_diffeo2ddslearn_config
from quickapp import QuickApp
from quickapp.app_utils import iterate_context_names_pair


__all__ = ['DDSLDemo1']


class DDSLDemo1(DDSL.sub, QuickApp):  # @UndefinedVariable
    """ A demo that runs parallel learning on many of the estimators defined here. """
    
    cmd = 'demo1'
    
    streams = [
        'test_random_dpx1_30_15',
        'test_random_drob1_30_15'
    ] 
    
    estimators = [
        'test_dds_estimator_simple_continuous_10',
        'test_dds_estimator_simple_binary_10',
        'test_dds_estimator_fast_order_10',
        'test_dds_estimator_fast_sim_10',
        'test_dds_estimator_fast_order_10_unc_norm',
        'test_dds_estimator_fast_sim_10_unc_normrel',
    ]
    
    def define_options(self, params):
        pass
        
    def define_jobs_context(self, context): 
        get_diffeo2ddslearn_config().load('default')
        
        estimators = DDSLDemo1.estimators
        streams = DDSLDemo1.streams
        
        children = iterate_context_names_pair(context, streams, estimators)
        for c, stream, estimator in children:
            c.subtask(DDSLLearnParallel, stream=stream, estimator=estimator)


            
