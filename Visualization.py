# -*- coding: utf-8 -*-
"""
Created on Mon May 25 22:26:56 2020

@author: wang_

all the function for visualization


"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import stft
from numpy import ma
from matplotlib import ticker, cm
from mpl_toolkits.axes_grid1 import make_axes_locatable


def draw_fine_tune_wave_form_perturb_rate(fn, wave_form, perturb_rate_block, over_threshold_ind):
    """
    the input should be
    fn, wave_form, info[1], info[2]
    
    fn, wave_form_perturb1, info[1], info[2]
    """
    
    perturb_ind = np.array(over_threshold_ind)
    
    wave_index = np.arange(wave_form.shape[0])
    
    #n_character = len(fn)
    color_array = np.zeros((1, wave_form.shape[0]))
    
    point_in_one_block = perturb_ind.shape[0]//(perturb_rate_block.shape[0]-1)
    
    for i in range(perturb_rate_block.shape[0] - 1):
        block_ind_in_wave_form = perturb_ind[i*point_in_one_block : (i+1)*point_in_one_block] 
        color_array[0, block_ind_in_wave_form] = perturb_rate_block[i+1]
  
    # plt.plot(wave_index, wave_form)
    # plt.imshow(color_array, cmap="YlOrRd", interpolation='none', extent=(0, wave_form.shape[0], 10000, -10000))
    # plt.colorbar()
        
    plt.rcParams['savefig.dpi'] = 500 #图片像素
    plt.rcParams['figure.dpi'] = 500 #分辨率
    
    #plt.rcParams['figure.figsize'] = [100., 0.5]
    
    #
    font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 5}

    plt.rc('font', **font)
    
    ax = plt.subplot(111)
    
    ax.plot(wave_index, wave_form)
    # x label 
    
    x_ind = np.arange(0, 160000, 9600)
    ax.set_title("d) Azure")
    ax.set_xticks(x_ind)
    ax.set_xticklabels(np.around(x_ind/48000, decimals=1))
    
    ax.set_xlabel("Time (s)")
    
    
    height = 10_000
    im = ax.imshow(color_array, cmap="YlOrRd", interpolation='none', extent=(0, wave_form.shape[0], -height, height), origin='lower')
    
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    
    
    plt.colorbar(im, cax=cax)

    plt.show()
    
    

