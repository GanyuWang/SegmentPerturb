# -*- coding: utf-8 -*-
"""
Created on Mon May 25 20:11:56 2020

@author: wang_
"""

import numpy as np
from SpeechRecognitionAPI import Recognizer
from SegmentPerturbAPI import perturb_segment
from Visualization import draw_fine_tune_wave_form_perturb_rate

import winsound

# file save path
Experiment_folder = "AudioSamples\\Experiment4_SoundSample\\sound1\\"
Attack_folder = "AudioSamples\\Experiment4_SoundSample\\attack4_random_spectrum\\"

# configure
recognizer = Recognizer()

ASR_dict= {1: "google",
           2: "wit",
           3: "ibm",
           4: "azure"
           }

# change model here
target_model = ASR_dict[1]
recognizer.set_model(target_model)

# input
command_dict = {1: "turn on airplane mode",
                2: "open the door",
                3: "turn on the computer",
                4: "turn on the light",
                5: "call 911",
                6: "turn on wifi",
                7: "turn on wireless hotspot" # deleted
                }

# change audio command here. 
fn = command_dict[6]
framerate = recognizer.read_parameter(Experiment_folder + fn + ".wav")
wave_form = recognizer.read_wave_form(Experiment_folder + fn + ".wav")
correct_list = [fn, "call nine one one", "turn on wi-fi", "okay google"]

#Segment attack 
perturb_mode_list = ["random_delete", "random_delete_spectrum"]
perturb_mode = perturb_mode_list[1]
perturb_seq_mode = "sort-a"

#perturb_seq_mode = "sort"
wave_form_perturb, info = perturb_segment(wave_form, 
                                          correct_list, 
                                          recognizer,
                                          perturb_mode = perturb_mode, 
                                          transcribe_mode = "line",
                                          perturb_rate_list = [0.6, 0.8, 0.9, 1], 
                                          #perturb_rate_list = [1.],
                                          n_segment= 0,
                                          timeframe_length_ms=20,
                                          perturb_seq_mode = perturb_seq_mode,
                                          break_mode = False)
average_perturbation_rate = info[0]

# Changed the ouput file name. 
comment = "%s-%s" % (perturb_mode, perturb_seq_mode)
save_file_path = "%s%s_%s_%s.wav" % (Attack_folder, fn, target_model, comment)
AMP = 2
recognizer.write_wavfile(wave_form_perturb*AMP, save_file_path)
    
# alert finish
winsound.MessageBeep()

