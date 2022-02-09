"""
Credit to peppe8o for tutorial/guide and base source code.
(https://peppe8o.com/read-qr-codes-from-raspberry-pi-with-pyzbar-and-python/)
"""

import os
import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
from datetime import datetime
import time

width = 2592
height = 1944

camera = cv2.VideoCapture(0)
camera.set(3,width)
camera.set(4,height)

coefficients = [0.114 * 1, 0.587 * 1, 0.399 * 1]
m = np.array(coefficients).reshape((1,3))

def decodeCam(image, colors):
    #image = cv2.transform(image, m)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    barcodes = pyzbar.decode(image)
    for barcode in barcodes:
        barcodeData = barcode.data.decode()
        barcodeType = barcode.type
        colors.add(barcodeData)
        
    return colors, image

def read(t):
    start = time.time()
    colors = set()
    image = None
    
    for i in range(t):
        ret, frame = camera.read()
        colors, image = decodeCam(frame, colors)
    
    """
    date = str(datetime.now())
    date = date[:10] + '_' + date[11:22]
    par_dir = os.getcwd()
    path = os.path.join(par_dir, 'log', date)
    os.mkdir(path)
    cv2.imwrite(path + '/image.png', frame)
    f = open(path + '/colors.txt', 'w')
    f.write(str(colors))
    f.close()
    """    
    
    end = time.time()
    print(round(end - start, 2))
    
    return (colors, image)