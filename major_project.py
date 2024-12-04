from re import M
from sre_constants import SUCCESS
import cv2
import mediapipe as mp
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as nm

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# volume.GetMute()
# volume.GetMasterVolumeLevel()

volRange = volume.GetVolumeRange()
minVol= volRange[0]
maxVol= volRange[1]
# volume.SetMasterVolumeLevel(-20.0, None)
volume.SetMasterVolumeLevel(0.0, None)


mpDraw = mp.solutions.drawing_utils
mpHands = mp.solutions.hands
hands = mpHands.Hands()


cap = cv2.VideoCapture(0)
while True:
    success,img = cap.read()
    results =  hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lmList=[]
            for id, lm in enumerate(handLms.landmark):
                    h,w,c=img.shape
                    # print(id,lm)
                    cx,cy =int(lm.x*w), int (lm.y*h)
                    lmList.append([id,cx,cy])
                    # print(lmList)

            mpDraw.draw_landmarks(img,handLms , mpHands.HAND_CONNECTIONS)

            if lmList:
                x1,y1=lmList[4][1],lmList[4][2]
                x2,y2=lmList[8][1],lmList[8][2]
                cv2.circle(img,(x1,y1),15,(1,12,12),cv2.FILLED)
                cv2.circle(img,(x2,y2),15,(1,12,12),cv2.FILLED)
                cv2.line(img,(x1,y1),(x2,y2),(1,12,12),3)
                length= math.hypot((x2-x1),(y2-y2))
                # print(length)
                vol = nm.interp(length, [20,100],[minVol,maxVol])
                volume.SetMasterVolumeLevel(vol, None)

                

    cv2.imshow("Image",img)
    cv2.waitKey(1)



# lenght = 0->200
# volRange 0:-65.25  ---->>>  200:0.0
