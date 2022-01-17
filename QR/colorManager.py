import cv2
import pyzbar.pyzbar as pyzbar
from datetime import datetime
import keyboard
import sys
import tty
import termios
import qrCodeReader as qr

try:
    while True:
        # Read current frame
        read = qr.read(1)
        colors = read[0]
        frame = read[1]
        
        print(colors)
        print()
        cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Frame', 600, 600)
        cv2.imshow('Frame', frame)
        
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print('Closed')
    cv2.destroyAllWindows()