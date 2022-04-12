# This File is the main driver for creating Uncle Banners

from ReadFiles import *
import re
import openpyxl
import pandas as pd
from BannerFunctions import *

# tkinter initialization
root = tk.Tk()
root.withdraw()

# Creating Database from mdd
variables = read_datamap()

# Requesting file path from user
file_path = filedialog.askopenfilename()

# Moving excel file to dataframe
ban_setup = pd.read_excel(file_path, sheet_name=None)

# Setting up Excel Writer
dirname = filedialog.askdirectory()
banname = input("Please enter desired file name: ")
path = dirname + '/' + banname + '.txt'

for sheet in ban_setup:
    ban = ban_setup[sheet]
    with open(path, "w", encoding="utf-8") as f:
        write_col_headers(ban, f, 1)
        write_RO_lines(f)
        write_C_lines(ban,variables,f)