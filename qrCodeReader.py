# Author: peppe8o
# Date: Aug 2nd, 2021
# Blog: https://peppe8o.com
# Version: 1.0

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

colors = set()
it = 0

coefficients = [0.114 * 1, 0.587 * 1, 0.399 * 1]
m = np.array(coefficients).reshape((1,3))

def decodeCam(image):
    global it
    #gray = cv2.transform(image, m)
    barcodes = pyzbar.decode(image)
    #print('reading...', end='\r')
    for barcode in barcodes:
        barcodeData = barcode.data.decode()
        barcodeType = barcode.type
        #print("["+str(datetime.now())+"] Type:{} | Data: {}".format(barcodeType, barcodeData))
        colors.add(barcodeData)
    #print()
    it += 1
    return image

start = time.time()
end = time.time()

try:
    while True:
        # Read current frame
        ret, frame = camera.read()
        im=decodeCam(frame)
        if it >= 2:
            #if len(colors) != 4:
                #print ('ERROR')
            print(colors)
            colors = set()
            it = 0
            cv2.imwrite('test.png', im)
            end = time.time()
            print(end - start)
            start = time.time()
except KeyboardInterrupt:
     print('interrupted!')
