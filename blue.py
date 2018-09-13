import cv2
#import serial
import numpy as np
cap=cv2.VideoCapture(1)
#s=serial.Serial('/dev/ttyUSB0',9600)
width=int(cap.get(3))
width=int(width/2)
#s.write(width)
while 1:
	_, img = cap.read()
	hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
	red_lower=np.array([150,20,20]) #110 115 150
	red_upper=np.array([255,2555,255]) #130 255 255                        110,115,150,130,255,255
	red=cv2.inRange(hsv,red_lower,red_upper)
	bmask = cv2.GaussianBlur(red, (5,5),0)
	kernal=np.ones((5,5)) ##
	red=cv2.erode(red,kernal)
	red=cv2.dilate(red,kernal)
	res=cv2.bitwise_and(img,img,mask=red)
	(_,contours, hierarchy)=cv2.findContours(red,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	
	if len(contours)>0:
		largest = 0
		area = 0
		for i in range(len(contours)):
			temp_area = cv2.contourArea(contours[i])
			if temp_area > area:
				area = temp_area
				largest = i
		coordinates = cv2.moments(contours[largest])
		x = int(coordinates['m10']/coordinates['m00'])
		y = int(coordinates['m01']/coordinates['m00'])
		diam = int(np.sqrt(area)/4)
		cv2.circle(res,(x,y),diam,(0,255,0),1)
		cv2.line(res,(x-2*diam,y),(x+2*diam,y),(0,255,0),1)
		cv2.line(res,(x,y-2*diam),(x,y+2*diam),(0,255,0),1)
		#s.write(width)
		if x > width :
			print ("clockwise")
			#print width
			print (x-width)
		else:
			print ("anticlockwise")
			print (x-width)
			#print width
	cv2.imshow("color Tracking",img)
	cv2.imshow("rk",res)
	

	if cv2.waitKey(10) & 0xFF == ord('q'):
		cap.release()
		cv2.destroyAllWindows()
		break