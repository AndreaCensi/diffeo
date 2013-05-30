from .dev import Dev
from compmake import compmake_execution_stats
from diffeo2dds_learn.programs import DDSLLearn
from quickapp import QuickApp, iterate_context_names_quartet
from reprep.report_utils import StoreResults

__all__ = ['Dev04']


class Dev04(Dev.get_sub(), QuickApp):  # @UndefinedVariable
    """ Formal benchmarks for some of the estimators. """
     
    cmd = 'dev04'
    
          
    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):
        sizes = [ 16, 32, 64]  # 128, 256, 512]
        nobss = [500]
        streams = ['test_gauss_drx1']
        estimators = ['test_ddsest_unc_refine0',
                      'test_ddsest_unc_simple_bin']
        max_displ = 0.3
        
        results = StoreResults()
        comp_stats = StoreResults()
        combs = iterate_context_names_quartet(context, sizes, nobss, streams, estimators)
        for c, shape, length, stream, estimator in combs:
            key = dict(length=length, shape=shape, stream=stream, estimator=estimator)
            id_stream = stream + '_%s_%s' % (shape, length)
            learned = c.subtask(DDSLLearn, stream=id_stream, estimator=estimator,
                          max_displ=max_displ) 
            results[key] = learned
            comp_stats[key] = compmake_execution_stats(learned)
