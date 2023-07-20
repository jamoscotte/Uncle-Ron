#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Reads necessary files for table building.
   read_datamap() - Reads in datamap file
   read_SPSS() - Reads in SPSS File
"""

# Packages to open files
import tkinter as tk
from tkinter import filedialog
from Variable import *
import re
import pandas as pd
import pyreadstat




def read_datamap() -> list:
    """ read_datamap(self)
        Reads in datamap file to create variable objects
        returns list of variable objects.
    """
    root = tk.Tk()   # Initializing tk to ask for file select
    root.withdraw()
    file_path = filedialog.askopenfilename()

    # Opening File form filepath and placing lines in lines variable
    file = open(file_path, encoding='utf-8')
    lines = file.read().splitlines()  # Reading Lines from file

    # Parsing through list for variable names
    variable_list = []
    new_var = True
    value_loop = False
    for l in lines:
        l = l.replace("[]","")
        if len(l) < 1:
            new_var = True
            value_loop = False
            continue
        elif new_var:             # Creating Variable, setting name and qtext
            line_split = l.split(":")
            var = Variable()
            if ']' in line_split[0]:

                var.name = line_split[0][1:-1]
            else:
                var.name = line_split[0]

            if len(line_split) > 2:
                var.qtext = line_split[1][1:] + ' ' + line_split[2]
            else:
                var.qtext = line_split[1][1:]
            var.qtext = re.sub("\[.*?\]", '', var.qtext)
            new_var = False
            variable_list.append(var)
        elif l[0] == '(':               # Setting value range
            data_col_split = l[1:-1].split("-")
            if len(data_col_split) > 1:
                var.data_col.append(int(data_col_split[0]))
                var.data_col.append(int(data_col_split[1]))
                var.data_col_range = True
            else:
                var.data_col.append(int(data_col_split[0]))
        elif "Values:" in l:
            value_split = l[8:].rsplit("-",1)
            #print(l,value_split)
            var.value_range.append(int(value_split[0]))
            var.value_range.append(int(value_split[1]))
            value_loop = True
        elif var.name in l:

            var.is_loop = True
            #print(l)
            loop_name_split = re.split("]\t|] ",l[2:],1) #l[2:].split("] ")
            loop_name_split[0] = re.sub("\[.*?\]", '', loop_name_split[0])
            var.loop_names.append(loop_name_split[0])
            #print(loop_name_split)
            loop_pair_split = loop_name_split[1].rsplit("\t(",1)
            if len(loop_pair_split) == 1:
                loop_pair_split = loop_name_split[1].rsplit(" (",1)
                loop_pair_split[0] = re.sub("\[.*?\]", '', loop_pair_split[0])
            #print(loop_pair_split)
            loop_pair_split[0] = re.sub("\[.*?\]", '', loop_pair_split[0])
            if "-" in loop_pair_split[1]:
                loop_pair_range_split = loop_pair_split[1][:-1].split("-")
                #print(loop_pair_range_split)
                var.loop_pair.append([loop_pair_split[0].replace("/","//"),int(loop_pair_range_split[0]),int(loop_pair_range_split[1])])
                var.data_col_range = True
            else:
                var.loop_pair.append([loop_pair_split[0].replace("/","//"),int(loop_pair_split[1][:-1])])
        elif value_loop:
            if "0=Unchecked" in l or "0\tUnchecked" in l:
                var.is_multi = True
                value_loop = False
                continue
            value_pair_split = re.split("=|\t", l[1:]) #l[1:].split("=")
            #(variable_list[-1].name,value_pair_split)
            #print(variable_list[-1].name)
            #print(var.name,value_pair_split)
            value_pair_split[0] = re.sub("\[.*?\]", '', value_pair_split[0])
            var.value_pair.append((int(value_pair_split[0]),value_pair_split[1].replace("/","//")))
            if len(var.value_pair) == var.value_range[-1]:
                if var.value_range[0] == 0:
                    if len(var.value_pair) == var.value_range[-1] + 1:
                        value_loop = False
                else:
                    value_loop = False
    return variable_list

def read_SPSS() -> list:
    """
    This function opens spss and finds total answered for each variable
    :param spss_path:
    :return: list of variables with their base
    """
    # Opening and moving spss into dataframe
    root = tk.Tk()  # Initializing tk to ask for file select
    root.withdraw()
    file_path = filedialog.askopenfilename()

    print("Opening SPSS . . . \n")

    df = pd.read_spss(file_path)
    base = len(df['record'])
    those_asked = []
    delete_tables = []

    print("Checking counts in SPSS . . . \n")

    for (column_name,column_data) in df.iteritems():
        if df[column_name].notnull().sum() < base:
            those_asked.append(column_name)

    print("Checking for empty variables in SPSS . . . \n")


    ################################################################
    for (column_name, column_data) in df.iteritems():
        if len(df[column_name].value_counts()) == 0:
            delete_tables.append(column_name)
    ################################################################

    return those_asked, delete_tables

def read_spssmap() -> list:
    """
    This function takes the datamap from uncle (created by SPSS upload) and stores values for variable names to change

    :return: list of variables with their spss map column location
    """

    eFile = open(r"datamap.txt", encoding='utf-8')  # Opening database file
    eList = eFile.read().splitlines()  # Reading Lines from file

    updated_cols=[]

    for line in eList:
        if '* The Uncle data file' in line:
            return updated_cols
        if len(line)==0:
            continue
        if '* DATAPOS' in line:
            continue
        column_split = line.split()
        column_value = column_split[1].split(':')

        #Determining ranges and single value columns
        if column_value[0] == column_value[1]:
            var_pair = [column_split[2],int(column_value[0])]
        else:
            var_pair = [column_split[2],int(column_value[0]),int(column_value[1])]

        updated_cols.append(var_pair)







