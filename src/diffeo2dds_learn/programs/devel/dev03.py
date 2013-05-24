from .dev import Dev
from calendar import c
from diffeo2dds_learn import get_diffeo2ddslearn_config
from diffeo2dds_learn.programs import DDSLLearn, DDSLShowStream
from quickapp import QuickApp
from quickapp.app_utils import iterate_context_names, iterate_context_names_pair

__all__ = ['Dev03']


class Dev03(Dev.get_sub(), QuickApp):  # @UndefinedVariable
    """ Trying the simple benchmark with all of our estimators """
     
    cmd = 'dev03'
    
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
    
    streams = ['exp21_unicornA_ceil',
               'exp21_unicornA_front',
               'exp21_unicornA_hlhr_sane_1']
          
    def define_options(self, params):
        pass
    
    
    def define_jobs_context(self, context):
        boot_root = '/Users/andrea/scm/boot12env/ws-yc1304-grace/out/boot-root'
        for cs, stream in iterate_context_names(context, Dev03.streams):
            add_bootstream(boot_root=boot_root, id_robot=stream, limit=5000)
            
            cs.subtask(DDSLShowStream, nsamples=4, streams=stream)
            

        combs = iterate_context_names_pair(context,
                                           Dev03.streams, Dev03.estimators)
        
        for c, stream, estimator in combs: 
            c.subtask(DDSLLearn, stream=stream, estimator=estimator,
                      max_displ=0.3)


def add_bootstream(boot_root, id_robot, limit=1000):
    """ Creates a Stream that reads data from a robot """
    bootstream = ['diffeo_agents.library.BootStream',
                      dict(id_robot=id_robot, shape=[128, 128],
                           boot_root=boot_root)]
    
    spec = dict(id=id_robot, desc="",
                code=['diffeo2dds_learn.library.LimitStream',
                      dict(n=limit, stream=bootstream)])
                      
    config = get_diffeo2ddslearn_config()
    config.streams[spec['id']] = spec
