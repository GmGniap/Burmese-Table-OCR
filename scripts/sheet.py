import gspread_dataframe as gd
import gspread as gs
import csv
import pandas as pd

gc = gs.service_account(filename='creds.json')

def export_to_sheets(df, mode='r'):
    sh = gc.open_by_key('1tp2mkT_keY6joUulQIyDDoL3Yr_f6x5--DqoJqtk9WQ').worksheet('main')
    if(mode == 'w'):
        sh.clear()
        gd.set_with_dataframe(worksheet=sh, dataframe=df, include_index=False,include_column_header=True,resize=True)
        return True
    elif(mode == 'a'):
        print("Append Mode")
        sh.add_rows(df.shape[0])
        gd.set_with_dataframe(worksheet=sh, dataframe=df, include_index=False, include_column_header=False, row=sh.row_count+1, resize=False)
        return True
    else:
        return gd.get_as_dataframe(worksheet=sh)

'''
path =  './symo.csv'

data = pd.read_csv(path, encoding='utf-8')
print(data.head(8))
#df.to_csv('out.csv', index=False)
'''
'''
# Reading Burmese word csv file as 'UTF-8'
test = open("symo.csv", "r").read().encode("utf8")
gc.import_csv('1tp2mkT_keY6joUulQIyDDoL3Yr_f6x5--DqoJqtk9WQ', data=test)
'''

#worksheet = sh.sheet1
#res = worksheet.get_all_records()
#print(res)

'''
with open('day.csv', 'r') as file_obj:
    #reader = csv.reader(file_obj)
    content = file_obj.read()
    gc.import_csv('1tp2mkT_keY6joUulQIyDDoL3Yr_f6x5--DqoJqtk9WQ', data=content)

#path =  '/Users/johndoe/file.csv'

with open('output.csv', 'r', encoding='utf-8', errors='ignore') as infile, open('final.csv', 'w') as outfile:

    def unicode_csv(infile, outfile):
        inputs = csv.reader(utf_8_encoder(infile))
        output = csv.writer(outfile)

        for index, row in enumerate(inputs):
            yield [unicode(cell, 'utf-8') for cell in row]
            if index == 0:
                 continue
        output.writerow(row)

    def utf_8_encoder(infile):
        for line in infile:
            yield line.encode('utf-8')

unicode_csv(infile, outfile)
'''
