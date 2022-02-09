"""
Credit to gandalf15 on GitHub for HX711 Python library and example_save_state.py source code.
(https://github.com/gandalf15/HX711/blob/master/python_examples/example_save_state.py)
"""

import RPi.GPIO as GPIO
from hx711 import HX711
import pickle
import os

try:
    GPIO.setmode(GPIO.BCM)
    hx = HX711(dout_pin=5, pd_sck_pin=6)

    save_file_name = 'save_file.swp'
    if os.path.isfile(save_file_name):
        with open(save_file_name, 'rb') as save_file:
            hx = pickle.load(save_file)
    else:
        err = hx.zero()
        if err:
            raise ValueError('Tare is unsuccessful.')
        
        reading = hx.get_raw_data_mean()
        if reading:
            print('Data subtracted by offset but still not converted to units: ', reading)
        else:
            print('Invalid Data: ', reading)
            
        input('Put known weight on the scale and then press Enter')
        reading = hx.get_data_mean()
        if reading:
            print('Mean value from HX711 subtracted by offset: ', reading)
            known_weight_grams = input('Write how many grams it was and press Enter: ')
            try:
                value = float(known_weight_grams)
                print(value, 'grams')
            except ValueError:
                print('Expected integer or float. Received:', known_weight_grams)
                
            ratio = reading / value
            hx.set_scale_ratio(ratio)
            print('Ratio is set.')
        else:
            raise ValueError('Cannot calculate mean value. Variable reading:', reading)
        
        print('Saving the HX711 state to swap file on persistant memory.')
        with open(save_file_name, 'wb') as save_file:
            pickle.dump(hx, save_file)
            save_file.flush()
            os.fsync(save_file.fileno())
            
    input('Press Enter to begin reading.')
    while True:
        print(hx.get_weight_mean(20), 'g')
        
except (KeyboardInterrupt, SystemExit):
    print('Closing.')
    
finally:
    GPIO.cleanup()
