import cv2
import numpy as np

kernel = np.ones((5,5), np.uint8)
img = cv2.imread("resources/lena.png")

imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 0)
imgCanny = cv2.Canny(img, 150, 200)
imgDilation = cv2.dilate(imgCanny, kernel, iterations=1)
imgErosion = cv2.erode(imgDilation, kernel, iterations=1)

cv2.imshow("Orjinal resim", img)
cv2.imshow("Gri seviye", imgGray)
cv2.imshow("Blur resim", imgBlur)
cv2.imshow("Kenar algilama", imgCanny)
cv2.imshow("Dilation resmi", imgDilation)
cv2.imshow("Erosion resmi", imgErosion)
cv2.waitKey(0)