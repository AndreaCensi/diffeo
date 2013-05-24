from .dev import Dev
from diffeo2dds_learn.programs import DDSLLearn, DDSLShowStream
from quickapp import QuickApp
from quickapp.app_utils import iterate_context_names, iterate_context_names_pair

__all__ = ['Dev02']


class Dev02(Dev.get_sub(), QuickApp):  # @UndefinedVariable
    """ Trying the simple benchmark with all of our estimators """
     
    cmd = 'dev02'
    
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

    streams = ['test_gauss_drx1_68_500']
          
    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):
        for cs, stream in iterate_context_names(context, Dev02.streams):
            cs.subtask(DDSLShowStream, nsamples=4, streams=stream)
            

        combs = iterate_context_names_pair(context,
                                           Dev02.streams, Dev02.estimators)
        
        for c, stream, estimator in combs: 
            c.subtask(DDSLLearn, stream=stream, estimator=estimator,
                      max_displ=0.3)
