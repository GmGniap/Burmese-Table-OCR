# -*- coding: utf-8 -*-

import cv2 as cv
import argparse
import os
import csv
import pandas as pd

#import img_utils
#import line_segment

from sheet import export_to_sheets
from preprocessing import get_grayscale, get_binary, invert_area, draw_text, detect
from ROI_selection import detect_lines, get_ROI
#from ROI_stack import detect_lines, get_ROI

RESIZED_HEIGHT = 2500

def do_OCR(folder_path,display = False, print_text = False, write = False):

    ext = ( 'jpg', 'jpeg', 'png', 'tif', 'tiff')
    keywords = os.listdir(folder_path)
    print(keywords)

    dict_burmese = {}
    for keyword in keywords:
        dict_burmese[keyword] = []

    for img_file in os.listdir(folder_path):
        if img_file.endswith(ext):
            img_basename = os.path.splitext(img_file)[0]
            print('\n')
            print('#################################')
            print('### processing:', img_file )
            print('#################################')
            print('\n')

            src = cv.imread(os.path.join(folder_path,img_file))  #(..,0) - Flag removed while edit

            #print(src.shape)

            ## we need to tune Threshold & minLinLength values to adjust font size & column height of related image
            horizontal, vertical, last_row, last_column = detect_lines(src, threshold = 150, minLinLength=150, display=True, write = False)

            print("Last Row: ")
            print(last_row)
            '''
            print("Horizon:")
            print(horizontal)
            print("\n")
            print("verti:")
            print(vertical)
            '''

            gray = get_grayscale(src)
            bw = get_binary(gray)
            cv.imshow("bw", bw)
            #cv.imwrite("bw.png", bw)
            cv.waitKey(10)
            cv.destroyAllWindows()

            keyword = img_file
            print(keyword)

            text_array = []
            ## set counter for image indexing
            counter = 0

            ## set line indexarray (interested row 0 to last_row)
            first_line_index = 0
            last_line_index = last_row

            ## set column index
            left_line_index = 0
            last_column_index = last_column

            ## read text
            print("Start detecting text...")
            for i in range(first_line_index, last_line_index):
                #for j, keyword in enumerate(keywords):
                for j in range(left_line_index, last_column_index):
                    counter += 1

                    #progress = counter/((last_line_index-first_line_index)*len(keywords)) * 100
                    progress = counter/((last_line_index-first_line_index)*last_column) * 100
                    percentage = "%.2f" % progress
                    print("Progress: " + percentage + "%")

                    left_line_index = j
                    #print("L: ")
                    #print(left_line_index)
                    right_line_index = j+1
                    #print(right_line_index)
                    top_line_index = i
                    bottom_line_index = i+1

                    cropped_image, (x,y,w,h) = get_ROI(src, horizontal, vertical, left_line_index,
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
                    text = detect(cropped_image, is_eng=False)
                    dict_burmese[keyword].append(text)

                    if (display or write):
                            image_with_text = draw_text(src, x, y, w, h, text)

                    if (display):
                        cv.imshow("detect", image_with_text)
                        cv.waitKey(0)
                        cv.destroyAllWindows()

                    if (write):
                        cv.imwrite("../Images/"+ str(counter) + ".png", image_with_text);
            '''
            print(text_array)
            ts = []
            no = []
            for i in range(0,len(text_array)):
                if i % 2:
                    no.append(text_array[i])
                else:
                    ts.append(text_array[i])
            print(len(ts))
            print(len(no))

            township = pd.Series(ts)
            number = pd.Series(no)
            data = {
            "Township": township,
            "Number" : number
            }
            df = pd.concat(data, axis =1)
            df.to_csv('../all/test.csv',index = False, header= True)
            #print(df)

            print("Success")
            '''
    data = dict_burmese
    #print(data)
    df = pd.DataFrame.from_dict(data, orient='index')
    #df = pd.DataFrame.from_dict(data)
    e_df = df.transpose()
    e_df.to_csv('../all/State/state_vote.csv',index=False)
    print("success")
    #export_to_sheets(df, 'w')
    '''
    export_to_sheets(e_df, 'w')
    print("Success")

    with open('../all/symo.csv', 'w', encoding='utf-8') as output:
        writer = csv.writer(output)
        for key, value in dict_burmese.items():
            writer.writerow([key, value])

            img = img_utils.resize(img, height=RESIZED_HEIGHT)
            img = img_utils.clean(img)
            height, width = img.shape
            # invert = img_utils.invert(img)
            lines = line_segment.get_lines(img)
            print('founded lines: ', len(lines))
            # max_width will be use as paragraph analyzer
            longest_line = (sorted(lines, key=lambda line: line[2]))[-1]
            max_x = longest_line[0] + longest_line[2]
            avg_height = (int) (sum([line[3] for line in lines]) / len(lines))

            if mode != 1:
                print('Processing OCR ... ')
                texts = ''
                paragraph_decider = 50
                for i, rect in enumerate(lines):
                    x = rect[0] + rect[2]
                    text_line = ocr.get_text(rect, img, avg_height)
                    if text_line:
                        texts += text_line.strip()
                        if   x + paragraph_decider < max_x:
                            texts += '\n'

                # save ocr text to file
                textfile = os.path.join(folder_path, img_basename + '.txt' )
                print('saved to: ', textfile)
                with open(textfile, 'w', encoding='utf-8') as out:
                    out.write(texts + '\n\n')


            if mode == 1 or mode == 2:
                print('saving bounded box image...')
                path = os.path.join( folder_path, 'debug')
                if not os.path.exists(path):
                    os.makedirs(path)
                debug_file = os.path.join(path, img_file)
                debug_img = img_utils.get_bounded_box_image(img, lines)
                cv2.imwrite(debug_ Columnfile, debug_img)
                '''

if __name__ == "__main__":

    ap = argparse.ArgumentParser(description='textline segmentation and do ocr on these lines')
    ap.add_argument("-i", "--input", type=str, help='input image folder')
    #ap.add_argument("-m", "--mode", type=int, nargs='?', const=0, default=0, help=' 0: OCR. 1: only save bounded image 2: OCR + save bounded image. ')
    args = ap.parse_args()
    if(args.input == None):
        print('usage: python folder_input.py --input path_to_image_folder')

    else:
        do_OCR(args.input)
