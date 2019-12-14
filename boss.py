import cv2
import numpy as np
import RPi.GPIO as gpio
import time
capture = cv2.VideoCapture(0)  #read the video
capture.set(3,320.0) #set the size
capture.set(4,240.0)  #set the size
capture.set(5,15)  #set the frame rate
kernel=np.ones((5,5),np.uint8)

def init():
 gpio.setmode(gpio.BCM)
 gpio.setup(17, gpio.OUT)#i1
 gpio.setup(22, gpio.OUT)#i2
 gpio.setup(23, gpio.OUT)#i3
 gpio.setup(24, gpio.OUT)#i4

def forward(sec):
 init()
 gpio.output(17, True)
 gpio.output(22, False)
 gpio.output(23, True)
 gpio.output(24, False)
 time.sleep(sec)
 gpio.cleanup()

def reverse(sec):
 init()
 gpio.output(17, False)
 gpio.output(22, True)
 gpio.output(23, False)
 gpio.output(24, True)
 time.sleep(sec)
 gpio.cleanup()

def left(sec):
 init()
 gpio.output(17, False)
 gpio.output(22, True)
 gpio.output(23, True)
 gpio.output(24, False)
 time.sleep(sec)
 gpio.cleanup()

def right(sec):
 init()
 gpio.output(17, True)
 gpio.output(22, False)
 gpio.output(23, False)
 gpio.output(24, True)
 time.sleep(sec)
 gpio.cleanup()



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


for i in range(0,2):
    flag, trash = capture.read()
while cv2.waitKey(1) != 27:
        flag, frame = capture.read() #read the video in frames
        #gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)#convert each frame to grayscale.
        blur=cv2.GaussianBlur(frame,(5,5),0)#blur the grayscale image
      
#  ret1,th1 = cv2.threshold(blur,220,255,cv2.THRESH_BINARY)# invert the pixels of the image frame
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
        dilation2=cv2.dilate(th2,kernel,iterations=5)
        th3=region_of_interest(th2, vertices)

        img,contours,hierarchy = cv2.findContours(th2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) #find the contours
        cv2.circle(frame,(160,120),10,(0,255,0),1)
        cv2.circle(frame,(160,120),2,(255,0,0),2)
        cv2.drawContours(frame,contours,-1,(0,255,0),3)
        cv2.imshow('frame',frame) #show video
        #cv2.imshow('frame1',th3)
        #cv2.imshow('frame3',rect)
        for cnt in contours:
           if cnt is not None:
               area = cv2.contourArea(cnt)# find the area of contour
           if area>0 :
            # find moment and centroid
            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            print(cx)
            #print(cy)
            if 150<=cx<=180:
                print("straight")
                forward(0.05)
            elif cx<150:
                print("LEFT")
                left(0.05)
                forward(0.02)
            elif cx>180:
                print("RIGHT")                            
                right(0.05)
                forward(0.02)

