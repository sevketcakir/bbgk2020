import cv2
import numpy as np

kernel = np.ones((5,5), np.uint8)
img = cv2.imread("resources/lena.png")

imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


cv2.imshow("Orjinal resim", img)
cv2.imshow("Gri seviye", imgGray)
cv2.waitKey(0)