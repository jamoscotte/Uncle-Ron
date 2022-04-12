import os
import shutil
import json
from decipher.beacon import api
import tkinter as tk
from tkinter import filedialog

# AUTHENTICATION
KEY = 'h4uxfqg19dwwr1x1k3escv37ej5b0e2ejmwsum0c6fyy4cgbun4xxnc1zgxsp7vy'
api.login(KEY, 'https://nrg.decipherinc.com')

def get_files():
    #job_number = input("Enter job number: ")
    #path = '/surveys/selfserve/53b/{jobNum}/'.format(jobNum=job_number)

    root = tk.Tk()   # Initializing tk to ask for file select
    root.withdraw()
    file_path = filedialog.askdirectory()

    # Getting and saving datamap file
    #datamap_file = api.get(path + 'datamap?format=fw-text')
    #dat_file = api.get(path + 'data?format=fwu&cond=qualified')
    #spss_file = api.get(path + 'data?format=spss&cond=qualified')


    # with open(file_path + "/datamap.txt", 'wb') as fd:
    #     fd.write(datamap_file)
    #     fd.close()

    #with open(file_path + '/'+ job_number + ".dat", 'wb') as fd:
    #    fd.write(dat_file)
    #    fd.close()

    return file_path




