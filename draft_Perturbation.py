# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 23:22:35 2021

@author: Ganyu Wang

Perturbation Draft



"""
import numpy as np
import random
from SpeechRecognitionAPI import Recognizer

import ffmpeg
import os

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


def random_negative(wave_form, percent):
    nframe = wave_form.shape[0]
    n_point = int(nframe * percent)
    wave_form_perturb = np.copy(wave_form)
    
    point_ind = random.sample(range(0, nframe), n_point)
    wave_form_perturb[point_ind] = - wave_form_perturb[point_ind]

    return(wave_form_perturb)

def random_delete_window(wave_form, percent):
    # add 0. 
    # first reshape(), window size
    # rand int for the window
    # delete the column in the window.
    # get back the original 
    time_window = 400
    
        # make matrix
    nframe = wave_form.shape[0]
    wave_form_perturb = np.copy(wave_form)
    wave_form_perturb = wave_form_perturb[:nframe - nframe%time_window]
    wave_form_matrix = wave_form_perturb.reshape(-1, time_window)
    
        # delete
    n_perturb = int(time_window * percent)
    point_ind = random.sample(range(0, time_window), n_perturb)
    wave_form_matrix[:, point_ind] = 0
        # get back 
    wave_form_perturb = wave_form_matrix.reshape(-1)
    
    return wave_form_perturb

def random_delete_threshold(wave_form, percent):
    
    wave_form_perturb = np.copy(wave_form)
    over_threshold_ind = threshold(wave_form)
    n_perturb = int(percent*len(over_threshold_ind))
    
    point_ind = random.sample(over_threshold_ind, n_perturb)
    wave_form_perturb[point_ind] = 0
    
    return(wave_form_perturb)


def random_negative_threshold(wave_form, percent):
    wave_form_perturb = np.copy(wave_form)
    over_threshold_ind = threshold(wave_form)
    n_perturb = int(percent*len(over_threshold_ind))
    
    point_ind = random.sample(over_threshold_ind, n_perturb)
    wave_form_perturb[point_ind] = - wave_form_perturb[point_ind]
    
    return(wave_form_perturb)


def random_scale(wave_form, sigma):
    sigma = sigma*2
    nframe = wave_form.shape[0]
    wave_form_perturb = np.copy(wave_form)
    perturb_matrix = np.random.randn(nframe)
    perturb_matrix[perturb_matrix>0] = 0
    wave_form_perturb = wave_form_perturb*(1 + perturb_matrix * sigma)
    wave_form_perturb = wave_form_perturb.astype("int16")
    

    return(wave_form_perturb)



#%% Perturbation method.

def perturb_feedback_random(wave_form, correct_result_list, recognizer, \
                            mode="efficiency", perturb_mode="delete", transcribe_mode= "line"):
    """
        input wave_form
            analysis the wave form
            
            continue perturb the wave form and find the classification margin. 
            
            
        
        output the success perturbation file. to path "AudioSamples\\AttackSample\\"
        Return wave_form_perturb. 
    
    """
    if perturb_mode == "delete":
        perturb_function = random_delete
    elif perturb_mode == "deletewindow":
        perturb_function = random_delete_window
    elif perturb_mode == "deletethreshold":
        perturb_function = random_delete_threshold
        
    elif perturb_mode == "negative":
        perturb_function = random_negative
    elif perturb_mode == "negativethreshold":
        perturb_function = random_negative_threshold
    elif perturb_mode == "scale":
        perturb_function = random_scale
    else:
        return
        
    if transcribe_mode == "line":
        transcribe_function = recognizer.transcribe
    elif transcribe_mode == "air":
        transcribe_function = recognizer.transcribe_air
    
    
    wave_form_perturb = np.copy(wave_form)
    #inititate the max perturbation 
    wave_form_perturb_max = np.copy(wave_form)
    perturb_rate_max = 0
    
    nframe = wave_form.shape[0]
    
    if mode == "efficiency":
        first = 0.
        last = 1.
    
        mid = (first + last)/2
        grain = 1
        
        while grain > 0.01 :
            
            mid = (first + last)/2
            grain = mid-first
            
            mid_result = []
            check_times = 2
            
            get_the_command = False
            for i in range(check_times):
                wave_form_perturb = perturb_function(wave_form, mid)
                # air
                mid_result = transcribe_function(wave_form_perturb)
                print(mid_result + "[" + str(mid) + "]  check times: " + str(i))
                if mid_result in correct_result_list:
                    get_the_command = True
                    break
            
            if get_the_command:
                first = mid
                # consider the max
                if mid > perturb_rate_max:
                    perturb_rate_max = mid
                    wave_form_perturb_max = np.copy(wave_form_perturb)

            else:
                last = mid 
                if mid < perturb_rate_max:
                    break
                    

        print("totally point of the audio" + str(nframe))
        print("max perturbation rate:" + str(perturb_rate_max))        
        return wave_form_perturb_max, perturb_rate_max
    
    elif mode == "traverse":
        
        if perturb_mode == "negative":
            traverse_list = np.arange(0.1, 0.0, -0.01)
        else:
            traverse_list = np.arange(0.95, 0.5, -0.05)
        
        # traverse through 1 ~ 0.07
        
        for perturb_rate in traverse_list:
            wave_form_perturb = perturb_function(wave_form, perturb_rate)
            result = transcribe_function(wave_form_perturb)
            print(result)
            print(perturb_rate)
            if result in correct_result_list:
                print("totally point of the audio" + str(nframe))
                print("max perturbation rate:" + str(perturb_rate))  
                return wave_form_perturb, perturb_rate
                 
        print("perturb failed")
        return wave_form, 0