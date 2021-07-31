import csv
import tkinter as tk
from tkinter import filedialog
import fitz
file_name = filedialog.askopenfilename()
root = tk.Tk()
root.withdraw()

# file_name = input()
# raw = parser.from_file(file_name)
# content = raw['content'].split('\n\n\n')
# pages = []
# for page in content:
#     if page == '':
#         continue
#     page = page.split('\n\n')
#     if len(page) < 5:
#         continue
#     if len(page) == 31:
#         page = page[:-1]
#     pages.append(page)
#
pages = []
with fitz.open(file_name) as doc:
    for page in doc:
        text = page.getText()
        pages.append(page.getText())
addresses = []
for page in pages:
    page = page.split('\n')
    address = []
    for raw in page:
        raw = raw.replace('\ufffd', '')
        try:
            bin_or_not = raw.split()[-1]
            n = len(bin_or_not)
        except IndexError as ie:
            bin_or_not = ''
            n = 0
        if '-' in raw or (bin_or_not.isdecimal() and n >= 4):
            address.append(raw)
            addresses.append(address)
            address = []
        else:
            address.append(raw)
output = []
for address in addresses:
    try:
        bin = address[-1].split()[-1]
        state = address[-1].split()[-2]
        city = address[-1].split()[0].replace(',', '')
        creating = []
        for i in range(len(address) - 1):
            creating.append(address[i])
        while len(creating) < 7:
            creating.append('')
        creating.append(city)
        creating.append(state)
        creating.append(bin)
        if creating != []:
            output.append(creating)
    except IndexError as IE:
        continue
with open(file_name.replace('.pdf', '.csv'), 'w', newline='') as file:
    writer = csv.writer(file, delimiter=";")
    writer.writerow('sep=;')
    writer.writerows(output)
