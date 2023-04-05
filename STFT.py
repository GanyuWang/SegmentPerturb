# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 23:02:30 2020

@author: wang_
"""

#%% 
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import stft
from scipy.io import wavfile
from numpy import ma
from matplotlib import ticker, cm
from mpl_toolkits.axes_grid1 import make_axes_locatable

def get_wave_form(path):
    wav_sci = wavfile.read(path)
    wave_form = wav_sci[1]
    if wave_form.ndim > 1:
        wave_form = wave_form[:, 0]
    return wave_form

def get_STFT_power(wave_form):
    f, t, Zxx = signal.stft(wave_form, fs=48000, nperseg = 1000)
    Zxx = np.flipud(Zxx)
    power = 10* np.log10(abs(Zxx))
    #power[power<-] = -10000
    
    return power, f, t
    
#%% Single plot 

i = 2

fn = ""
target_model = "ibm"
target_model_name = {"google": "Google", "wit": "Wit", "ibm": "IBM", "azure" : "Azure"}


title_list = ['Original command', "Noise Signal", "Segmented Perturbation on "+ target_model_name[target_model] ]

original_path = "AudioSamples\\Experiment4_SoundSample\\sound1\\"
segment_path = "AudioSamples\\Experiment4_SoundSample\\attack1\\"

wave_form_original = get_wave_form( original_path + fn +".wav")
wave_form_RPG = np.random.randint(-100, 100, size=137088)
wave_form_segment = get_wave_form(segment_path + fn + "_" + target_model + "_fine_tune_delete_breadth_first.wav")

wave_form_list = [wave_form_original, wave_form_RPG, wave_form_segment ]

power_original, f, t = get_STFT_power(wave_form_original)
power_RPG, f, t = get_STFT_power(wave_form_RPG)
power_segment, f, t = get_STFT_power(wave_form_segment)

power_list = [power_original, power_RPG, power_segment]

# set 
plt.rcParams['savefig.dpi'] = 800 #
plt.rcParams['figure.dpi'] = 800 #
# 

ax = plt.subplot(111)

im = ax.imshow(power_list[i],  cmap="YlOrRd", interpolation='none', origin='lower')
ax.set_ylabel("Frequency (Hz)")
ax.set_xlabel("Time (s)")
x_ind = [0, 100, 190]
y_ind = range(0, 500, 50)

ax.set_title(title_list[i])
ax.set_xticks(x_ind)
ax.set_yticks(y_ind)
ax.set_xticklabels(np.around(t[x_ind], decimals=1))
ax.set_yticklabels( f[y_ind])

divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="10%", pad=0.1)
colorbar = plt.colorbar(im, cax=cax)
colorbar.set_label("Power/Frequency (dB/Hz)")





