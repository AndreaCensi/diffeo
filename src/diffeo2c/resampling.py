from contracts import contract, new_contract
import numpy as np

__all__ = ['diffeoc_from_diffeou', 'diffeou_from_diffeoc', 'diffeo_resample']

new_contract('valid_diffeou', 'array[HxWx2](float32,>=0,<=1)')
# from diffeo2d.misc_utils import coords_iterate
# from diffeo2d.diffeo_basic import coords_to_X, X_to_coords

# @contract(d='array[HxWx2],valid_diffeomorphism',
#           returns='array[HxWx2],valid_diffeou')
# def diffeou_from_diffeoc(d):
#     """ Converts a discrete diffeomorphism to a field
#         with float values in [-1,+1], using coords_to_X.  """
#     H, W, _ = d.shape
#     du = np.zeros((H, W, 2), dtype='float32')
#     du.fill(np.nan)
#     for c in coords_iterate((H, W)):
#         du[c[0], c[1], :] = coords_to_X(d[c], (H, W))
#     return du
#     
# 
# @contract(du='array[HxWx2],valid_diffeou',
#           returns='valid_diffeomorphism_cont')
# def diffeoc_from_diffeou(du):
#     """ 
#         Converts a field of [-1,1] coordinates to a valid 
#         diffeomorphism (continuous). 
#     """
#     H, W, _ = du.shape
#     f = np.zeros((H, W, 2), dtype='float32')
#     f.fill(np.nan)
#     for c in coords_iterate((H, W)):
#         f[c[0], c[1], :] = X_to_coords(du[c], (H, W))
#     return f

@contract(d='array[HxWx2],valid_diffeomorphism',
          returns='array[HxWx2],valid_diffeou')
def diffeou_from_diffeoc(d):
    """ Converts a discrete diffeomorphism to a field
        with float values in [-1,+1], using coords_to_X.  """
    H, W, _ = d.shape
    du = np.zeros((H, W, 2), dtype='float32')
    for i in range(2):
        du[:, :, i] = d[:, :, i] * (1.0 / d.shape[i]) 
    np.clip(du, 0, 1, du)
    return du
    

@contract(du='array[HxWx2],valid_diffeou',
          returns='valid_diffeomorphism_cont')
def diffeoc_from_diffeou(du):
    """ 
        Converts a field of [-1,1] coordinates to a valid 
        diffeomorphism (continuous). 
    """
    H, W, _ = du.shape
    f = np.zeros((H, W, 2), dtype='float32')
    for i in range(2):
        f[:, :, i] = du[:, :, i] * du.shape[i]
        np.clip(f[:, :, i], 0, du.shape[i] - 1, f[:, :, i])
    return f

    
@contract(d='valid_diffeomorphism',
          shape='seq[2](int,>=1)',
          returns='valid_diffeomorphism_cont,array[XxYx2](float32)')
def diffeo_resample(d, shape, order=3):
    """ 
        Resamples a diffeomorphism.
    """
    shape = tuple(shape)
    from .scipy_resample import scipy_image_resample

    # First we convert to resolution-independent coordinates
    du = diffeou_from_diffeoc(d)
    # print('--- resample')
    # print('d  line 0: %s' % d[0, :, 0])
    # print('du line 0: %s' % du[0, :, 0])
    
    # Next, we can resample this using normal functions
    dur = np.zeros((shape[0], shape[1], 2), 'float32')
    dur.fill(np.nan)
    dur[:, :, 0] = scipy_image_resample(du[:, :, 0], shape, order=order)
    dur[:, :, 1] = scipy_image_resample(du[:, :, 1], shape, order=order)
    
    np.clip(dur, 0, 1, dur)
    
    # print('dur line 0: %s' % dur[0, :, 0])
    
    d2 = diffeoc_from_diffeou(dur)
    # print('d2  line 0: %s' % d2[0, :, 0])
    return d2


