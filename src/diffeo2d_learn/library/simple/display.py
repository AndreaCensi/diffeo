from PIL import Image  # @UnresolvedImport
from contracts import contract
from diffeo2d import coords_iterate
from diffeo2d.visualization import (diffeo_to_rgb_angle,
    diffeo_to_rgb_norm)
import matplotlib.pyplot as plt
import numpy as np
import numpy.linalg as la


@contract(diff='valid_diffeomorphism,array[MxNx2]')
def display_diffeo_images(diff, name):
    im_ang = Image.fromarray(diffeo_to_rgb_angle(diff)).resize((400, 300))
    im_norm = Image.fromarray(diffeo_to_rgb_norm(diff)).resize((400, 300))
    im_ang.save(name + 'ang.png')
    im_norm.save(name + 'norm.png')

    
def sim_square_check(sim_square):
#    fig = plt.figure()
#    ax = fig.gca(projection='3d')
#    X, Y = np.meshgrid(range(sim_square.shape[0]), range(sim_square.shape[0]))
#    surf = ax.plot_surface(X, Y, sim_square, rstride=1, cstride=1, cmap=cm.jet,
#        linewidth=0, antialiased=False)
#    fig.colorbar(surf, shrink=0.5, aspect=5)
#    plt.savefig('test.png')
    Image.fromarray((sim_square * 255).astype('uint8')).resize((400, 300)).save('sim_square.png')
    
def display_disp_quiver(diff, name):
    Y, X = np.meshgrid(range(diff.shape[1]), range(diff.shape[0]))
    plt.figure()
    plt.quiver(X, Y, diff[:, :, 1], -diff[:, :, 0])
    plt.savefig(name)
    
def display_continuous_stats(diff, variance, minerror, maxerror, name):
    Y, X = np.meshgrid(range(diff.shape[1]), range(diff.shape[0]))
    plt.figure(figsize=(16, 12), dpi=600)
    plt.quiver(X, Y, diff[:, :, 1], diff[:, :, 0])
    
    minvar = np.min(variance)
    maxvar = np.max(variance)
    norm_variance = (variance - minvar) / (maxvar - minvar) * 50 + 1
#    plt.scatter(X + diff[:, :, 0], Y + diff[:, :, 1], c=minerror, s=norm_variance)
    plt.scatter(X, Y, c=minerror, s=norm_variance)
    
    plt.savefig(name)
    

def sim_square_modify(sim_square, minval=None, maxval=None):
    if minval is None:
        mi = np.min(sim_square)
    else:
        mi = minval
    if maxval is None:
        ma = np.max(sim_square)
    else:
        ma = maxval
    
    mod_square = -(sim_square - ma) / (ma - mi)
    return mod_square, mi, ma
    
def get_cm(sim_arr):
    shape = np.array(sim_arr.shape)
    cent = (shape.astype('float') - [1, 1]) / 2
    # center of mass
    torque = np.array([0.0, 0.0])
    mass = 0.0
    inertia_sum = 0.0
    
    area = np.zeros(sim_arr.shape)
    area[sim_arr > np.max(sim_arr) * 0.9] = sim_arr[sim_arr > np.max(sim_arr) * 0.9]
        
    for cn in coords_iterate(shape):
        r = (np.array(cn) - cent)
        torque += area[cn] * r
        mass += area[cn]
        
    # if no mass, return zero
    if mass == 0:
        return np.array([0, 0]), 0    
    
    cm = torque / mass
    
    for cn in coords_iterate(shape):
        r = (np.array(cn) - cent)
        a = la.norm(r)
        inertia_sum += a ** 2 * area[cn]
    
    inertia = inertia_sum / mass 
    return cm, inertia
