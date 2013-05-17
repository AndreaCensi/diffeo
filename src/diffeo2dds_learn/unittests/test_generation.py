from diffeo2d.tests.utils.generation import fancy_test_decorator
from diffeo2dds_learn.configuration.config_master import get_diffeo2ddslearn_config

def testconfig():
    """ Makes sure we loaded the default config. """
    config = get_diffeo2ddslearn_config()
    config.load('default')
    return config
    
def lister():
    config = testconfig()
    keys = config.image_streams.keys()
    keys = [k for k in keys if k.startswith('test_')]
    return keys
    

for_all_imagestreams = fancy_test_decorator(lister=lister,
            arguments=lambda id_image_stream: 
                (id_image_stream, testconfig().image_streams.instance(id_image_stream)),
            attributes=lambda id_image_stream: dict(image_stream=id_image_stream),
            debug=True)

def stream_lister():
    config = testconfig()
    keys = config.streams.keys()
    keys = [k for k in keys if k.startswith('test_')]
    return keys

for_all_streams = fancy_test_decorator(lister=stream_lister,
            arguments=lambda x: (x, testconfig().streams.instance(x)),
            attributes=lambda x: dict(stream=x),
            debug=True)


