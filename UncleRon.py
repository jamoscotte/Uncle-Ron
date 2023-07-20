# This file is the main driver to create tables for UNCLE

from ReadFiles import *
from TableFunctions import *
from Print_Tables import *
from API import *



# Getting files from Decipher API
path = get_files()

bases, delete_list = read_SPSS()

spss_columns = read_spssmap()


# Opening datamap.txt
tables = read_datamap()

tables = delete_tables(tables)

tables = set_base(tables, bases)

tables = numeric_tables(tables)

tables = scale_tables(tables)

tables = set_column(tables, spss_columns)

print_tables(tables,path)

tables = link_loops(tables)

print_sumgentabs(tables,path)

print_gentabs(tables,path)

print_grids(tables,path)

print_9999(tables,path)

print_datamap(tables)

print_basecheck(tables,path)

print_DE_tables(tables,path)

print_csv(tables,path)

print_text(tables,path)




