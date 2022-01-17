import cv2
import pyzbar.pyzbar as pyzbar
from datetime import datetime
import keyboard
import sys
import tty
import termios

# Camera Initialization
width = 1280
height = 720

camera = cv2.VideoCapture(0)
camera.set(3,width)
camera.set(4,height)

# Color management
colorIDs = {}
colorNum = 0
prevColors = set()
initMass = {}
finalMass = {}
initialized = False
        
def update(colors):
    global prevColors
    
    if prevColors == colors: return
    
    dif = colors.difference(prevColors)
    
    if len(dif) != 1: return
    
    for new in dif:
        if not initialized:
            print(new)
            initMass[new] = 50
        else:
            print(new)
            finalMass[new] = 50
        
    prevColors = colors
                
def decodeCam(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    barcodes = pyzbar.decode(gray)
    colors = set()
    
    for barcode in barcodes:
       colors.add(barcode.data.decode())
       print(barcode.data.decode())
       
    return image

try:
    while True:
        # Read current frame
        ret, frame = camera.read()
        im = decodeCam(frame)
except KeyboardInterrupt:
    print('Closed')