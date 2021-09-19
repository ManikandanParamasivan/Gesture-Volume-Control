import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mphands = mp.solutions.hands
hands = mphands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0


while True:
    success, img = cap.read()

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)     #converting to RGB images
    results = hands.process(imgRGB)    #for proceesing the image
    #print(results.multi_hand_landmarks)      #just in case if we want to see if its working
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                #print(id, lm) this statement to find the decimal point of the landmark
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                print(id, cx, cy)   #position in int form
                if id == 0:          #for detecting the landmark 0 and we can change this to check which finger we want to trace
                    cv2.circle(img, (cx, cy), 25, (255,0,255), cv2.FILLED)
            mpDraw.draw_landmarks(img, handLms, mphands.HAND_CONNECTIONS)   #for drawing hand connections and dots


    cTime = time.time()
    fps = 1/(cTime - pTime)    #for fps
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)   #for printing fps on the screen

    cv2.imshow("Image", img)
    cv2.waitKey(1)





