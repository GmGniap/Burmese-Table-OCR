# Burmese-Table-OCR
:computer:
Extract text from tables of images. Use OpenCV to detect margin lines and PyTesseract to detect Burmese text.
:keyboard:


## :label: To-Do List
- [x] Upload to Github
- [x] Folder Input
  * folder_input.py - current output as CSV append , so need to delete or find a way to overwrite to apply new folder. Then another possible work is directly upload into Google Sheets.
  * In output csv , there's uncessary characters(like \\n symbol), need to find a way to remove these.(possible with pandas then overwrite)

- [x] Link with Google APIs
 - [x] Google Sheets [Helping Guide](https://www.youtube.com/watch?v=T1vqS1NL89E)
 - [x] Fix not to overwrite for appending CSVs

- [x] Always opening BW image for each page
  * I think I can fix with by changing waitkey() & destoryAllWindows functions.
  Solution - change waitkey(0) into waitkey(10) then add destory.

- [x] Correct Horizontal , Vertical & Intersection of table
  * FindContour?
  * Adjusting parameters
- [ ] Pandas - Removing non-Unicode characters
  -  Regex characters
  -  Appending rows by rows
  - Even or Odd numbers of Array
    1. 1D Array into Pandas.Dataframe series
    2. Combine multiple sereis as one Dataframe

- [ ] Accuracy Test
- [ ] Google Vision API
- [ ] Web Version

## Error Notes :fire: :sweat_drops:
- Unicode CSV encoding problem - when I try to export csv into google sheets , the font wasn't correct when using with Gspread 'import_csv' function.
  * Solution -> open("angel.csv", "r").read().encode("utf8")

- Nov 27,2020
  - A lot of errors also today. I didn't note down everything but the solved tasks that I remember is
    * Adjusting threshold & minLinLength values to detect the table correctly (it's the most important thing)
    * Append the dictionary according to filenames
    * Generate CSV - row by row
  - Overall result is satisfied.
  - My code is full of comments & editions. Noone won't be able to understand at the first look.:satisfied:
    * I need to write a blog about this project and also record a explanation video. 

## :books: Ref
1. [Main Reference Guide](https://fazlurnu.com/2020/06/23/text-extraction-from-a-table-image-using-pytesseract-and-opencv/)
2. [Burmese Tesseract Project](https://github.com/pndaza/tesseract-myanmar)
