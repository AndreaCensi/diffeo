from .ddsl import DDSL
from .ddsl_learn import DDSLLearn
from quickapp import QuickApp
from quickapp.app_utils import iterate_context_names_pair
from diffeo2dds_learn.programs.ddsl_learn_parallel import DDSLLearnParallel


__all__ = ['DDSLDemo1']


class DDSLDemo1(DDSL.sub, QuickApp):  # @UndefinedVariable
    """ A demo that runs parallel learning on many of the estimators defined here. """
    
    cmd = 'demo1'
    
    streams = [
        'test_random_dpx1_64_10',
        'test_random_drob1_64_10'
    ] 
    estimators = [
        'test_dds_estimator_simple_continuous_10',
        'test_dds_estimator_simple_binary_10',
        'test_dds_estimator_fast_order_10',
        'test_dds_estimator_fast_sim_10',
    ]
    
    def define_options(self, params):
        pass
        
    def define_jobs_context(self, context): 
        estimators = DDSLDemo1.estimators
        streams = DDSLDemo1.streams
        
        children = iterate_context_names_pair(context, streams, estimators)
        for c, stream, estimator in children:
#             c.subtask(DDSLLearn, stream=stream, estimator=estimator)
            c.subtask(DDSLLearnParallel, stream=stream, estimator=estimator)
        
