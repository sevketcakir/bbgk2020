import cv2
import numpy as np

img = np.zeros((512,512,3), np.uint8)

#img[:] = 255,0,0
#print(img)

cv2.line(img, (0,0), (img.shape[1], img.shape[0]), (255,0,0), 3)
cv2.rectangle(img, (0,0), (250,350),(0,0,255),2)
cv2.circle(img, (400,50), 30, (255,0,255), 5)
cv2.putText(img, "Pyhton OpenCV", (150,200), cv2.FONT_HERSHEY_COMPLEX, 1, (0,150,0), 2)

cv2.imshow("Resim", img)
cv2.waitKey(0)