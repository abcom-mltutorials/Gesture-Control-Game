# Copyright @ 2020 ABCOM Information Systems Pvt. Ltd. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================



import numpy as np

import cv2

import pyautogui
from directKeys import  up, left, down, right
from directKeys import PressKey, ReleaseKey

# write the range of lower and upper boundaries of the "blue" object after converting it to hsv region
blueLower = np.array([50,50,50])
blueUpper = np.array([180,180,155])
#declare a variable to capture the real time video of our webcam
video = cv2.VideoCapture(0); 

#set the initial values for parameter to use them later in the code
current_key = set()
#set radius of circle for covering the object
radius_of_circle = 15
#set window size of grabbed frame
window_size = 160
#use Loop until OpenCV window is not closed
while True:
    keyPressed = False
    keyPressed_lr= False
    # to grab the current frame from webcam
    _, grabbed_frame = video.read()
    height,width = grabbed_frame.shape[:2]
    '''GaussianBlur	(	InputArray 	src,
                        OutputArray 	dst,
                        Size 	ksize,
                        double 	sigmaX,
                        double 	sigmaY = 0,
                        int 	borderType = BORDER_DEFAULT)	'''
    #above is the basic syntax of gaussianblur attribute here in our code input array is grabbed_frame, ksize=(11,11) and sigmaY=0
    #the official documentation where you will find the purpose of each element in detail is in below comment
    #https://docs.opencv.org/3.1.0/d4/d86/group__imgproc__filter.html#gaabe8c836e97159a9193fb0b11ac52cf1
    # blur the captured image to make the image smooth and then convert it in hsv color
    #grabbed_frame = imutils.resize(grabbed_frame, width=600)
    
    grabbed_frame = cv2.resize(grabbed_frame, dsize=(600, height))
    blur_frame = cv2.GaussianBlur(grabbed_frame, (11, 11), 0)
    hsv_value = cv2.cvtColor(blur_frame, cv2.COLOR_BGR2HSV)

    # create a cover for object so that you are able to detect the object easily without any
    #  distraction by other details of image you are capturing
    cover = cv2.inRange(hsv_value, blueLower, blueUpper)
    #Erode the masked output
    cover = cv2.erode(cover, None, iterations=2)
    #Dilate the resultant image
    cover = cv2.dilate(cover, None, iterations=2)
    


    # here we will divide the frame into two halves one for up and down keys
    # and other half is for left and right keys by using indexing
    left_cover = cover[:,0:width//2,]
    right_cover = cover[:,width//2:,]

    #define a function to extract the countours from the list 
    def extract_contour(contours):
        if len(contours) == 2:
            contours = contours[0]
            
        elif len(contours) == 3:
            contours = contours[1]

        else:
            raise Exception(("Contours tuple must have length 2 or 3," 
            "otherwise OpenCV changed their cv2.findContours return "
            "signature. Refer to OpenCV's documentation "
            "in that case"))

        return contours
            
    #contours in the left and right frame to find the shape outline of the object for left side
    contour_l = cv2.findContours(left_cover.copy(),
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    #use the defined function to extract from contour_l
    contour_l = extract_contour(contour_l)
    left_centre = None
#RETR_EXTERNAL is for exctracting only outer contour in heirarchy and we use CHAIN_APPROX_SIMPLE here to detect only main point of contour instead of all boundary point
#https://docs.opencv.org/3.4/d9/d8b/tutorial_py_contours_hierarchy.html you can visit this site also for the same
    contour_r = cv2.findContours(right_cover.copy(),
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    #use the defined function to extract from contour_r
    contour_r = extract_contour(contour_r)
    right_centre = None

    # start looping if at least one contour or centre is found in left side of frame
    if len(contour_l) > 0:
        #for creating a circular contour with centroid
        c = max(contour_l, key=cv2.contourArea)
        ((x, y), r) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        #below is formula for calculating centroid of circle
        left_centre = (int(M["m10"] / (M["m00"]+0.000001)), int(M["m01"] / (M["m00"]+0.000001)))

        # if the radius meets a minimum size to avoid small distraction of same color then mark it in frame
        if r > radius_of_circle:
            # draw the circle and centroid on the frame,
            cv2.circle(grabbed_frame, (int(x), int(y)), int(r),
                (0, 255, 0), 2)
            cv2.circle(grabbed_frame, left_centre, 5, (0, 255, 0), -1)

           #set positions where left and right key will be detected
            if left_centre[1] < (height/2 - window_size //2):
                cv2.putText(grabbed_frame ,'LEFT',(20,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
                #pyautogui is for clicking left key through gesture
                pyautogui.press('left')
                current_key.add(left)
                keyPressed = True
                keyPressed_lr=True
            elif left_centre[1] > (height/2 + window_size //2):
                cv2.putText(grabbed_frame,'RIGHT',(20,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
                pyautogui.press('right') #pyautogui is for clicking right key through gesture
                current_key.add(right)
                keyPressed = True
                keyPressed_lr=True

    # start looping if at least one contour or centre is found in right side of frame
    if len(contour_r) > 0:
        c2 = max(contour_r, key=cv2.contourArea)
        ((x2, y2), r2) = cv2.minEnclosingCircle(c2)
        M2 = cv2.moments(c2)
        right_centre = (int(M2["m10"] / (M2["m00"]+0.000001)), int(M2["m01"] / (M2["m00"]+0.000001)))
        right_centre = (right_centre[0]+width//2,right_centre[1])


        if r2 > radius_of_circle:
            # draw the circle and centroid on the frame,
            cv2.circle(grabbed_frame, (int(x2)+width//2, int(y2)), int(r2),
                (0, 255, 0), 2)
            cv2.circle(grabbed_frame, right_centre, 5, (0, 255,0), -1)
            if right_centre[1] < (height//2 - window_size //2):
                cv2.putText(grabbed_frame,'UP',(200,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
                pyautogui.press('up')
                keyPressed = True
                current_key.add(up)
            elif right_centre[1] > (height//2 + window_size //2):
                cv2.putText(grabbed_frame,'DOWN',(200,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
                pyautogui.press('down')
                keyPressed = True
                current_key.add(down)

    # Below code will show the window through which you can see the detection of your object. I named it grabbed_frame
    grabbed_frame_copy = grabbed_frame.copy()
#below line is for creating the blue rectangular box and i set it for user reference because your arrow key will be pressed below and above it
    grabbed_frame_copy = cv2.rectangle(grabbed_frame_copy,(0,height//2 - window_size //2),(width,height//2 + window_size //2),(255,0,0),2)
    cv2.imshow("grabbed_frame", grabbed_frame_copy)


    #release all pressed keys to avoid any glitch


    if not keyPressed and current_key!= 0:
        for key in current_key:

            ReleaseKey(key)
            current_key=set()
 #we use hexadecimal value 0xFF here because when we will press q then it can return other values also if your numlock is activated
    k = cv2.waitKey(1) & 0xFF

    # to stop the loop
    if k == ord("q"):
        break

video.stop()
# close all windows when you will stop capturing video
cv2.destroyAllWindows()
