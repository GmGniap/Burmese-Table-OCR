# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 10:21:08 2020

@author: Fazlur Rahman
"""

from preprocessing import get_grayscale, get_binary, invert_area, draw_text, detect
from ROI_selection import detect_lines, get_ROI
import cv2 as cv

# Save Dictionary file as CSV
import csv

def main(display = False, print_text = False, write = False):
    # filename = '../images/source7.png'

    filename = '../test/1.png' #testing file by Pi

    # src = cv.imread(cv.samples.findFile(filename))
    src = cv.imread(filename)


    horizontal, vertical = detect_lines(src, minLinLength=350, display=True, write = True)
    print("Horizon:")
    print(horizontal)
    print("\n")
    print("verti:")
    print(vertical)

    '''
    ## invert area
    left_line_index = -1 #17
    right_line_index = 0 #20
    top_line_index = 0
    bottom_line_index = -1

    cropped_image, (x, y, w, h) = get_ROI(src, horizontal, vertical, left_line_index,
                         right_line_index, top_line_index, bottom_line_index)
                         '''
    gray = get_grayscale(src)
    bw = get_binary(gray)
    cv.imshow("bw", bw)
    cv.imwrite("bw.png", bw)

    #bw = invert_area(bw, x, y, w, h, display=True)
    #cv.imshow("Inverted", bw)
    #cv.imwrite("bw_inver.png", bw)

    #bw = erode(bw, kernel_size=2)

    cv.waitKey(0)


    ## set keywords
    '''
    keywords = ['no', 'kabupaten', 'kb_otg', 'kl_otg', 'sm_otg', 'ks_otg', 'not_cvd_otg',
            'kb_odp', 'kl_odp', 'sm_odp', 'ks_odp', 'not_cvd_odp',
            'kb_pdp', 'kl_pdp', 'sm_pdp', 'ks_pdp', 'not_cvd_pdp',
            'positif', 'sembuh', 'meninggal']
    '''
    # keywords = ['no1', 'no2', 'no3' , 'no4', 'no5', 'no6',  'no7', 'no8', 'no9']

    keywords = ['TS', 'Number']

    dict_burmese = {}
    for keyword in keywords:
        dict_burmese[keyword] = []

    ## set counter for image indexing
    counter = 0

    ## set line indexarray (interested row 2-14)
    first_line_index = 1
    last_line_index = 23

    ## read text
    print("Start detecting text...")
    for i in range(first_line_index, last_line_index):
        for j, keyword in enumerate(keywords):
            counter += 1

            progress = counter/((last_line_index-first_line_index)*len(keywords)) * 100
            percentage = "%.2f" % progress
            print("Progress: " + percentage + "%")

            left_line_index = j
            right_line_index = j+1
            top_line_index = i
            bottom_line_index = i+1

            cropped_image, (x,y,w,h) = get_ROI(bw, horizontal, vertical, left_line_index,
                         right_line_index, top_line_index, bottom_line_index)

            if (keywords[j]=='kabupaten'):
                text = detect(cropped_image)
                dict_burmese[keyword].append(text)

                if (print_text):
                    print("Not number" + ", Row: ", str(i), ", Keyword: " + keyword + ", Text: ", text)
            else:
                text = detect(cropped_image, is_number=False)
                dict_burmese[keyword].append(text)

                if (print_text):
                    print("Is number" + ", Row: ", str(i), ", Keyword: " + keyword + ", Text: ", text)

            if (display or write):
                    image_with_text = draw_text(src, x, y, w, h, text)

            if (display):
                cv.imshow("detect", image_with_text)
                cv.waitKey(0)
                cv.destroyAllWindows()

            if (write):
                cv.imwrite("../Images/"+ str(counter) + ".png", image_with_text);

    with open('output.csv', 'w') as output:
        writer = csv.writer(output)
        for key, value in dict_burmese.items():
            writer.writerow([key, value])

    print(dict_burmese)
    return 0

    '''
        # import json (need to add above)
        with open('test.txt', 'w') as file:
            file.write(json.dumps(dict_burmese))
    '''


if __name__ == "__main__":
    main()
