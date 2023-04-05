# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 16:34:34 2020

@author: Ganyu Wang

"""

#%% draft for Experiment 1 heat map

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
# sphinx_gallery_thumbnail_number = 2

vegetables = ["Turn on airplane mode", "Open the door", "Turn on the computer", "Turn on the light",
              "Call 911", 
              #"Turn on wireless hotspot",
              "Turn on Wi-Fi"
              ]
farmers = ["Google", "wit", #"Houndify",
           "IBM", "Azure"]

harvest = np.array([[0.91, 0.85,  0.11, 0.82],
                    [0.67, 0.77,  0.06, 0.68],
                    [0.67, 0.73,  0.28, 0.63],
                    [0.77, 0.66,  0.18, 0.63],
                    [0.94, 0.79,  0.76, 0.90],
                    #[0.88, 0.  ,  0.  , 0.74]
                    [0.92, 0.89,  0.11, 0.82]
                    ])

fig, ax = plt.subplots()
im = ax.imshow(harvest, cmap="YlOrRd")

# We want to show all ticks...
ax.set_xticks(np.arange(len(farmers)))
ax.set_yticks(np.arange(len(vegetables)))
# ... and label them with the respective list entries
ax.set_xticklabels(farmers)
ax.set_yticklabels(vegetables)

# Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")

# Loop over data dimensions and create text annotations.
for i in range(len(vegetables)):
    for j in range(len(farmers)):
        text = ax.text(j, i, harvest[i, j],
                       ha="center", va="center", color="w")

#ax.set_title("Perturbation rates for over the line attack")
fig.tight_layout()

divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
plt.colorbar(im, cax=cax, ticks= [0., 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])

plt.show()
plt.rcParams['savefig.dpi'] = 500 #图片像素
plt.rcParams['figure.dpi'] = 500 #分辨率


#%% draft for Experiment 2 heat map
# over-the-line fine grain. 

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
# sphinx_gallery_thumbnail_number = 2

vegetables = ["Turn on airplane mode", "Open the door", "Turn on the computer", "Turn on the light",
              "Call 911", 
              #"Turn on wireless hotspot", 
              "Turn on Wi-Fi"]
farmers = ["Google", "wit",
           "IBM", "Azure"]

harvest = np.array([[0.96, 0.86, 0.54, 0.86],
                    [0.91, 0.90, 0.53, 0.84],
                    [0.90, 0.85, 0.51, 0.82],
                    [0.95, 0.91, 0.81, 0.92],
                    [0.91, 0.82, 0.82, 0.90],
                    #[0.88, 0.81, 0.,   0.80],
                    [0.94, 0.91, 0.55, 0.92]
                    ])

plt.rcParams['savefig.dpi'] = 500 #图片像素
plt.rcParams['figure.dpi'] = 500 #分辨率

fig, ax = plt.subplots()
im = ax.imshow(harvest, cmap="YlOrRd", vmin=0., vmax=1.)

# We want to show all ticks...
ax.set_xticks(np.arange(len(farmers)))
ax.set_yticks(np.arange(len(vegetables)))
# ... and label them with the respective list entries
ax.set_xticklabels(farmers)
ax.set_yticklabels(vegetables)

# Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")

# Loop over data dimensions and create text annotations.
for i in range(len(vegetables)):
    for j in range(len(farmers)):
        text = ax.text(j, i, harvest[i, j],
                       ha="center", va="center", color="w")

#ax.set_title("Perturbation rates for over the line attack")
fig.tight_layout()

divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
cb = plt.colorbar(im, cax=cax, ticks= [0., 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])

plt.show()



#%% draft for Experiment 3 over the air segment-based perturbation  heat map
# over-the-line fine grain. 

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
# sphinx_gallery_thumbnail_number = 2

vegetables = ["Turn on airplane mode", "Open the door", "Turn on the computer", "Turn on the light",
              "Call 911", 
              #"Turn on wireless hotspot",
              "Turn on Wi-Fi"
              ]
farmers = ["Google", "wit",
           "IBM", "Azure"]

harvest = np.array([[0.78, 0.49, 0.15, 0.76],
                    [0.73, 0.67, 0.14, 0.83],
                    [0.56, 0.50, 0.20, 0.61],
                    [0.86, 0.43, 0.11, 0.73],
                    [0.92, 0.69, 0.30, 0.74],
                    #[0.77, 0.00, 0., 0.38],
                    [0.85, 0.64, 0.08, 0.83]
                    ])

plt.rcParams['savefig.dpi'] = 500 #图片像素
plt.rcParams['figure.dpi'] = 500 #分辨率

fig, ax = plt.subplots()
im = ax.imshow(harvest, cmap="YlOrRd", vmin=0., vmax=1.)

# We want to show all ticks...
ax.set_xticks(np.arange(len(farmers)))
ax.set_yticks(np.arange(len(vegetables)))
# ... and label them with the respective list entries
ax.set_xticklabels(farmers)
ax.set_yticklabels(vegetables)

# Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")

# Loop over data dimensions and create text annotations.
for i in range(len(vegetables)):
    for j in range(len(farmers)):
        text = ax.text(j, i, harvest[i, j],
                       ha="center", va="center", color="w")

# ax.set_title("Perturbation rates for over the line attack")
fig.tight_layout()

divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
plt.colorbar(im, cax=cax,  ticks= [0., 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])

plt.show()


#%% draft for Over-line SegmentPerturb - Random Delete Spectrum. 

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
# sphinx_gallery_thumbnail_number = 2

vegetables = ["Turn on airplane mode", "Open the door", "Turn on the computer", "Turn on the light",
              "Call 911", 
              #"Turn on wireless hotspot",
              "Turn on Wi-Fi"
              ]
farmers = ["Google", "wit",
           "IBM", "Azure"]

harvest = np.array([[0.80, 0.75, 0.52, 0.83],
                    [0.73, 0.79, 0.66, 0.85],
                    [0.79, 0.76, 0.71, 0.85],
                    [0.78, 0.66, 0.66, 0.82],
                    [0.83, 0.77, 0.65, 0.83],
                    [0.82, 0.77, 0.60, 0.86]
                    ])

plt.rcParams['savefig.dpi'] = 500 #图片像素
plt.rcParams['figure.dpi'] = 500 #分辨率

fig, ax = plt.subplots()
im = ax.imshow(harvest, cmap="YlOrRd", vmin=0., vmax=1.)

# We want to show all ticks...
ax.set_xticks(np.arange(len(farmers)))
ax.set_yticks(np.arange(len(vegetables)))
# ... and label them with the respective list entries
ax.set_xticklabels(farmers)
ax.set_yticklabels(vegetables)

# Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")

# Loop over data dimensions and create text annotations.
for i in range(len(vegetables)):
    for j in range(len(farmers)):
        text = ax.text(j, i, harvest[i, j],
                       ha="center", va="center", color="w")

# ax.set_title("Perturbation rates for over the line attack")
fig.tight_layout()

divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
plt.colorbar(im, cax=cax,  ticks= [0., 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])

plt.show()



#%% Graph for the explaination of the fine grain perturbation

import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

initiate = np.array([0, 0, 0, 0, 0, 0.25, 0.4, 0.3, 0.5, 0.6, \
                          0.2, 0.4, 0.5, 0.15, 0.2, 0, 0, 0, 0])

init_len = initiate.shape[0]
random_matrix = np.random.random(init_len)

# class_b = initiate + 0.1* random_matrix
# class_b[initiate==0] = 0.05 * random_matrix[initiate==0]

class_b = np.array([0, 0, 0, 0, 0.1, 0.3, 0.45, 0.33, 0.58, 0.66, \
                          0.24, 0.47, 0.6, 0.2, 0.3, 0.1, 0, 0, 0])

real = initiate

x_ind = np.arange(init_len)
y_ticks = np.arange(0, 1.1, 0.1)

plt.rcParams['savefig.dpi'] = 500 #图片像素
plt.rcParams['figure.dpi'] = 500 #分辨率

ax.bar(x_ind, real, width=0.5)
ax.set_xticks(x_ind)
ax.set_yticks(y_ticks)


ax.plot(class_b, "r")
ax.legend(["Theoretical Perturbation Boundary", "Real Perturbation Rate"])

ax.set_xlabel("Segment Index")
ax.set_ylabel("Perturbation rate")
#ax.set_title("The Concept Graph for Fine Grain Perturbation Algorithm")


#%% Box plot, Segment Length - APR. 
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['savefig.dpi'] = 500 #图片像素
plt.rcParams['figure.dpi'] = 500 #分辨率

font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 12}

plt.rc('font', **font)


data = [[.80, .75, .78, .80], #10
        [.93, .87, .36, .85, .92, .92, .74, .90],  #100
        [.88, .82, .24, .84, .875, .875, .6, .90], #200
        [.87, .83, .30, .80, .9, .83, .5, .9 ],    #300
        [.90, .85, .01, .75, .8, .85, .6, .55, .8 ]    #400
        ]

fig, ax = plt.subplots()

ax.boxplot(data)

ax.set_xticklabels(["10", "20", "30", "40", "50"])
ax.set_xlabel("Segment Length (ms)")
ax.set_ylabel("Average Perturbation Rate")

#%% Box plot, over the line, SegmentPerturb Random delete spectrum
# 
# Segment Length - APR
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['savefig.dpi'] = 500 #图片像素
plt.rcParams['figure.dpi'] = 500 #分辨率

font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 12}

plt.rc('font', **font)


data = [[.85, .82, .79, .82, .83, .86],
        [.83, .78, .80, .82, .80, .85],
        [.80, .83, .79, .78, .83, .82],
        [.79, .79, .79, .83, .80, .83],
        [.81, .78, .75, .80, .76, .78]
        
        ]

fig, ax = plt.subplots()

ax.boxplot(data)

ax.set_xticklabels(["10", "20", "30", "40", "50"])
ax.set_xlabel("Segment Length (ms)")
ax.set_ylabel("Average Perturbation Rate")


#%% Box plot. Distance - Perturbation rate. Over the line

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['savefig.dpi'] = 500 #图片像素
plt.rcParams['figure.dpi'] = 500 #分辨率

font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 12}

plt.rc('font', **font)


data = [[0.78, 0.73, 0.56, 0.86, 0.92, 0.85],
        [0.62, 0.73, 0.41, 0.66, 0.81, 0.73],
        [0.76, 0.66, 0.45, 0.75, 0.80, 0.84],
        [0.62, 0.46, 0.36, 0.58, 0.76, 0.65],
        ]

fig, ax = plt.subplots()

ax.boxplot(data, 0, "")

ax.set_xticklabels(['100', '150', '200', '250'])
ax.set_xlabel("The Distance from the Speaker to the Microphone (cm)")
ax.set_ylabel("Average Perturbation Rate")



#%% Use of the API to draw graph. 

from DrawGraphAPI import *

vegetables = ["Turn on airplane mode", "Open the door", "Turn on the computer", "Turn on the light",
              "Call 911", 
              #"Turn on wireless hotspot",
              "Turn on WIFI"
              ]
farmers = ["Google", "wit",
           "IBM", "Azure"]

harvest = np.array([[0.41, 0.43, 0., 0.4],
                    [0.50, 0.22, 0., 0.59],
                    [0.27, 0.27, 0., 0.45],
                    [0.66, 0.45, 0., 0.55],
                    [0.75, 0.40, 0., 0.75],
                    #[0.39, 0.00, 0., 0.38]
                    [0.61, 0.22, 0., 0.70]
                    ])

heat_map_for_ASR_command(farmers, vegetables, harvest)


#%% Extra test 2
















