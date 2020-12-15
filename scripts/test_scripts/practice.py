from pathlib import Path
data_folder = Path("scripts/")
file_to_open = "reading.txt"

file = open(file_to_open, 'r')
inp = file.read()
for line in file:
    if line.startswith('From:'):
        print(line)
