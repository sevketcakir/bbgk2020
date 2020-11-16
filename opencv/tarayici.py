import cv2
from fonksiyonlar import stackImages
import numpy as np

def onisleme(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(5,5),1)
    imgCanny = cv2.Canny(imgBlur, 200, 200)
    kernel = np.ones((5,5))
    imDila = cv2.dilate(imgCanny, kernel, iterations=2)
    imgThres = cv2.erode(imDila, kernel, iterations=1)
    return imgThres

def sirala(noktalar):
    pass

def dondur(img, biggest):
    pass

def getContours(img, imgContour):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    biggest = np.array([])
    maxArea = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>5000:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            if area>maxArea and len(approx)==4:
                biggest = approx
                maxArea = area
    cv2.drawContours(imgContour, biggest, -1, (255,0,0), 20)
    return biggest

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    gen, yuk = 540, 640

    while True:
        success, img = cap.read()
        imgContour = img.copy()
        imgThres = onisleme(img)
        biggest = getContours(imgThres, imgContour)
        
        stacked = stackImages(0.4,[imgContour, imgThres])
        cv2.imshow("resim", stacked)

        if cv2.waitKey(1) == ord('q'):
            break