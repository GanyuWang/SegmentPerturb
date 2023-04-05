# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 14:36:09 2020

@author: Ganyu Wang

"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable



def heat_map_for_ASR_command(ASR_list, command_list, heat_matrix):
    
    plt.rcParams['savefig.dpi'] = 500 #图片像素
    plt.rcParams['figure.dpi'] = 500 #分辨率
    
    fig, ax = plt.subplots()
    im = ax.imshow(heat_matrix, cmap="YlOrRd", vmin=0., vmax=1.)
    
    # We want to show all ticks...
    ax.set_xticks(np.arange(len(ASR_list)))
    ax.set_yticks(np.arange(len(command_list)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(ASR_list)
    ax.set_yticklabels(command_list)
    
    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")
    
    # Loop over data dimensions and create text annotations.
    for i in range(len(command_list)):
        for j in range(len(ASR_list)):
            text = ax.text(j, i, heat_matrix[i, j],
                           ha="center", va="center", color="w")
    
    #ax.set_title("Perturbation rates for over the line attack")
    fig.tight_layout()
    
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    cb = plt.colorbar(im, cax=cax, ticks= [0., 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    
    plt.show()
    
