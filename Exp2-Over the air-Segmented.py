# -*- coding: utf-8 -*-
"""
Created on Mon May 11 16:23:02 2020

@author: wang_
"""


from SpeechRecognitionAPI import Recognizer
from SegmentPerturbAPI import perturb_segment

# file save place
Experiment_folder = "AudioSamples\\Experiment4_SoundSample\\sound1\\"
Attack_folder = "AudioSamples\\Experiment4_SoundSample\\attack2_spectrum_draft\\"

# 
# configure
recognizer = Recognizer()
target_model = "google"
recognizer.set_model(target_model)
perturb_rate_list = [0.2, 0.4, 0.6, 0.8]



# input
fn = "turn on wifi"
#correct_list = [fn, "turn on the airplane mode"]
#correct_list = [fn, "open the doors"]
#correct_list = [fn, "turn on the computers"]
#correct_list = [fn, "turn on the lights"]
#correct_list = [fn, "call nine one one"]
#correct_list = [fn, "turn on wireless hotspots"]
correct_list = [fn, "turn on wi-fi"]

#fine tuning attack 
framerate = recognizer.read_parameter(Experiment_folder + fn + ".wav")
wave_form = recognizer.read_wave_form(Experiment_folder + fn + ".wav")

wave_form_perturb, info = perturb_segment(wave_form, 
                                          correct_list, 
                                          recognizer, 
                                          transcribe_mode = "air",
                                          perturb_rate_list = perturb_rate_list,
                                          timeframe_length_ms=35
                                          )
average_perturbation_rate = info[0]


    
# ouput file name. 
comment = "air_spectrum_2m"
save_file_path = "%s%s_%s_%s.wav" % (Attack_folder, fn, target_model, comment)
recognizer.write_wavfile(wave_form_perturb, save_file_path)


