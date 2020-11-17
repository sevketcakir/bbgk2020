import cv2
from fonksiyonlar import stackImages
import numpy as np

def onisleme(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(5,5),1)
    imgCanny = cv2.Canny(imgBlur, 200, 200)
    kernel = np.ones((7,7))
    imDila = cv2.dilate(imgCanny, kernel, iterations=3)
    imgThres = cv2.erode(imDila, kernel, iterations=1)
    return imgThres

def sirala(noktalar):
    noktalar = noktalar.reshape((4,2))
    # print(noktalar)
    yeniNoktalar = np.zeros((4,1,2), np.int32)
    toplam = noktalar.sum(1)
    # print(toplam)
    yeniNoktalar[0] = noktalar[np.argmin(toplam)]
    yeniNoktalar[3] = noktalar[np.argmax(toplam)]
    fark = np.diff(noktalar, axis=1)
    yeniNoktalar[1] = noktalar[np.argmin(fark)]
    yeniNoktalar[2] = noktalar[np.argmax(fark)]
    # print(yeniNoktalar)
    return yeniNoktalar

def dondur(img, biggest, gen, yuk):
    biggest = sirala(biggest)
    pts1 = np.float32(biggest)
    pts2 = np.float32([[0,0],[gen,0],[0,yuk],[gen,yuk]])
    matris = cv2.getPerspectiveTransform(pts1, pts2)
    imgOutput = cv2.warpPerspective(img, matris, (gen, yuk))
    imgCropped = imgOutput[20:imgOutput.shape[0]-20,20:imgOutput.shape[1]-20]
    imgCropped = cv2.resize(imgCropped, (gen, yuk))
    return imgCropped

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
    cap = cv2.VideoCapture("resources/b5.mp4")
    gen, yuk = 540, 640
    success = True
    while success:
        success, img = cap.read()
        if not success:
            break
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        imgContour = img.copy()
        imgThres = onisleme(img)
        biggest = getContours(imgThres, imgContour)
        if biggest.size != 0:
            imgWarped = dondur(img, biggest, gen, yuk)
            stacked = stackImages(0.4,[imgContour, imgWarped])
        else:
            stacked = stackImages(0.4, [imgContour, img])
        cv2.imshow("resim", stacked)

        if cv2.waitKey(100) == ord('q'):
            break