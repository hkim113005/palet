import cv2
import pyzbar.pyzbar as pyzbar
from datetime import datetime
import keyboard
import sys
import tty
import termios 
import RPi.GPIO as GPIO
from hx711 import HX711
import pickle
import os

from qr import qr

records = {}

try:
    GPIO.setmode(GPIO.BCM)
    hx = HX711(dout_pin=5, pd_sck_pin=6)
    save_file_name = 'save_file.swp'
    with open(save_file_name, 'rb') as save_file:
        hx = pickle.load(save_file)    
    
    print()
    
    mini = 1000
    maxi = 0
    
    while True:
        print("Press the Enter key to reset")
        input()
        hx.zero(readings = 50)
        
        print("Press the Enter key to record")
        input()
        
        mass = round(hx.get_weight_mean(50), 2)
        print(mass)
        
        """
        w = round(hx.get_weight_mean(50), 2)
        mini = min(mini, w)
        maxi = max(maxi, w)
        print(maxi - mini)
        """
        
        # Read current frame
        read = qr.read(1)
        colors = read[0]
        frame = read[1]
        
        print(colors)
        print()
        
        """
        cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Frame', 600, 600)
        cv2.imshow('Frame', frame)
        """
        
        for color in colors:
            if color in records:
                records[color] = (records[color][0], mass)
            else:
                records[color] = (mass, 0)
    
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

except (KeyboardInterrupt, SystemExit):
    print('Closed')
    cv2.destroyAllWindows()
    
finally:
    GPIO.cleanup()