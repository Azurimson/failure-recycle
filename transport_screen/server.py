import numpy as np
import cv2
from PIL import ImageGrab as ig
import sys
import socket
import time
import threading
import numpy as np

def tcplink(sock, addr):
    try:
        while 1:
            s = ig.grab()
            r, c = s.size
            r = ("%04d" % r).encode(encoding = 'utf-8')
            c = ("%04d" % c).encode(encoding = 'utf-8')#确定数据规格
            sock.send(r)
            sock.send(c)
            s=cv2.cvtColor(np.array(s), cv2.COLOR_RGB2BGR)
##            print(s.shape)
            sock.send(s.tostring())
        sock.close()
##            cv2.imwrite('123.jpg', s)
##            break
    except Exception as e:
        print(e)

s = socket.socket()
host = '127.0.0.1'
port = 12345            
s.bind((host, port))
print(host)
s.listen(5) 
while True:
    sock, addr = s.accept()
    t = threading.Thread(target = tcplink, args = (sock, addr))
    t.start()

##s = ig.grab()
##r, c = s.size
##print(r, c)
##s=cv2.cvtColor(np.array(s), cv2.COLOR_RGB2BGR)
##for i in s:
##    for j in i:
##        print(j)
##        print(type(j))
##        print(type(j[0]))
##        list1 = j.tostring()
##        print(list1)
##        print(type(list1))
##        break
##    break
##print(len(s))
##cv2.namedWindow("s", 0)
####cv2.resizeWindow("s", 960, 640)
##cv2.imshow('s', s)
##print(type(s))
