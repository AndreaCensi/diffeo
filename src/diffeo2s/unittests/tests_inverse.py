from diffeo2s import NoInverseAvailable
from geometry import printm
import numpy as np
from .generation import for_all_symdiffeos

@for_all_symdiffeos
def check_symdiffeo_inverse1(id_symdiffeo, symdiffeo):  # @UnusedVariable
    try:
        inverse = symdiffeo.get_inverse()
    except NoInverseAvailable:
        print('Skipping %r because no inverse available.' % id_symdiffeo)
        return
    
    manifold = symdiffeo.get_topology()
        
    points = [[0, 0], [-1, -1], [+1, -1]]
     
    for p in points:
        p0 = np.array(p)
        p = manifold.normalize(p0)
        p1 = symdiffeo.apply(p)
        p2 = inverse.apply(p1)
    
        print('%s = %s -> %s -> %s' % (p0, p, p1, p2))
        try:    
            manifold.assert_close(p, p2)
        except:
            print('Function: %s' % symdiffeo)
            print('Inverse: %s' % inverse)
            printm('p', p)
            printm('f(p)', p1)
            printm('g(f(p))', p2)
            raise
        
