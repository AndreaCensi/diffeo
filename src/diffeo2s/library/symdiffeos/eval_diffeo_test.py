from diffeo2s.configuration.config_master import get_conftools_symdiffeos
from geometry.formatting import printm
import numpy as np
from geometry.rotations import SO2_from_angle
# 
# def test_eval_diffeo1():
#     tr2 = get_conftools_symdiffeos().instance('tr2')
#     print tr2
#     
#     p = np.array([-1, -1])
#     p2 = tr2.apply(p)
#     
#     R = SO2_from_angle(np.pi / 4)
#     p2exp = np.dot(R, p)
#     
#     printm('p', p, 'p2', p2, 'p2exp', p2exp)
#     print p2
