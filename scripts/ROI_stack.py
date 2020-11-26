'''
Follow the guide by nathancy from stackoverflow
Link - https://stackoverflow.com/questions/60521925/how-to-detect-the-horizontal-and-vertical-lines-of-a-table-and-eliminate-the-noi
'''

import cv2 as cv
import numpy as np
import sys
import math
from preprocessing import get_grayscale, get_binary, invert_area, draw_text, detect

# Load image, grayscale, Gaussian blur, Otsu's threshold
filename = '../all/Error/5.png'
org = cv.imread(filename)
gray = cv.cvtColor(org, cv.COLOR_BGR2GRAY)
blur = cv.GaussianBlur(gray, (3,3), 0)
thresh = cv.threshold(blur, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]

# Detect horizontal lines
horizontal_kernel = cv.getStructuringElement(cv.MORPH_RECT, (50,1))
horizontal_mask = cv.morphologyEx(thresh, cv.MORPH_OPEN, horizontal_kernel, iterations=1)

# Detect vertical lines
vertical_kernel = cv.getStructuringElement(cv.MORPH_RECT, (1,50))
vertical_mask = cv.morphologyEx(thresh, cv.MORPH_OPEN, vertical_kernel, iterations=1)

# Combine masks and remove lines
table_mask = cv.bitwise_or(horizontal_mask, vertical_mask)
org[np.where(table_mask==255)] = [255,255,255]



'''
cv2.imshow('thresh', thresh)
cv2.waitKey(10)
cv2.imshow('horizontal_mask', horizontal_mask)
cv2.waitKey(10)
cv2.imshow('vertical_mask', vertical_mask)
cv2.waitKey(10)
'''
'''
### Modified & Tested Code by Thet Paing ###
minLineLength = 100
maxLineGap = 10
rho = 1
theta = np.pi/180
threshold = 100

#gray = cv2.cvtColor(, cv2.COLOR_BGR2GRAY)
#dst = cv2.Canny(table_mask, 50, 150, None, 3)
linesP = cv2.HoughLinesP(table_mask, rho , theta, threshold,minLineLength, maxLineGap) #Direct usage of table_mask image gave better result than converting Canny & Gray

## Getting lines & illustrate detected lines on the images
for i in linesP:
    #print(i)
    for x1,y1,x2,y2 in i:
        cv2.line(image,(x1,y1),(x2,y2),(0,255,0),2)
#cv2.imwrite('hough.jpg',image)

'''
'''
## OpenCV HoughLines tutorial

img = cv2.imread(filename)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 3)
minLineLength = 100
maxLineGap = 10
lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
for x1,y1,x2,y2 in lines[0]:
    cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)

cv2.imwrite('houghlines5.jpg',img)
'''
'''
cv2.namedWindow('table_mask',cv2.WINDOW_NORMAL)
cv2.resizeWindow('table_mask', 600,600)
cv2.imshow('table_mask', table_mask)
cv2.waitKey(0)
cv2.namedWindow('image',cv2.WINDOW_NORMAL)
cv2.resizeWindow('image', 600,600)
cv2.imshow('image', image)
cv2.waitKey()
'''
##### Below is copy code from ROI_selection.py and modified to work inside this code
def is_vertical(line):
    return line[0]==line[2]

def is_horizontal(line):
    return line[1]==line[3]

def overlapping_filter(lines, sorting_index):
    filtered_lines = []

    lines = sorted(lines, key=lambda lines: lines[sorting_index])

    for i in range(len(lines)):
            l_curr = lines[i]
            if(i>0):
                l_prev = lines[i-1]
                if ( (l_curr[sorting_index] - l_prev[sorting_index]) > 5):
                    filtered_lines.append(l_curr)
            else:
                filtered_lines.append(l_curr)

    return filtered_lines

