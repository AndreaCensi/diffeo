from .ddsl import DDSL
from conf_tools import GlobalConfig
from contracts import contract
from diffeo2dds import DiffeoSystem, ds_dump
from diffeo2dds_learn import (DiffeoSystemEstimatorInterface,
    get_diffeo2ddslearn_config)
from quickapp import QuickApp
from reprep import Report
import os


__all__ = ['DDSLLearn']

class DDSLLearn(DDSL.sub, QuickApp):  # @UndefinedVariable
    """ Run normal learning for a given stream and learner."""
    
    cmd = 'learn'
    
    def define_options(self, params):
        params.add_string('estimator', help='Which learner to use.')
        params.add_string('stream', help='Which data stream to use.')
        
    def define_jobs_context(self, context): 
        estimator = self.options.estimator
        stream = self.options.stream
        
        jobs_learning(context, estimator, stream)
        
        
def jobs_learning(context, estimator, stream):
    # learn
    learner = context.comp_config(learn_from_stream,
                                  stream=stream, estimator=estimator)
    # summarize
    dds = context.comp(get_estimated_dds, learner)
    
    # save dds
    outdir = context.get_output_dir()
    context.comp(save_results, estimator, stream, outdir, dds)
    
    # create reports
    params = dict(stream=stream, estimator=estimator)
    learner_report = context.comp(report_learner, learner) 
    dds_report = context.comp(report_dds, dds)
    context.add_report(learner_report, 'learner', **params)
    context.add_report(dds_report, 'dds', **params)
        
         
@contract(stream='str', estimator='str')
def learn_from_stream(stream, estimator):
    """ Returns the estimator instance at the end of the learning. """
    ddsl_config = get_diffeo2ddslearn_config()
        
    diffeo_learner = ddsl_config.diffeosystem_estimators.instance(estimator)
    assert isinstance(diffeo_learner, DiffeoSystemEstimatorInterface)
    stream = ddsl_config.streams.instance(stream)

    for log_item in stream.read_all():
        y0 = log_item.y0
        y1 = log_item.y1
        u = log_item.u
        diffeo_learner.update(y0, u, y1)
        
    return diffeo_learner 


@contract(stream='str', estimator='str', i='int,>=0', n='int')
def learn_from_stream_parallel(stream, estimator, i, n):
    """ This version also gives the parallel hints. """
    ddsl_config = get_diffeo2ddslearn_config()

    stream = ddsl_config.streams.instance(stream)
        
    estimator = ddsl_config.diffeosystem_estimators.instance(estimator)
    assert isinstance(estimator, DiffeoSystemEstimatorInterface)

    # here we hint that you are one of many
    estimator.parallel_process_hint(i, n)

    for log_item in stream.read_all():
        y0 = log_item.y0
        y1 = log_item.y1
        u = log_item.u
        estimator.update(y0, u, y1)
        
    return estimator 


def save_results(estimator, stream, outdir, dds):
    """ Save estimated model externally. """
    id_dds = '%s-%s' % (estimator, stream)
    resdir = os.path.join(outdir, 'results')
    desc = "Learned from stream %s and learner %s" % (stream, estimator)
    ds_dump(dds, resdir, id_dds, desc)
    
@contract(returns=Report)
def report_learner(learner):
    r = Report('learner')
    learner.display(r)
    return r

@contract(returns=Report)
def report_dds(dds):
    r = Report('dds')
    dds.display(r)
    return r

@contract(returns=DiffeoSystem)
def get_estimated_dds(estimator):
    """ Extracts the model from the estimator. """
    return estimator.get_value()

