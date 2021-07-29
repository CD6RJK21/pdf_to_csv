from tika import parser
import csv
from PyQt6.QtGui import QFileOpenEvent
import tkinter as tk
from tkinter import filedialog
file_name = filedialog.askopenfilename()
root = tk.Tk()
root.withdraw()

# file_name = input()
raw = parser.from_file(file_name)
content = raw['content'].split('\n\n\n')
pages = []
for page in content:
    if page == '':
        continue
    page = page.split('\n\n')
    if len(page) < 5:
        continue
    if len(page) == 31:
        page = page[:-1]
    pages.append(page)
output = []
for page in pages:
    for address in page:
        try:
            address = address.split('\n')
            bin = address[-1].split()[-1]
            state = address[-1].split()[-2]
            city = address[-1].split()[0].replace(',', '')
        except IndexError as IE:
            continue
        creating = []
        for i in range(len(address) - 1):
            creating.append(address[i])
        while len(creating) < 7:
            creating.append('')
        creating.append(city)
        creating.append(state)
        creating.append(bin)
        output.append(creating)
with open(file_name.replace('.pdf', '.csv'), 'w') as file:
    writer = csv.writer(file, delimiter=";")
    writer.writerow('sep=;')
    writer.writerows(output)
