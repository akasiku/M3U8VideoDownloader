import os

import cv2
import numpy as np
def empty():
    pass
def showDir():
    dirlist = os.listdir()
    li=[]
    for i in dirlist:
        if i.endswith(("png","PNG","JPG","jpg","jepg","JEPG","webp","WEBP")):
            li.append(i)
    if len(li)>0:
        for i, j in enumerate(li):
            print(f"{i}  -------->  {j}")
        return li
    else:
        print("没能找到图片文件(jpg,png,jepg)")
try:
	li=showDir()
	ta=int(input("输入压缩目标："))
	pa=li[ta]
except:
	print("出错了")

img=cv2.imread(pa)
hsv=cv2.cvtColor(img,cv2.COLOR_RGB2HSV)
cv2.namedWindow("control")
cv2.resizeWindow("control",600,350)
cv2.createTrackbar("hue min","control",0,179,empty)
cv2.createTrackbar("hue max","control",179,179,empty)
cv2.createTrackbar("sat min","control",0,255,empty)
cv2.createTrackbar("sat max","control",255,255,empty)
cv2.createTrackbar("val min","control",0,255,empty)
cv2.createTrackbar("val max","control",255,255,empty)
while True:
    h_min=cv2.getTrackbarPos("hue min","control")
    h_max=cv2.getTrackbarPos("hue max","control")
    s_min=cv2.getTrackbarPos("sat min","control")
    s_max=cv2.getTrackbarPos("sat max","control")
    v_min=cv2.getTrackbarPos("val min","control")
    v_max=cv2.getTrackbarPos("val max","control")
    print(h_min,h_max,s_min,s_max,v_min,v_max)
    lowwer=np.array([h_min,s_min,v_min])
    upper=np.array([h_max,s_max,v_max])
    ff=cv2.inRange(hsv,lowwer,upper)
    result=cv2.bitwise_and(img,img,mask=ff)
    cv2.imshow("result",result)
    cv2.imshow("xx",img)
    cv2.imshow("ff",ff)
    cv2.imshow("hsv",hsv)
    cv2.waitKey(1)