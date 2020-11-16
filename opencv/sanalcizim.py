import cv2
import numpy as np
from fonksiyonlar import *

def findColors(img, renkler, imgResult, cizimRenk):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    newpoints = []
    for count, renk in enumerate(renkler):
        lower = np.array(renk[0:3])
        upper = np.array(renk[3:6])
        maske = cv2.inRange(imgHSV, lower, upper)
        x,y = getContours(maske)
        cv2.circle(imgResult, (x,y), 15, cizimRenk[count], cv2.FILLED)
        if x!=0 and y!=0:
            newpoints.append([x,y,count])
    return newpoints


def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        alan = cv2.contourArea(cnt)
        if alan>500:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x+w//2, y

def tuvaleCiz(img, noktalar, cizimRenkler):
    for nokta in noktalar:
        cv2.circle(img, (nokta[0],nokta[1]), 10, cizimRenkler[nokta[2]], cv2.FILLED)

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    renkler = [
        [108, 143, 8, 120, 255, 193], #Mavi kalem
        [167, 87, 24, 179, 255, 212]
    ]
    cizimRenk = [[255, 0, 0],
                 [0,0,255]]
    noktalar = [] # [x,y,renk]
    while True:
        success, img = cap.read()
        imgResult = img.copy()
        newpoints = findColors(img, renkler, imgResult, cizimRenk)
        noktalar.extend(newpoints)
        if len(noktalar)!=0:
            tuvaleCiz(imgResult, noktalar, cizimRenk)
        stacked = stackImages(0.5, [imgResult])
        cv2.imshow("Sonuc", stacked)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        elif key == ord('r'):
            noktalar = []

