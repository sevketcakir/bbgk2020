import cv2
from fonksiyonlar import stackImages

if __name__ == '__main__':
    img = cv2.imread("resources/lena.png")
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgGaussian = cv2.GaussianBlur(imgGray, (7, 7), 0)
    imgCanny = cv2.Canny(img, 150, 200)
    imgCards = cv2.imread("resources/cards.jpg")
    imgLambo = cv2.imread("resources/lambo.png")

    stacked = stackImages(0.5, [[img, imgGray, imgCards], [imgGaussian, imgLambo, imgCanny]])
    cv2.imshow("Stacked", stacked)
    cv2.waitKey(0)