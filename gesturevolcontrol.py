# from operator import length_hint
from operator import length_hint
from sre_constants import SUCCESS
import cv2
import math
import GestureVolumeControl.HandTracking as htm
import time
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

cap = cv2.VideoCapture(0)

detector = htm.handDetector(detectionCon=0.9)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volrange = volume.GetVolumeRange()
minvol=volrange[0]
maxvol=volrange[1]

while True:
    SUCCESS,img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        x1 , y1 = lmList[4][1] , lmList[4][2]
        x2 , y2 = lmList[8][1] , lmList[8][2]
        cx ,cy = (x1+x2)//2,(y1+y2)//2
        cv2.circle(img , (x1,y1) , 15 , (255,0,255), cv2.FILLED)
        cv2.circle(img , (x2,y2) , 15 , (255,0,255), cv2.FILLED)
        cv2.circle(img , (cx,cy) , 15 , (255,0,255), cv2.FILLED)
        cv2.line(img ,(x1,y1), (x2,y2) , (255,0,255) , 5 )
        length = math.hypot(x2-x1,y2-y1) 
        if length<140:
            cv2.line(img ,(x1,y1), (x2,y2) , (255,255,255) , 5 )
        
        vol = np.interp(length,[30,200 ],[minvol,maxvol])
        volume.SetMasterVolumeLevel(vol, None)
        print(vol)
    cv2.imshow("image",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break