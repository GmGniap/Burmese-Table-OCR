import pytesseract

# For Window OS
#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

import cv2 as cv
from ROI_selection import detect_lines, get_ROI
import numpy as np

def get_grayscale(image):
    return cv.cvtColor(image, cv.COLOR_BGR2GRAY)

def get_binary(image):
    (thresh, blackAndWhiteImage) = cv.threshold(image, 100, 255, cv.THRESH_BINARY)
    return blackAndWhiteImage

def invert_area(image, x, y, w, h, display=False):
    ones = np.copy(image)
    ones = 1

    image[ y:y+h , x:x+w ] = ones*255 - image[ y:y+h , x:x+w ]

    if (display):
        cv.imshow("inverted", image)
        cv.waitKey(0)
        cv.destroyAllWindows()
    return image

def detect(cropped_frame, is_eng = False):
    if (is_eng):
        # text = pytesseract.image_to_string(cropped_frame, config ='-c tessedit_char_whitelist=0123456789 --psm 10 --oem 2')
        text = pytesseract.image_to_string(cropped_frame, lang= "eng", config ='--psm 10 --oem 2')
    else:
        text = pytesseract.image_to_string(cropped_frame, lang="mya", config='--psm 10 --oem 1')

    return text

def draw_text(src, x, y, w, h, text):
    cFrame = np.copy(src)
    cv.rectangle(cFrame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    cv.putText(cFrame, "text: " + text, (50, 50), cv.FONT_HERSHEY_SIMPLEX,
               2, (0, 0, 0), 5, cv.LINE_AA)

    return cFrame

def erode(img, kernel_size = 5):
    kernel = np.ones((kernel_size,kernel_size), np.uint8)
    img_erosion = cv.dilate(img, kernel, iterations=2)
    return img_erosion
