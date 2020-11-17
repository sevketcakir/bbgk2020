#https://github.com/muratlutfigoncu/turkish-license-plate-detector
#https://www.kaggle.com/andrewmvd/car-plate-detection
#https://www.kaggle.com/pcmill/license-plates-on-vehicles

#Plaka resimlerini yukardaki kaynaklardan indirip ilgili klasöre kaydetmek gerekir.
from setuptools import glob
import cv2
from fonksiyonlar import stackImages

if __name__ == '__main__':
    images = []
    for file in glob.glob("resources/plates/[!.][!_]*.png"): #._ ile başlayanları almayacak
        images.append(file)

    # Hata 1: "resouces" şeklinde yazılmış
    siniflandirici = cv2.CascadeClassifier("resources/haarcascades/haarcascade_russian_plate_number.xml")

    basarili, basarisiz = 0, 0
    for image in images:
        img = cv2.imread(image)
        if img is None:
            continue
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # cv2.imshow("resim", img)
        # cv2.waitKey(1000)
        plakalar = siniflandirici.detectMultiScale(imgGray, 1.1, 10)

        if len(plakalar)==0:
            basarisiz += 1
        else:
            basarili += 1

        for x, y, w, h in plakalar:
            if w*h>200:
                cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,255), 2)
                imgRoi = img[y:y+h,x:x+w].copy()
                # Gri seviye resim stacklemede sorun var
                stacked = stackImages(0.5,[img, imgRoi])
                cv2.imshow("Plaka", stacked)
                cv2.waitKey(1)

    print(f"{basarili+basarisiz} resimden {basarili} tanesi algılandı, {basarisiz} tanes algılanamadı")