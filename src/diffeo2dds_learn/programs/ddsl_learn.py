from ..configuration import get_diffeo2ddslearn_config
from .ddsl import DDSL
from conf_tools import GlobalConfig

from quickapp import QuickApp


__all__ = ['DDSLLearn']

class DDSLLearn(DDSL.sub, QuickApp):  # @UndefinedVariable
    cmd = 'learn'
    description = 'Run normal learning for a given stream and learner.'
    
    
    def define_options(self, params):
        params.add_string('estimator', help='Which learner to use.')
        params.add_string('stream', help='Which data stream to use.')
        
    def define_jobs_context(self, context): 
        estimator = self.options.estimator
        stream = self.options.stream
        context.comp(learn_from_stream, GlobalConfig.get_state(),
                     stream=stream, estimator=estimator)
        
         
def learn_from_stream(global_config, stream, estimator):
    GlobalConfig.set_state(global_config)
    
    ddsl_config = get_diffeo2ddslearn_config()
        
    diffeo_learner = ddsl_config.diffeosystem_estimators.instance(estimator)
    stream = ddsl_config.streams.instance(stream)
