from . import contract, np, diffeo_identity, dmod
from collections import namedtuple


DiffeoStats = namedtuple('DiffeoStats', 'norm angle dx dy curv')


def diffeo_stats(D):
    ''' Returns norm, angle representation. '''
    identity = diffeo_identity(D.shape[0:2])
    dx = (D - identity)[:, :, 0]
    dy = (D - identity)[:, :, 1]
    
    dx = dmod(dx, D.shape[0] / 2)
    dy = dmod(dy, D.shape[1] / 2)
    angle = np.arctan2(dy, dx)
    norm = np.hypot(dx, dy)
    angle[norm == 0] = np.nan
    dxdx, dxdy = np.gradient(dx)
    dydx, dydy = np.gradient(dy)
    curv = (dxdx * dydy - dxdy * dydx) / 4.0
    return DiffeoStats(norm=norm, angle=angle, dx=dx, dy=dy, curv=curv)




@contract(D='valid_diffeomorphism')
def diffeo_text_stats(D):
    stats = diffeo_stats(D)
    s = ''
    s += 'Maximum norm: %f\n' % stats.norm.max()
    s += 'Mean norm: %f\n' % np.mean(stats.norm)
    s += 'Mean  d0: %f\n' % np.mean(stats.dx)
    s += 'Mean  d0: %f\n' % np.mean(stats.dy)
    s += 'Mean |d0|: %f\n' % np.mean(np.abs(stats.dx))
    s += 'Mean |d1|: %f\n' % np.mean(np.abs(stats.dy))

    s += 'Mean curv: %f\n' % np.mean(stats.curv)
    s += 'Min, max curv: %f %f\n' % (np.min(stats.curv), np.max(stats.curv))
    return s

