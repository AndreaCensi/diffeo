from diffeo2d import Diffeomorphism2D
from diffeo2dds import get_conftools_discdds, get_diffeo2dds_config
from diffeo2dds_learn.library.action_estimators.diffeo_action_estimator_newunc import (
    consistency_based_uncertainty)
from diffeo2s import get_diffeo2s_config
from reprep import Report
import contracts


def test_consistency_uncertainty():
    configs = [ get_diffeo2dds_config(),
               get_diffeo2s_config()]
    
    for config in configs:
        config.load()   
    contracts.disable_all()
    symdds = 'sym-dpchain1-120'
    print('instancing dds %s' % symdds)
    
    dds = get_conftools_discdds().instance(symdds)
    shape = dds.get_shape()
    d1f = dds.actions[0].get_diffeo2d_forward()
    d1b = dds.actions[0].get_diffeo2d_backward()
    
    fb = Diffeomorphism2D.compose(d1f, d1b)
    bf = Diffeomorphism2D.compose(d1b, d1f)
    identity = Diffeomorphism2D.identity(shape)
    print(Diffeomorphism2D.distance_L2_infow(d1f, identity))
    print(Diffeomorphism2D.distance_L2_infow(d1b, identity))
    print(Diffeomorphism2D.distance_L2_infow(fb, identity))
    print(Diffeomorphism2D.distance_L2_infow(bf, identity))

    action = dds.actions[0]
    action2 = consistency_based_uncertainty(action, None)

    r = Report(symdds)
    r.text('symdds', symdds)
    with r.subsection('action') as sub:
        action.display(sub)
    with r.subsection('action2') as sub:
        action2.display(sub)
#         
#     with r.subsection('misc') as sub:
#         d = d1f.get_discretized_diffeo()
#         f = sub.figure()
#         f.array_as_image('d0', d[:, :, 0])
#         f.array_as_image('d1', d[:, :, 1])
#         
        
#     with r.subsection('d1f') as sub:
#         d1f.display(sub)
#     with r.subsection('d1b') as sub:
#         d1b.display(sub)
# 
#     with r.subsection('fb') as sub:
#         fb.display(sub)
#     with r.subsection('bf') as sub:
#         bf.display(sub)
    
    r.to_html('test_consistency_uncertainty.html')
