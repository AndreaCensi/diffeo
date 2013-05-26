from diffeo2d import Diffeo2dDistance, Diffeomorphism2D

__all__ = ['DDL2']
 
class DDL2(Diffeo2dDistance):
      
    def distance(self, d1, d2):
        """ Distance that does not take into account the uncertainty. """
        assert isinstance(d1, Diffeomorphism2D)
        assert isinstance(d2, Diffeomorphism2D)
        from diffeo2d.diffeo_basic import diffeo_distance_L2
        return diffeo_distance_L2(d1.d, d2.d)
