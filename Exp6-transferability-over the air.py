# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 13:31:21 2021

@author: Ganyu Wang
"""

from SpeechRecognitionAPI import Recognizer

# Target model dict, command_dict
target_model_dict = {1: "google", 
                     2: "wit",
                     3: "ibm",
                     4: "azure"
                     }

command_dict = {1: "turn on airplane mode",
                2: "open the door",
                3: "turn on the computer",
                4: "turn on the light",
                5: "call 911",
                6: "turn on wifi"
                }

# initiate Recognizer
recognizer = Recognizer()
# initiate folder
Attack_folder = "AudioSamples\\Experiment6_Transferability\\attack3-random-2m"

# the original command attack 
target_model_a = target_model_dict[1]
# the model for transfer attack
target_model_b = target_model_dict[1]

# the command for attack 
command = command_dict[4]

result_list = []
for i in range(5):

    # the experiment
    Attack_file_path = "%s\\%s_%s_2m.wav" % (Attack_folder, command, target_model_a)
    # ******change to normal file ***********
    
    # Attack_file_path = "AudioSamples\\Experiment6_Transferability\\attack0_ordinary\\%s.wav" % command
    
    
    # set target model
    recognizer.set_model(target_model_b)
    
    framerate = recognizer.read_parameter(Attack_file_path)
    wave_form = recognizer.read_wave_form(Attack_file_path)
    
    result = recognizer.transcribe_air(wave_form)
    result_list.append(result)
    print(result)

print(result_list)

