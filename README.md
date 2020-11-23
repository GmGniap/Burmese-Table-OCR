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
 - [ ] Fix not to overwrite for appending CSVs

- [x] Always opening BW image for each page
  * I think I can fix with by changing waitkey() & destoryAllWindows functions.
  Solution - change waitkey(0) into waitkey(10) then add destory.

- [ ] Pandas - Removing non-Unicode characters
  - (x) Regex characters
  - (x) Appending rows by rows

- [ ] Accuracy Test
- [ ] Google Vision API
- [ ] Web Version

## Error Notes
- Unicode CSV encoding problem - when I try to export csv into google sheets , the font wasn't correct when using with Gspread 'import_csv' function.
-- Solution -> open("angel.csv", "r").read().encode("utf8")

## :books: Ref
1. [Main Reference Guide](https://fazlurnu.com/2020/06/23/text-extraction-from-a-table-image-using-pytesseract-and-opencv/)
2. [Burmese Tesseract Project](https://github.com/pndaza/tesseract-myanmar)
