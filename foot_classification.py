#-*- coding: utf-8 -*-
import cv2 as cv
import numpy as np

def classification_by_footindex(Rate):
    if Rate >= 40.2:
        print("Borader")
    elif Rate < 40.2 and Rate >= 36.8:
        print("Standard")
    elif Rate < 36.8:
        print("Slender")

def classification_by_toelength(start_y, end_y):
    #convert pixels to millimeters
    pixel_to_mm = (end_y - start_y) * float(foot_high) / float(pixel_footlength)
    print('toe length diff :', abs(pixel_to_mm))


    if (which_foot == 'right'):
        if ( start_y < end_y and abs(end_y - start_y) > pixel_to_mm ):
            print("egyption type")
        elif( abs(end_y - start_y) < pixel_to_mm ):
            print("squared type")
        elif ( start_y > end_y and  abs(end_y - start_y) > pixel_to_mm ):
            print("greek type")

    if (which_foot == 'left'):
        if ( start_y < end_y and abs(end_y - start_y) > pixel_to_mm ):
            print("greek type")
        elif( abs(end_y - start_y) < pixel_to_mm ):
            print("squared type")
        elif ( start_y > end_y and  abs(end_y - start_y) > pixel_to_mm ):
            print("egyption type")

end_x = 0
end_y = 50000
flag = -1

#foot image
img_color = cv.imread('ICTC_Foot_ImageProcessing/image/egyptian.png')
#gaussian blur
img_gaussian = cv.GaussianBlur(img_color, (5,5), 0)
#RGB to YCbCr
img_ycbcr = cv.cvtColor(img_gaussian, cv.COLOR_BGR2YCrCb)
#YCbCr range
img_mask = cv.inRange(img_ycbcr,np.array([0,135,75]),np.array([255,180,130]))
#morpology
kernel = np.ones((2,2), np.uint8)
result = cv.morphologyEx(img_mask, cv.MORPH_OPEN, kernel)
#dilate
img_dilation = cv.dilate(result, kernel, iterations = 1)
#erode
img_erosion = cv.erode(img_dilation, kernel, iterations = 1)
#draw contour
contours, hierarchy = cv.findContours(result, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

#find max_area
max_area = 0
for cnt in contours:
    area = cv.contourArea(cnt)

    if area > max_area:
        max_area = area

#draw max_area (foot outline)
cv.drawContours(img_color, [cnt], 0, (0, 0, 255), 10)  #red

#draw convex hull
for cnt in contours:
    hull = cv.convexHull(cnt, returnPoints = False)
    area = cv.contourArea(cnt)
    defects = cv.convexityDefects(cnt, hull)

    if area == max_area:

        for i in range(defects.shape[0]):
            s,e,f,d = defects[i,0]
            start = tuple(cnt[s][0])
            end = tuple(cnt[e][0])
            far = tuple(cnt[f][0])

            #find connection between big toe and second toe
            if d > 500:

                if end[1] < end_y:
                    start_x = start[0]
                    start_y = start[1]
                    end_x = end[0]
                    end_y = end[1]

                # print("endpoint : ", end)
                # print("startpoint:", start)



#store image
# cv.imwrite("ICTC_Foot_ImageProcessing/foot1/foot1_ycrcb.jpg", img_ycbcr
#)
# cv.imwrite("ICTC_Foot_ImageProcessing/foot1/foot1_mask.jpg", img_mask)
# cv.imwrite("ICTC_Foot_ImageProcessing/foot1/foot1_contour.jpg", img_color)

# print("start point: ", start_x, start_y)
# print("end point: ", end_x, end_y)

#draw connection between two toes
cv.line(img_color, (start_x,start_y), (end_x,end_y), [255, 0, 0], 10)
#obtain end points of two toes
cv.circle(img_color, (start_x,start_y), 15, [20,255,20], -1)
cv.circle(img_color, (end_x,end_y), 15, [150,150,150], -1)

#find end points 
leftmost = tuple(cnt[cnt[:,:,0].argmin()][0])
rightmost = tuple(cnt[cnt[:,:,0].argmax()][0])
topmost = tuple(cnt[cnt[:,:,1].argmin()][0])
bottommost = tuple(cnt[cnt[:,:,1].argmax()][0])

# print("left end point: ", leftmost)
# print("right end point: ", rightmost)
# print("top end point: ", topmost)
# print("bottom end point: ", bottommost)

#find pixel of length and width
pixel_footlength = bottommost[1]-topmost[1]
pixel_footwidth = rightmost[0]-leftmost[0]
Rate = (pixel_footwidth/pixel_footlength) * 100

#draw circle
cv.circle(img_color,leftmost,7,(100,255,100),-1)
cv.circle(img_color,rightmost,7,(100,255,100),-1)
cv.circle(img_color,topmost,7,(100,255,100),-1)
cv.circle(img_color,bottommost,7,(100,255,100),-1)

#draw footlength and width
cv.line(img_color, leftmost, (rightmost[0], leftmost[1]), [200, 200, 150], 3)
cv.line(img_color, topmost, (topmost[0], bottommost[1]), [200, 200, 150], 3)

#user information
which_foot = input("which foot? (left or right): ")
foot_high = input("your foot length: ")
print("your foot width: ", float(foot_high) * pixel_footwidth / pixel_footlength)
print("length : ", pixel_footlength, "pixels")
print("width  : ", pixel_footwidth, "pixels")
print("foot index : ", Rate ) 

#classification by the foot index
classification_by_footindex(Rate)

#classification by the toe length
classification_by_toelength(start_y, end_y)


cv.imwrite("ICTC_Foot_ImageProcessing/result_of_image/ycbcr.jpg", img_ycbcr)
cv.imwrite("ICTC_Foot_ImageProcessing/result_of_image/mask.jpg", img_mask)
cv.imwrite("ICTC_Foot_ImageProcessing/result_of_image/result.jpg", img_color)

cv.imshow("ycbcr", img_ycbcr)
cv.imshow("mask", img_mask)
cv.imshow("result", img_color)


cv.waitKey(0)
