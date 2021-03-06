import numpy as np
import threading
import cv2
from statistics import mean
import math
import serial 
port="/dev/ttyACM0"
rate=9600
s1=serial.Serial(port,rate)
s1.flushInput()

font                   = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (160,50)
fontScale              = 1
fontColor              = (255,0,0)
lineType               = 2

#Constants
#Segmentation On Lower Half of The Frame
seg1 = [np.array([[0,120],[0,150],[320,120],[320,150]],dtype=np.int32)]
seg2 = [np.array([[0,150],[0,180],[320,150],[320,180]],dtype=np.int32)]
seg3 = [np.array([[0,180],[0,210],[320,180],[320,210]],dtype=np.int32)]
seg4 = [np.array([[0,210],[0,240],[320,210],[320,240]],dtype=np.int32)]
vertices = [np.array([[0,240],[320,240],[160,0]],dtype=np.int32)]  

def communicate (a):
    a=a+","
    if s1.inWaiting()>0:
        print(a)
        s1.write(a.encode())

def getAngle(a, b, c):
    ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    return -(ang - 90) if ang < 0 else 90-ang

def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    if len(img.shape) > 2:
        channel_count = img.shape[2]  
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

vertices = [np.array([[0,240],[320,240],[160,0]],dtype=np.int32)]

def image_processing(frame):
        blur=cv2.GaussianBlur(frame,(5,5),0)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        low = np.array([0, 120, 70])
        high = np.array([10, 255, 255])
        mask1 = cv2.inRange(hsv, low, high)
        low = np.array([170, 120, 70])
        high = np.array([180, 255, 255])
        mask2 = cv2.inRange(hsv, low, high)
        mask=mask1+mask2      
        erosion=cv2.erode(mask,kernel,iterations=3)
        dilation=cv2.dilate(erosion,kernel,iterations=5)
        closing=cv2.morphologyEx(dilation,cv2.MORPH_CLOSE,kernel)
        th2=cv2.Canny(closing,75,150)
#         dilation2=cv2.dilate(th2,kernel,iterations=5)
        return th2
def segmentation(image,seg):
    frm = region_of_interest(image,seg)
    f_pix = np.argwhere(frm == 255)
    average = [sum(x)/len(x) for x in zip(*f_pix)]
    if len(average)>0 : 
        f_cx = int(round(average[1]))
        f_cy = int(round(average[0]))
        if f_cy < 150:
            f_cy = 135
        if f_cy>150 and f_cy<180:
            f_cy = 165
        if f_cy>180 and f_cy<210:
            f_cy = 195
        if f_cy>210:
            f_cy = 225
    else:
        f_cx = 160
        f_cy = 160
    cv2.circle(image,(f_cx,f_cy),2,(255,0,0),2)
    return f_cx
    

def contour_center(th2):
    contours,hierarchy = cv2.findContours(th2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) 
#     cv2.drawContours(th2,contours,-1,(0,255,0),3)
    if len(contours)<0:
        for cnt in contours:
           if cnt is not None:
               area = cv2.contourArea(cnt)# find the area of contour
           if area>0 :
            # find moment and centroid
            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
        return cx
    else:
        return 160
    

    #*****Main Program *******#
    
cap = cv2.VideoCapture(0)
cap.set(3,320.0) #set the size
cap.set(4,240.0)  #set the size
cap.set(5,15)  
kernel=np.ones((5,5),np.uint8)
frames=[]
count=0
while(True):
    image=np.zeros((240,320,3),np.uint8)
    ret, frame = cap.read()
    gray = frame
    img = image_processing(gray)
    cx1 = segmentation(image=img,seg=seg1)
    cx2 = segmentation(image=img,seg=seg2)
    cx3 = segmentation(image=img,seg=seg3)
    cx4 = segmentation(image=img,seg=seg4)

    direction_X = int(round(mean([cx1,cx2,cx3,cx4])))
    img = cv2.line(img, (160,240), (direction_X,120), (255, 0, 0) , 3) 

    direction_angle = int(round(getAngle((direction_X, 120), (160, 240), (160,120))))
    direction_final="S"
    direction_angle=str(direction_angle)
    if direction_X < 140:
        direction_final = "L "+direction_angle
    if direction_X > 180:
       direction_final = "R "+ direction_angle
    if direction_X>141 and direction_X<179:
       direction_final = "S "+direction_angle
    cv2.putText(img,direction_final, 
    bottomLeftCornerOfText, 
    font, 
    fontScale,
    fontColor,
    lineType)
    disr=str(direction_angle)
    communicate(disr)
    cv2.imshow('input',frame)
    cv2.imshow('output',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

	
			
       
 
