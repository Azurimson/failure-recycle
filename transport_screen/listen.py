import numpy as np
import cv2
from PIL import ImageGrab as ig
import sys
from socket import *

s = socket(AF_INET, SOCK_STREAM)
s.connect(('127.0.0.1', 12345))
while 1:
    r = s.recv(4)
    c = s.recv(4)
    r = int(r.decode('utf-8'))
    c = int(c.decode('utf-8'))
    print(r, c)
    img = s.recv(r * 3)
    img = np.fromstring(img, dtype=np.uint8)
    img = img.reshape(1, r, -1)
    print(img.shape)
    for i in range(1, c):
        cele = s.recv(r * 3)
        cele = np.fromstring(cele, dtype=np.uint8)
        cele = cele.reshape(1, r, -1)
        img = np.row_stack((img, cele))
    print(img.shape)
##    cv2.imwrite('124.jpg', img)
        
##    cv2.namedWindow("img", 0)
##    cv2.resizeWindow("img", 960, 640)
    cv2.destroyAllWindows()
    cv2.imshow('img', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
s.close()
cv2.destroyAllWindows()
