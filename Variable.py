#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Class File: Variable
    Variable object that holds all table info
"""
class Variable:
    def __init__(self):
        self.name =""                   # Core name of variable
        self.qtext = ""                 # Question text of variable
        self.data_col = []              # column value if variable is a single variable
        self.loop_names = []            # Unsure and possibly unused
        self.value_range = []           # Range of values for responses
        self.value_pair = []            # Names and data columns for responses ([range, response text])
        self.is_loop = False            # Flag for loops
        self.loop_pair = []             # (Loop name, loop column, loop column 2 (if needed))
        self.is_multi = False           # Flag for multi punch
        self.is_numeric = False         # Flag for numeric
        self.is_scale = False           # Flag for recognized scale question
        self.reverse_scale = False      # Flag for scale question where positive is reversed (5-positive, 1-negative)
        self.move_scale = False         # Flag for if scale has been moved
        self.base = ""                  # Base text
        self.data_col_range = False     # Flag for a ranged data column
        self.table_range = []           # Range for table numbers
        self.sum_table_numbers = []     # Link to numbers for sum tables
        self.t2b = ''                   # Top 2 Box range
        self.b2b = ''                   # Bottom 2 Box range
        self.split_loop = False
        self.split_loop_head = False
        self.multi_loop = []                # table name,table grid





