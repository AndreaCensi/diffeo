from diffeo2dds_learn import get_diffeo2ddslearn_config
from quickapp import iterate_context_names_pair

from .ddsl_learn_parallel import jobs_learning_parallel


__all__ = ['jobs_ddsl_demo']


# class DDSLDemo1(DDSL.sub, QuickApp):  # @UndefinedVariable
#
#     cmd = 'demo1'
#     def define_options(self, params):
#         pass
#
#     def define_jobs_context(self, context):


def jobs_ddsl_demo(context):
    """ A demo that runs parallel learning on many of the estimators defined here. """
    

    
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
    
    get_diffeo2ddslearn_config().load('default')

    children = iterate_context_names_pair(context, streams, estimators)
    for c, stream, estimator in children:
        max_displ = (0.24, 0.24)
        nthreads = 4  # num threads
        jobs_learning_parallel(c, estimator, stream, max_displ=max_displ, nthreads=nthreads)
