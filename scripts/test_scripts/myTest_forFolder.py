import cv2
import argparse
import os

ext = ( 'jpg', 'jpeg', 'png', 'tif', 'tiff')
def convert_folder(folder_path):
    for img_file in os.listdir(folder_path):
        if img_file.endswith(ext):
            img_basename = os.path.splitext(img_file)[0]
            print('\n')
            print('#################################')
            print('### processing:', img_file )
            print('#################################')
            print('\n')

            image = cv2.imread(os.path.join(folder_path,img_file))
            #image = cv2.imread('test.jpg')

            result = image.copy()
            gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

            # Remove horizontal lines
            horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40,1))
            remove_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
            cnts = cv2.findContours(remove_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            #print(cnts[1])
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]

            for c in cnts:
                # print([c])
                cv2.drawContours(result, [c], -1, (255,255,255), 5)

            #cv2.imshow('result', result)

            # Remove vertical lines
            vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (0.5,40))
            remove_vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
            cnts = cv2.findContours(remove_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]
            for c in cnts:
                cv2.drawContours(result, [c], -1, (255,255,255), 5)

            #cv2.imshow('thresh', thresh)
            cv2.imshow('result', result)

            #cv2.imwrite('result.png', result)
            cv2.imwrite("./Pyithu/"+ str(img_basename) + ".png", result);
            cv2.waitKey(20)

if __name__ == "__main__":

    ap = argparse.ArgumentParser(description='Remove lines from images as folder input')
    ap.add_argument("-i", "--input", type=str, help='input image folder')
    #ap.add_argument("-m", "--mode", type=int, nargs='?', const=0, default=0, help=' 0: OCR. 1: only save bounded image 2: OCR + save bounded image. ')
    args = ap.parse_args()
    if(args.input == None):
        print('usage: python folder_input.py --input path_to_image_folder')

    else:
        convert_folder(args.input)
