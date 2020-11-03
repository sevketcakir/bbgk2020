import cv2

img = cv2.imread("resources/lambo.png")
print(img.shape)

imgResize = cv2.resize(img, (1000,500))
print(imgResize.shape)

imgCropped = img[0:200, 200:500]

cv2.imshow("Orjinal", img)
cv2.imshow("Boyutu degistirlmis", imgResize)
cv2.imshow("Kirpilmis resim", imgCropped)
cv2.waitKey(0)
