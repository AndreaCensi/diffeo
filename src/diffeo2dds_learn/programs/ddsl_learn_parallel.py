from .ddsl import DDSL
from .ddsl_learn import (learn_from_stream_parallel, get_estimated_dds,
    report_learner, report_dds, save_results)
from conf_tools import GlobalConfig
from quickapp import QuickApp


__all__ = ['DDSLLearnParallel']


class DDSLLearnParallel(DDSL.sub, QuickApp):  # @UndefinedVariable
    """ Run parallel learning for a given stream and learner."""
    
    cmd = 'learn-parallel'
    
    def define_options(self, params):
        params.add_string('estimator', help='Which learner to use.')
        params.add_string('stream', help='Which data stream to use.')
        params.add_int('n', default=4,
                       help='Number of threads to use.')
        
    def define_jobs_context(self, context): 
        estimator = self.options.estimator
        stream = self.options.stream
        n = self.options.n
        
        jobs_learning_parallel(context, estimator, stream, n)


def jobs_learning_parallel(context, estimator, stream, nthreads, intermediate_reports=True):
    """ Creates jobs for learning in parallel. """
    
    # partial results
    partial = []
    for i in range(nthreads):
        c = context.child('c%d' % (i + 1))
        
        learner_i = c.comp(learn_from_stream_parallel, GlobalConfig.get_state(),
                           stream=stream, estimator=estimator, i=i, n=nthreads,
                           job_id='learn')
    
        partial.append(learner_i)
        
        # If we want to generate intermediate reports
        if intermediate_reports:
            params_i = dict(stream=stream, estimator=estimator, i=i, n=nthreads)
            c.add_report(c.comp(report_learner, learner_i),
                         'learner_partial', **params_i)
            
            diffeo_i = c.comp(get_estimated_dds, learner_i,
                              job_id='summarize')
            
            c.add_report(c.comp(report_dds, diffeo_i),
                         'dds_partial', **params_i)
            
    # TODO: redo this in a hierarchical way
    current = partial[0]
    for i in range(1, nthreads):
        current = context.comp(merge, current, partial[i],
                               job_id='merge-%sof%s' % (i, nthreads - 1))
    # final learner
    learner = current
    # final model
    dds = context.comp(get_estimated_dds, current,
                       job_id='summarize')

    # save dds
    outdir = context.get_output_dir()
    context.comp(save_results, estimator, stream, outdir, dds)    
    
    params = dict(estimator=estimator, stream=stream)
    context.add_report(context.comp(report_learner, learner),
                       "learner", **params) 
    
    context.add_report(context.comp(report_dds, dds),
                       "dds", **params)

    
def merge(learner1, learner2):
    learner1.merge(learner2)
    return learner1
