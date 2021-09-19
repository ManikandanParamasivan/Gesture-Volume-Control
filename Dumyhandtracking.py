
# THE DUMMY FILE TO RUM HANDTRACKING MODULE HERE

import cv2
import mediapipe as mp
import time
import handTrackingModule as htm

pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)
detector = htm.handDetector()

while True:
    success, img = cap.read()
    img = detector.findHands(img)   # add arugument draw = false if u dont wanna draw
    lmlist = detector.findPosition(img) #add arugment draw = false if u dont wanna draw
    if len(lmlist) != 0:
        print(lmlist[4])  # 4 here is the tip of the thump


    cTime = time.time()
    fps = 1 / (cTime - pTime)  # for fps
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)  # for printing fps on the screen

    cv2.imshow("Image", img)
    cv2.waitKey(1)