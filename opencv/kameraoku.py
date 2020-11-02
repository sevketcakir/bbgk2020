import cv2

genislik = 640
yukseklik = 480

cap = cv2.VideoCapture(0)
#cap.set(3, genislik)
#cap.set(4, yukseklik)
#cap(10, 150)
while True:
    success, img = cap.read()
    cv2.imshow("Kamera", img)
    if cv2.waitKey(1) == ord('q'):
        break