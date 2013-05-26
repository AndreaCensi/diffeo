from diffeo2d import Diffeo2dDistance, Diffeomorphism2D
import numpy as np

__all__ = ['DDL2iw']
 
class DDL2iw(Diffeo2dDistance):
    """ 
        Distance that weights the mismatch by the product
        of the uncertainties. 
    """
      
    def distance(self, d1, d2):
        assert isinstance(d1, Diffeomorphism2D)
        assert isinstance(d2, Diffeomorphism2D)
        dd1 = d1.get_discretized_diffeo()
        dd2 = d2.get_discretized_diffeo()
        dd1_info = d1.get_scalar_info()
        dd2_info = d2.get_scalar_info()
        
        from diffeo2d.diffeo_basic import diffeo_local_differences
        x, y = diffeo_local_differences(dd1, dd2)
        dist = np.hypot(x, y)
        info = dd1_info * dd2_info
        info_sum = info.sum()
        if info_sum == 0:
            return 1.0  # XXX, need to check it is the bound
                    
        wdist = (dist * info) / info_sum
        
        res = wdist.sum()
        return res
    
