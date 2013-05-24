from .dev import Dev
from diffeo2dds_learn import get_diffeo2ddslearn_config
from diffeo2dds_learn.programs import DDSLLearn
from quickapp import QuickApp

__all__ = ['Dev01']


class Dev01(Dev.get_sub(), QuickApp):  # @UndefinedVariable
    """ Some tests developing the new algorithm. """
     
    cmd = 'dev01'
    
    robots = ['exp21_unicornA_ceil',
              'exp21_unicornA_front',
              'exp21_unicornA_hlhr_sane_1']

    id_stream = 'dev01'
    id_robot = 'exp21_unicornA_hlhr_sane_1'
#     estimator = 'test_dds_estimator_fast_order_10'
    estimator = 'test_dds_estimator_refine1'        
      
    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):
        boot_root = "${YC2013WS}/out/"
        boot_root = '/Users/andrea/scm/boot12env/ws-yc1304-grace/out/boot-root'
        id_stream = Dev01.id_stream
        id_robot = Dev01.id_robot
        estimator = Dev01.estimator
        
        bootstream = ['diffeo_agents.library.BootStream',
                          dict(id_robot=id_robot, shape=[64, 64],
                               boot_root=boot_root)]
        
        spec = dict(id=id_stream, desc="",
                    code=['diffeo2dds_learn.library.LimitStream',
                          dict(n=1000, stream=bootstream)])
                          
        
        config = get_diffeo2ddslearn_config()
        config.streams[spec['id']] = spec
        
        id_stream = 'test_gauss_drx1_30_300'
        context.subtask(DDSLLearn, stream=id_stream, estimator=estimator)
