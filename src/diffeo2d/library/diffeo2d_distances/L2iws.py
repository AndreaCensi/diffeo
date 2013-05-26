
from diffeo2d import Diffeo2dDistance, Diffeomorphism2D
import numpy as np

__all__ = ['DDL2iws']
 
class DDL2iws(Diffeo2dDistance):

    def distance(self, d1, d2):
        # XXX: written while rushing
        a = Diffeomorphism2D.distance_L2_infow(d1, d2)
        dd1_info = d1.get_scalar_info()
        dd2_info = d2.get_scalar_info()
        # x = dd1_info
        # print('min %g max %g' % (x.max(), x.min()))
        b = np.mean(np.abs(dd1_info - dd2_info))  # / dd1_info.size
        # print('a, b: %.5f %.5f   mean %g %g' % (a, b, dd1_info.mean(), dd2_info.mean()))
        return b + min(a, 0.5)  # a * (1 + b)
    
