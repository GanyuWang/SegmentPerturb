# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 21:34:07 2020

@author: Ganyu Wang

Segmented Perturbation API

"""

import numpy as np
import random
from SpeechRecognitionAPI import Recognizer
import ffmpeg
import os

def random_delete(wave_form, percent):
    """
    Input : wave_form, perturbation_rate
    Output : Perturbed_wave_form 
    """
    wave_form_perturb = np.copy(wave_form)
    nframe = wave_form.shape[0]
    n_delete = int(nframe*percent)      # the name was n_point
    delete_ind = random.sample(range(0, nframe), n_delete)
    wave_form_perturb[delete_ind] = 0

    return wave_form_perturb

def random_delete_spectrum(wave_form, percent):
    """
    Input : wave_form, perturbation_rate
        wave_form_perturb
    Output : Perturbed_wave_form 
    """
    wave_form_perturb = np.copy(wave_form)
    
    # fft and delete
    wave_form_perturb_fft = np.fft.fft(wave_form_perturb)

    # get the index to delete, in frequency domain. 
    # (the deletion is at certain spectrum corresponding to each frequency.)
    n_spectrum = wave_form_perturb_fft.shape[0]
    n_spectrum_lower_part = n_spectrum // 2
    n_delete_lower_part = int( n_spectrum_lower_part * percent )
    delete_ind_lower_part = random.sample(range(0, n_spectrum_lower_part), n_delete_lower_part)
    delete_ind_lower_part = np.array(delete_ind_lower_part)  # convert to np.array.
    delete_ind_upper_part = (n_spectrum-1)*np.ones_like(delete_ind_lower_part) \
        - delete_ind_lower_part
    
    # delete in frequency domain
    wave_form_perturb_fft[delete_ind_lower_part] = 0
    wave_form_perturb_fft[delete_ind_upper_part] = 0
    # iFFT 
    wave_form_perturb = np.fft.ifft(wave_form_perturb_fft)
        # format
    wave_form_perturb = np.real(wave_form_perturb).astype("int16")
    return wave_form_perturb
    

def threshold(wave_form):
    """
    input the wave_form
        get the max value, set 1/10 of the max value as the threshold
        return the wave_form. 
    return the index of higher than the threshold.
    """
    over_threshold = np.abs(wave_form)>20
    over_threshold_ind = []
    
    for (ind, judgement) in enumerate(over_threshold):
        if judgement:
            over_threshold_ind.append(ind)
    
    return over_threshold_ind

    
#%%
def perturb_segment(wave_form, 
                    correct_result_list, 
                    recognizer,
                    perturb_mode = "random_delete",
                    transcribe_mode = "air", 
                    perturb_rate_list = [0.4, 0.6, 0.8],
                    n_segment = 0,
                    timeframe_length_ms=20,
                    perturb_seq_mode = "random",
                    break_mode = False):

    # Initiate - perturb mode
    if perturb_mode == "random_delete":
        perturb_function = random_delete
    elif perturb_mode == "random_delete_spectrum":
        perturb_function = random_delete_spectrum
    
    # Initiate - transcribe mode
    if transcribe_mode == "line":
        transcribe_function = recognizer.transcribe
    elif transcribe_mode == "air":
        transcribe_function = recognizer.transcribe_air
        
    framerate = recognizer.get_framerate()
    # copy the wave_form
    wave_form_perturb = np.copy(wave_form)
    over_threshold_ind = threshold(wave_form)
    
    # #2 use settled timeframe length. 
    point_in_one_block = (framerate//1000) * timeframe_length_ms
    n_block = len(over_threshold_ind) // point_in_one_block
    
    if n_segment != 0:
        n_block = n_segment # if specific number of segment, use it.
        point_in_one_block = len(over_threshold_ind)
    
    meet_end_flag = np.zeros(n_block, dtype=bool)
    intergral_cal = np.zeros(n_block, dtype=float)
    
    if perturb_seq_mode == "random":
        # range(1, n_block)   range(n_block, 0, -1)  random.sample(range(1, n_block), n_block-1)
        random_perturb_seq_list = random.sample(range(0, n_block), n_block)
    elif perturb_seq_mode[:4] == "sort":
        print("**use sort***")
        # Calculate the sum of absolute of each block. 
        sum_of_block_array = np.zeros(n_block, dtype=float)
        for i in range(n_block):
            a = i*point_in_one_block
            b = (i+1)*point_in_one_block
            absolute = np.absolute(wave_form[over_threshold_ind[a:b]])
            sum_of_block = np.sum(absolute)
            sum_of_block_array[i] = sum_of_block
        # Sort sum_of_block_array to get the random_perturb_seq_list ()
        # smallest to largest.
        random_perturb_seq_list=sum_of_block_array.argsort()
        if perturb_seq_mode[4:] == "-d":
            print("**** descending ****")
            random_perturb_seq_list = np.flip(random_perturb_seq_list)
        
    for ind, perturb_rate in enumerate(perturb_rate_list):
        for block_ind in random_perturb_seq_list:
            if meet_end_flag[block_ind] == False:
                # Perturb on the block. record in wave_form_perturb_tmp.
                wave_form_perturb_tmp = np.copy(wave_form_perturb)
                left = block_ind * point_in_one_block
                right = (block_ind+1)*point_in_one_block
                perturb_point_ind = over_threshold_ind[left:right]
                wave_form_block = wave_form[perturb_point_ind]
                wave_form_perturb_block = perturb_function(wave_form_block, perturb_rate)
                wave_form_perturb_tmp[perturb_point_ind] = wave_form_perturb_block
                # Test the perturb part. 
                result = transcribe_function(wave_form_perturb_tmp)
                if result in correct_result_list:
                    #submit the change to wave_form_perturb
                    wave_form_perturb = wave_form_perturb_tmp
                    #record the current perturbation rate. 
                    intergral_cal[block_ind] = perturb_rate_list[ind]
                    print("%s_%s_%s" % (result, str(block_ind), str(perturb_rate)))
                else: # discard the change in wave_form_perturb_tmp.
                    meet_end_flag[block_ind] = True
                    
                    # record last perturbation rate in the preturbation rate
                    if ind == 0:
                        intergral_cal[block_ind] = 0
                    else:
                        # record the last perturbation rate for that block. 
                        intergral_cal[block_ind] = perturb_rate_list[ind-1]
                        
                    print("%s_%s_wrong_%s" % (result, str(block_ind), str(perturb_rate)))
                    if (perturb_seq_mode=="sort" and break_mode == True):
                        break
                    
        print("round**************")        

    intergral_perturbation_rate = np.sum(intergral_cal)/(n_block)
    
    info = (intergral_perturbation_rate, intergral_cal, over_threshold_ind)
    
    return wave_form_perturb, info




