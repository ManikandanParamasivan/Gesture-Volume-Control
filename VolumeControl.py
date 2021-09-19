import cv2
import time
import numpy as np
import handTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam, hCam = 1280, 720

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon = 0.9)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()

minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar =400

while True:
    success, img = cap.read()
    img = detector.findHands(img)  # for finding location of hands we us the function of the handtracking module
    lmlist = detector.findPosition(img, draw = False)
    if len(lmlist) != 0:
        print(lmlist[4], lmlist[8])
        x1, y1 = lmlist[4][1], lmlist[4][2]
        x2, y2 = lmlist[8][1], lmlist[8][2]
        cx, cy = (x1+x2) // 2, (y1+y2) // 2

        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx , cy), 15, (255, 0, 255), cv2.FILLED)  #for making a circle in between both the fingers

        length = math.hypot(x2-x1,y2-y1)   #distance between both the fingers
        vol = np.interp(length, [50, 300], [minVol, maxVol]) #using numpy to convert our hand range to vol range
        volBar = np.interp(length, [50, 300], [400, 150])  #for conversion to use it on the bar
        volume.SetMasterVolumeLevel(vol, None)


        if length<50:
            cv2.circle(img, (cx,cy), 15, (0, 255, 0), cv2.FILLED)

    cv2.rectangle(img, (50,150), (85,400), (255, 0, 0), 3)         #To display the volume change box
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)  #the moving filled part of the box
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40,50), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 3)

    cv2.imshow("img", img)
    cv2.waitKey(1)