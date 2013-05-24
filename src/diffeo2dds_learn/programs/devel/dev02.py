from .dev import Dev
from diffeo2dds_learn.programs import DDSLLearn
from quickapp import QuickApp
from quickapp.app_utils import iterate_context_names_pair

__all__ = ['Dev02']


class Dev02(Dev.get_sub(), QuickApp):  # @UndefinedVariable
    """ Trying the simple benchmark with all of our estimators """
     
    cmd = 'dev02'
    
    id_robot = 'exp21_unicornA_hlhr_sane_1'
    estimators = [
                  'test_dds_estimator_refine_30',
                  'test_dds_estimator_fast_order_30',
                  'test_dds_estimator_fast_sim_30',
#                   'test_dds_estimator_fast_order_30_unc_norm',
#                   'test_dds_estimator_fast_sim_30_unc_normrel'
    ]        
    streams = ['test_gauss_drx1_68_300']
          
    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):
        combs = iterate_context_names_pair(context,
                                           Dev02.streams, Dev02.estimators)
        for c, stream, estimator in combs: 
            c.subtask(DDSLLearn, stream=stream, estimator=estimator)
