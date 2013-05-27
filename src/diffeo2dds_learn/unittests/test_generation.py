# from diffeo2d.tests.utils.generation import fancy_test_decorator
# from diffeo2dds_learn.configuration.config_master import get_diffeo2ddslearn_config, \
#     get_conftools_streams, get_conftools_image_streams
# from comptests.registrar import comptests_for_all
# 
# def testconfig():
#     """ Makes sure we loaded the default config. """
#     config = get_diffeo2ddslearn_config()
#     config.load('default')
#     return config
#     
# def image_stream_lister():
#     config = testconfig()
#     keys = config.image_streams.keys()
#     keys = [k for k in keys if k.startswith('test_')]
#     return keys
#     
# 
# for_all_imagestreams = fancy_test_decorator(lister=image_stream_lister,
#             arguments=lambda id_image_stream: 
#                 (id_image_stream, testconfig().image_streams.instance(id_image_stream)),
#             attributes=lambda id_image_stream: dict(image_stream=id_image_stream),
#             debug=True)
# 
# def stream_lister():
#     config = testconfig()
#     keys = config.streams.keys()
#     keys = [k for k in keys if k.startswith('test_')]
#     return keys
# 
# for_all_streams = fancy_test_decorator(lister=stream_lister,
#             arguments=lambda x: (x, testconfig().streams.instance(x)),
#             attributes=lambda x: dict(stream=x),
#             debug=True)
from comptests.registrar import comptests_for_all
from diffeo2dds_learn import (get_conftools_streams,
    get_conftools_image_streams)
from diffeo2dds_learn.configuration.config_master import get_conftools_diffeoaction_estimators, \
    get_conftools_diffeosystem_estimators


for_all_streams = comptests_for_all(get_conftools_streams())
for_all_image_streams = comptests_for_all(get_conftools_image_streams())
for_all_diffeoaction_estimators = comptests_for_all(get_conftools_diffeoaction_estimators())
for_all_diffeosystem_estimators = comptests_for_all(get_conftools_diffeosystem_estimators())

