#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Variable
import re
import nltk
from Netlist import scale_list

rn = re.compile(r'r\d')
cn = re.compile(r'c\d')
un = re.compile(r'_\d')





"""Contains functions for table editing
   delete_table() - returns tables list after deleting unneeded tables
   numeric_tables() - labeling numeric tables as such
"""


def delete_tables(tables) -> list:
    """ delete_tables(tables)
        Reads in tables and deletes unecessary ones
    """
    first_var = input("Enter name of first variable in study: ")
    delete = False
    for table in reversed(tables):
        #print(table.name,first_var, table.name==first_var, delete)
        if table.is_multi:
            if len(table.loop_pair) < 0:
                tables.remove(table)
        if table.name == "noanswer":
            tables.remove(table)
        if not delete:
            if table.name == 'url':
                tables.remove(table)
                delete = True
            elif table.name == first_var:
                delete = True
            elif table.name[0:3] == 'PRG':
                tables.remove(table)
            elif 'termvideo' in table.name:
                tables.remove(table)
            elif 'HidQUOTA' in table.name:
                tables.remove(table)
            elif 'MRK_' in table.name:
                tables.remove(table)
            elif 'Mobile_pipe' in table.name:
                tables.remove(table)
            elif 'BrowserType' in table.name:
                tables.remove(table)
            elif 'selectPlayer' in table.name:
                tables.remove(table)
            elif 'securityLevel' in table.name:
                tables.remove(table)
            elif 'videoSelect' in table.name:
                tables.remove(table)
            elif 'MXD' in table.name:
                tables.remove(table)
            elif 'videot' in table.name:
                tables.remove(table)
            elif 'Error_Counter' in table.name:
                tables.remove(table)
            elif 'SEGMENT_ORDER' in table.name:
                tables.remove(table)
        else:
            if table.name == 'memberid':#'Term_PointTerm101': #'QAGE - Termination Point': #'RESP_TYPE':
                tables.remove(table)
                delete = False
            else:
                tables.remove(table)

    return tables

def numeric_tables(tables) -> list:
    """
    :param self: self
    :param tables: list of table variables
    :return: edited list of tables
    This function labels numerics
    """
    for table in tables:
        if not table.value_pair and not table.is_multi and table.data_col_range:
            table.is_numeric = True
    return tables

def scale_tables(tables) -> list:
    """
    :param self: self
    :param tables: list of table variables
    :return: edited list of table variables
    This function marks tables as scale questions
    """
    for table in tables:
        if table.value_pair:
            if len(table.value_pair) < 4:
                continue
            for scale in scale_list:
                if scale in table.value_pair[0][1]:
                    table.is_scale = True
                    table.t2b = [0, 1]
                    if "Don't know" in table.value_pair[-1][1] or "I've never been a fan of this league" in table.value_pair[-1][1] or "I'm not familiar with any" in table.value_pair[-1][1] or "No opinion" in table.value_pair[-1][1] or "I have never seen or heard of them before" in table.value_pair[-1][1] or "I don't remember this person" in table.value_pair[-1][1] or "I haven't seen enough to rate" in table.value_pair[-1][1] or "Unsure" in table.value_pair[-1][1]:
                        table.move_scale = True
                        table.b2b = [len(table.value_pair)-3,len(table.value_pair)-2]
                    else:
                        table.b2b = [len(table.value_pair)-2,len(table.value_pair)-1]
                    break
                elif scale in table.value_pair[-1][1]:
                    table.is_scale = True
                    table.reverse_scale = True
                    table.b2b = [0, 1]
                    table.t2b = [len(table.value_pair)-2,len(table.value_pair)-1]
                    break
                elif scale in table.value_pair[-2][1]:
                    table.is_scale = True
                    table.reverse_scale = True
                    table.move_scale = True
                    table.b2b = [0, 1]
                    table.t2b = [len(table.value_pair)-3,len(table.value_pair)-2]
                    break
    return tables

def set_base(tables, bases) -> list:
    """
    This function uses list of Those Answering tables and sets base
    :param tables:
    :param bases:
    :return:
    """

    for table in tables:
        for base in bases:
            if table.is_loop and not table.is_multi:
                table.base = "Total"
                for loop in table.loop_pair:
                    if loop[0] == base:
                        table.base = "Those Answering"
                        break
            else:
                if base in table.name:
                    #print(base, table.name)
                    table.base = "Those Answering"
                    break
                table.base = "Total"
    return tables

def set_column(tables,spss_columns) -> list:
    """

    :param tables: list with all table variables
    :param spss_columns: list with pairs of variable names, col location
    :return: updated tables list.
    """

    print("Setting new columns . . .\n")

    for table in tables:
        if table.is_multi:
            loop_index = 0
            for loop in table.loop_pair:
                for spss_var in spss_columns:
                    if table.loop_names[loop_index] == spss_var[0]:
                            loop[1] = spss_var[1]
                            break
                loop_index += 1
        elif table.is_loop or table.split_loop_head:
            loop_index = 0
            for loop in table.loop_pair:
                for spss_var in spss_columns:
                    if table.loop_names[loop_index] == spss_var[0]:
                        if table.data_col_range:
                            loop[1] = spss_var[1]
                            loop[2] = spss_var[2]
                        else:
                            loop[1] = spss_var[1]
                loop_index += 1
        else:
            for spss_var in spss_columns:
                if table.name == spss_var[0]:
                    if table.data_col_range:
                        print(table.name)
                        table.data_col[0] = spss_var[1]
                        table.data_col[1] = spss_var[2]
                    else:
                        table.data_col[0] = spss_var[1]

    return tables

def link_loops(tables) -> list:

    for table in tables:
        if not table.is_loop and (rn.findall(table.name) or cn.findall(table.name) or un.findall(table.name)) and not table.split_loop:
            for table2 in tables:
                if not table2.is_loop and table != table2 and (rn.findall(table2.name) or cn.findall(table2.name) or un.findall(table2.name)) and not table2.split_loop:
                    if nltk.edit_distance(table.name,table2.name) <= 2 and abs(len(table.name) - len(table2.name)) <= 1:
                        #print(table.name,table2.name,nltk.edit_distance(table.name,table2.name))
                        if not table.split_loop_head:
                            if table.data_col_range:
                                table.loop_pair.append([table.name, table.data_col[0], table.data_col[1]])
                            else:
                                table.loop_pair.append([table.name, table.data_col[0]])
                        table.split_loop = True
                        table.split_loop_head = True
                        table2.split_loop = True
                        if table.data_col_range:
                            #print(table.name)
                            table.loop_pair.append([table2.name,table2.data_col[0],table2.data_col[1]])
                        else:
                            table.loop_pair.append([table2.name, table2.data_col[0]])
                        table.table_range.append(table2.table_range[0])
    return tables

