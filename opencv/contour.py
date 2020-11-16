import cv2
import numpy as np
from fonksiyonlar import stackImages, getContours

if __name__ == '__main__':
    path = "resources/shapes.png"
    img = cv2.imread(path)
    imgContour = img.copy()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (7,7), 1)
    imgCanny = cv2.Canny(imgBlur, 50, 50)
    getContours(imgCanny, imgContour)
    imgBlank = np.zeros_like(img)
    imgStack = stackImages(1, [[img, imgContour, imgBlur], [imgCanny, imgGray, imgBlank]])
    cv2.imshow("Stack", imgStack)
    cv2.waitKey(0)