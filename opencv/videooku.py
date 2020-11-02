import cv2

genislik = 640
yukselik = 480

cap = cv2.VideoCapture("resources/bbgk4b1.mp4")

while True:
    success, img = cap.read()
    img = cv2.resize(img, (genislik, yukselik))
    cv2.imshow("Video", img)
    if cv2.waitKey(1) == ord('q'):
        break