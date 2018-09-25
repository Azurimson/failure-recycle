##import numpy as np
##import cv2
##from PIL import ImageGrab as ig
##import sys
##
##s = ig.grab()
##row, col = s.size
##fps = 16
##print(row, col)
##fourcc = cv2.VideoWriter_fourcc(*'MJPG')
##video = cv2.VideoWriter("1.avi", fourcc, fps, (row, col))
##
##k=np.zeros((200,200),np.uint8)
##while True:
##    im = ig.grab()
##    imm=cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
##    video.write(imm)
##    cv2.imshow('imm', k)
##    if cv2.waitKey(1) & 0xFF == ord('q'):
##        break
##    
##video.release()
##
##cv2.destroyAllWindows()

##import wave
##from pyaudio import PyAudio, paInt16
##
##framerate = 8000
##NUM_SAMPLES = 2000
##channels = 1
##sampwidth = 2
##TIME = 2
##
##def save_wave_file(filename,data):
##    wf=wave.open(filename,'wb')
##    wf.setnchannels(channels)#声道
##    wf.setsampwidth(sampwidth)#采样字节 1 or 2
##    wf.setframerate(framerate)#采样频率 8000 or 16000
##    wf.writeframes(b"".join(data))
##    wf.close()
##
##
##pa = PyAudio()
##stream = pa.open(format=paInt16,
##                 channels=1,
##                 rate=framerate,
##                 input=True,
##                 frames_per_buffer=NUM_SAMPLES)
##my_buf = []
##count = 0
##while count < TIME * 20:
##    string_audio_data = stream.read(NUM_SAMPLES)
##    my_buf.append(string_audio_data)
##    count +=1
##    print('.')
##save_wave_file('01.wav', my_buf)
##stream.close()

import numpy as np
a = np.array([])
b = np.array([[0,0,0]])
c = np.r_[a,b]
print(c)