def detect_lines(image, title='default', rho = 1, theta = np.pi/180, threshold = 50, minLinLength = 290, maxLineGap = 6, display = False, write = False):

    # Copy edges to the images that will display the results in BGR
    cImage = np.copy(org)

    #linesP = cv.HoughLinesP(dst, 1 , np.pi / 180, 50, None, 290, 6)
    linesP = cv.HoughLinesP(image, rho , theta, threshold, None, minLinLength, maxLineGap)

    horizontal_lines = []
    vertical_lines = []

    if linesP is not None:
        #for i in range(40, nb_lines):
        for i in range(0, len(linesP)):
            l = linesP[i][0]

            if (is_vertical(l)):
                vertical_lines.append(l)

            elif (is_horizontal(l)):
                horizontal_lines.append(l)

        horizontal_lines = overlapping_filter(horizontal_lines, 1)
        vertical_lines = overlapping_filter(vertical_lines, 0)

    count_row = []
    count_column = []

    if (display):
        for i, line in enumerate(horizontal_lines):
            cv.line(cImage, (line[0], line[1]), (line[2], line[3]), (0,255,0), 3, cv.LINE_AA)

            cv.putText(cImage, str(i) + "h", (line[0] + 5, line[1]), cv.FONT_HERSHEY_SIMPLEX,
                       0.5, (0, 0, 0), 1, cv.LINE_AA)
            count_row.append(i)
        cv.namedWindow('Hooo',cv.WINDOW_NORMAL)
        cv.resizeWindow('Hooo', 600,600)
        cv.imshow("Hooo", cImage)


        for i, line in enumerate(vertical_lines):
            cv.line(cImage, (line[0], line[1]), (line[2], line[3]), (0,0,255), 3, cv.LINE_AA)
            cv.putText(cImage, str(i) + "v", (line[0], line[1] + 5), cv.FONT_HERSHEY_SIMPLEX,
                       0.5, (0, 0, 0), 1, cv.LINE_AA)
            count_column.append(i)
        cv.namedWindow('Hooo',cv.WINDOW_NORMAL)
        cv.resizeWindow('Hooo', 600,600)
        cv.imshow("Hooo", cImage)
            #print("Count: ")
            #print(count_column)

        #cv.imshow("Source", cImage)

        #cv.imshow("Canny", cdstP)
        cv.waitKey(0)
        cv.destroyAllWindows()

    if (write):
        cv.imwrite("../Images/" + title + ".png", cImage);

    print("Count Column: ")
    print(count_column)
    return (horizontal_lines, vertical_lines, count_row[-1], count_column[-1])

def get_cropped_image(image, x, y, w, h):
    cropped_image = image[ y:y+h , x:x+w ]
    return cropped_image

def get_ROI(image, horizontal, vertical, left_line_index, right_line_index, top_line_index, bottom_line_index, offset=4):
    x1 = vertical[left_line_index][2] + offset
    y1 = horizontal[top_line_index][3] + offset
    x2 = vertical[right_line_index][2] - offset
    y2 = horizontal[bottom_line_index][3] - offset

    w = x2 - x1
    h = y2 - y1

    cropped_image = get_cropped_image(image, x1, y1, w, h)

    return cropped_image, (x1, y1, w, h)

def main(argv):

    default_file = '../Images/source6.png'
    filename = argv[0] if len(argv) > 0 else default_file

    src = cv.imread(cv.samples.findFile(filename))

    # Loads an image
    horizontal, vertical = detect_lines(src, display=True)

    return 0


gray = get_grayscale(org)
bw = get_binary(gray)

horizontal, vertical, last_row, last_column = detect_lines(table_mask, minLinLength=350, display=True, write = False)

counter = 0
## set ROW , COLUMN index
first_line_index = 0
last_row_index = last_row

left_line_index = 0
last_column_index = last_column

keywords = ['TS', 'Number']

dict_burmese = {}
for keyword in keywords:
    dict_burmese[keyword] = []

for i in range(first_line_index, last_row_index):
    for j in range(left_line_index, last_column_index):
        counter += 1

        #progress = counter/((last_line_index-first_line_index)*len(keywords)) * 100
        progress = counter/((last_row_index-first_line_index)*last_column) * 100
        percentage = "%.2f" % progress
        print("Progress: " + percentage + "%")

        left_line_index = j
        print("L: ")
        print(left_line_index)
        right_line_index = j+1
        print("R: " + str(right_line_index))
        top_line_index = i
        bottom_line_index = i+1

        cropped_image, (x,y,w,h) = get_ROI(bw, horizontal, vertical, left_line_index,
                     right_line_index, top_line_index, bottom_line_index)
        '''
        cv.namedWindow('Cropped',cv.WINDOW_NORMAL)
        cv.resizeWindow('Cropped', 600,600)
        cv.imshow("Cropped", cropped_image)
        cv.waitKey(0)
        cv.destroyAllWindows()
        '''
        if(right_line_index == last_column):  # Reset Column detect
            left_line_index = 0;
            print("Reset")

        # OCR Burmese
        text = detect(cropped_image, is_number=False)
        dict_burmese[keyword].append(text)
print(dict_burmese)

print("Success")
