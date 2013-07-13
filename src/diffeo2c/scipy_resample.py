from contracts import contract

__all__ = ['scipy_image_resample']

@contract(image='array[HxWx3](float32)|array[HxWx3](uint8)|array[HxW](float32)',
          shape='seq[2](int,>1)', returns='array')
def scipy_image_resample(image, shape, order=3):
    """ 
        :param order: Order of spline interpolation. order=0 should be invertible
        if upsampling.
    """
    import scipy.ndimage
    
    shape_target = list(image.shape)
    shape_target[0] = shape[0]
    shape_target[1] = shape[1]
    shape_target = tuple(shape_target)
    # 3 = cubic

    if True:
        eps = 0.0001
        zoom = [1.0 * (shape[0] + eps) / image.shape[0],
                1.0 * (shape[1] + eps) / image.shape[1]]
    
        if len(image.shape) == 3:
            zoom.append(1)

        # this is the way it is computed by scipy, using "int"
        projected = tuple([int(ii * jj) for ii, jj in zip(image.shape, zoom)])
        assert(projected == shape_target)
            
        # print('image orig: %s' % str(image.shape))
        # print('want: %s' % str(shape))
        # print('zoom: %s' % str(zoom))
        # s = np.array(zoom) * np.array(image.shape)
        # print('image orig * zoom: %s' % str(s))
        f = scipy.ndimage.interpolation.zoom
        y = f(image, zoom=zoom, order=order, mode='nearest')

#     else:
#         y = scipy_zoom(image, shape_target, order=order, mode='nearest')
    # print('target: %s' % str(shape_target))
    # print('obtained: %s' % str(y.shape))
    
#     from scipy.misc import imresize
#     y = imresize(image, shape)  # , mode='F')
    assert(y.shape == shape_target)
#     assert y.shape[0] == shape[0]
#     assert y.shape[1] == shape[1]
#     assert len(y.shape) == len(image.shape)
    return y
