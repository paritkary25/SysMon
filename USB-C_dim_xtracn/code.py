# Filename: code.py
# Author: Yash Paritkar
# Created: 2025/02/19 19:31
# Last Modified: Wednesday 19 February 2025 03:42:05 AM
# Simple CV program to extract mechanical information from the USB-C adapter. This will help a lot in making CAD.

import cv2
import numpy as np
import time

# Reading image
img = cv2.imread('front.jpg',cv2.IMREAD_COLOR)

# Since the required outline is golden, we can use a goldenlden mask to separate the component
# HSV = (cylinderical degree of colour (theta), intensity of colour (r), brightness (h))
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower = np.array([10, 40, 30]) 
upper = np.array([90, 255, 255])

mask = cv2.inRange(hsv, lower, upper)
mb = cv2.GaussianBlur(mask, (9, 9), 2)

# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# gb = cv2.blur(gray,(4,4))

test_im = mb
cv2.imwrite('test.jpg',test_im)

detected_circles = cv2.HoughCircles(test_im,cv2.HOUGH_GRADIENT, 1, 40, param1 = 50, param2 = 30, minRadius = 30,maxRadius = 90)

if detected_circles is not None:

    detected_circles = np.uint16(np.around(detected_circles))

    for pt in detected_circles[0,:]:
        a,b,r = pt[0], pt[1], pt[2]

        cv2.circle(img, (a,b), r, (0,255,0), 2)
        
        txt = "(" + str(a) + ", " + str(b) + ")"

        cv2.circle(img, (a,b), 1, (0,255,0), 2)
        cv2.putText(img,txt,(a+1,b+1),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),3)

        cv2.putText(img,("r = " + str(r)),(a+1,b+r),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),3)

        cv2.imwrite("detected_circles.jpg",img)
