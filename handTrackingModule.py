""" HAND TRACKING MODULE"""


import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self, mode =False, maxHands = 2, detectionCon = 0.5, trackCon = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mphands = mp.solutions.hands
        self.hands = self.mphands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # converting to RGB images
        self.results = self.hands.process(imgRGB)  # for proceesing the image
        # print(results.multi_hand_landmarks)      #just in case if we want to see if its working
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mphands.HAND_CONNECTIONS)  # for drawing hand connections and dots
        return img

    def findPosition(self, img, handNo=0, draw=True):
            lmlist = []                       # storing the data of the hand positions along with X and Y plot
            if self.results.multi_hand_landmarks:
                myHand = self.results.multi_hand_landmarks[handNo]
                for id, lm in enumerate(myHand.landmark):
                    # print(id, lm) this statement to find the decimal point of the landmark
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    # print(id, cx, cy)  # position in int form
                    lmlist.append([id, cx, cy])    #adding the data of the X and Y on the list
                    # if id == 0:  # for detecting the landmark 0 and we can change this to check which finger we want to trace
                    if draw:
                        cv2.circle(img, (cx, cy), 8, (255, 0, 255), cv2.FILLED)



            return lmlist





def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmlist = detector.findPosition(img)
        if len(lmlist) != 0:
            print(lmlist[4])  # 4 here is the tip of the thump


        cTime = time.time()
        fps = 1 / (cTime - pTime)  # for fps
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255),
                    3)  # for printing fps on the screen

        cv2.imshow("Image", img)
        cv2.waitKey(1)



if __name__ == "__main__":
    main()