#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Contains functions to print tables regular,sums, and gentabs
   print_tables(tables) - Prints normal tables from Input tables list
   print_gentabs(tables) - Prints Gentabs and Numeric Sums
"""

from Netlist import *


def print_tables(tables,path):
    """
    :param tables: list of variables
    :return: none
    This function prints normal tables
    """
    table_number = 1
    with open(path + "/tables.txt", "w", encoding="utf-8") as f:
        for table in tables:
            if (table.is_loop or table.split_loop_head) and not table.is_multi:
                loop_pair_index = 0
                for loop in table.loop_pair:
                    # Writing T lines
                    f.write('Table ' + str(table_number) + '\n')
                    f.write('T ' + table.name + "_" + str(loop_pair_index + 1) + '\n')
                    f.write('T ' + table.loop_pair[loop_pair_index][0] + '\n')
                    f.write('T ' + table.qtext.replace("/","//") + '\n')
                    f.write('T Respondents: {base}\n'.format(base=table.base))

                    # Writing Q lines
                    if table.data_col_range:
                        f.write('Q {range1}:{range2}n$ \n'.format(range1=str(loop[1]), range2=str(loop[2])))
                    else:
                        f.write('Q {range1}n$ \n'.format(range1=str(loop[1])))

                    # Writing O lines
                    #print(table.name)
                    if table.is_numeric:
                        f.write('O span {col1}:{col2} \n'.format(col1=str(loop[1]), col2=str(loop[2])))
                        f.write('R Mean ; A({col1}:{col2}) ; freq fdp 1\n'.format(col1=str(loop[1]), col2=str(loop[2])))
                        f.write('R Median ; PC({col1}:{col2},50) ; freq fdp 0\n'.format(col1=str(loop[1]),
                                                                                        col2=str(loop[2])))
                        f.write("*\n")
                        loop_pair_index += 1
                        table.table_range.append(table_number)
                        table_number += 1

                        continue

                    # Writing R Lines
                    if table.reverse_scale:
                        if table.move_scale:
                            for value in reversed(table.value_pair):
                                if table.data_col_range:
                                    f.write('R {rowtext} ; R({col1}:{col2},{punch})'.format(rowtext=value[1],
                                                                                            col1=str(loop[1]),
                                                                                            col2=str(loop[2]),
                                                                                            punch=value[0]))
                                else:
                                    f.write('R {rowtext} ; {col}-{punch}'.format(rowtext=value[1], col=str(loop[1]),
                                                                                 punch=str(value[0])))
                                if 'No Response' in value[1]:
                                    f.write(' ; szr nor')
                                else:
                                    for n in nor:
                                        if n in value[1]:
                                            f.write(' ; nor')
                                f.write('\n')
                            if table.data_col_range:
                                f.write('R {rowtext} ; R({col1}:{col2},{punch})'.format(rowtext=table.value_pair[-1][1],
                                                                                        col1=str(loop[1]),
                                                                                        col2=str(loop[2]),
                                                                                        punch=str(
                                                                                            table.value_pair[-1][0])))
                            else:
                                f.write('R {rowtext} ; {col}-{punch}'.format(rowtext=table.value_pair[-1][1],
                                                                             col=str(loop[1]),
                                                                             punch=str(table.value_pair[-1][0])))
                            f.write('\n')
                        else:
                            for value in reversed(table.value_pair):
                                if table.data_col_range:
                                    f.write('R {rowtext} ; R({col1}:{col2},{punch})'.format(rowtext=value[1],
                                                                                            col1=str(loop[1]),
                                                                                            col2=str(loop[2]),
                                                                                            punch=value[0]))
                                else:
                                    f.write('R {rowtext} ; {col}-{punch}'.format(rowtext=value[1], col=str(loop[1]),
                                                                                 punch=str(value[0])))
                                if 'No Response' in value[1]:
                                    f.write(' ; szr nor')
                                else:
                                    for n in nor:
                                        if n in value[1]:
                                            f.write(' ; nor')
                                f.write('\n')
                    else:
                        if table.value_pair:
                            for value in table.value_pair:
                                if table.data_col_range:
                                    f.write(
                                        'R {rowtext} ; R({col1}:{col2},{punch})'.format(rowtext=value[1], col1=str(loop[1]),
                                                                                        col2=str(loop[2]), punch=value[0]))
                                else:
                                    f.write('R {rowtext} ; {col}-{punch}'.format(rowtext=value[1], col=str(loop[1]),
                                                                                 punch=str(value[0])))
                                if 'No Response' in value[1]:
                                    f.write(' ; szr nor')
                                else:
                                    for n in nor:
                                        if n in value[1]:
                                            f.write(' ; nor')
                                f.write('\n')
                        else:
                            first_value = int(table.value_range[0])
                            last_value = int(table.value_range[-1])
                            for value in range(last_value):
                                table.value_pair.append([value+1,str(value+1)])
                                if table.data_col_range:
                                    f.write(
                                        'R {rowtext} ; R({col1}:{col2},{punch})'.format(rowtext=str(value+1), col1=str(loop[1]),
                                                                                        col2=str(loop[2]), punch=str(value+1)))
                                else:
                                    f.write('R {rowtext} ; {col}-{punch}'.format(rowtext=str(value+1), col=str(loop[1]),
                                                                                 punch=str(value+1)))
                                f.write('\n')



                    # Writing Nets
                    if table.is_scale:
                        if table.reverse_scale:
                            if table.move_scale:
                                if table.data_col_range:
                                    f.write(
                                        "R Top 2 Box ({label1}//{label2}) ; R({col}:{col2},{punch1},{punch2})\n".format(
                                            label1=table.value_pair[-3][1], label2=table.value_pair[-2][1],
                                            col1=str(loop[1]), col2=str(loop[2]), punch1=str(table.value_pair[-3][0]),
                                            punch2=str(table.value_pair[-2][0])))
                                    f.write("R Bottom 2 Box ({label1}//{label2}) ; R({col1}:{col2},1,2)\n".format(
                                        label1=table.value_pair[0][1], label2=table.value_pair[1][1], col1=str(loop[1]),
                                        col2=str(loop[2])))
                                else:
                                    f.write("R Top 2 Box ({label1}//{label2}) ; {col}-{punch1},{punch2}\n".format(
                                        label1=table.value_pair[-3][1], label2=table.value_pair[-2][1],
                                        col=str(loop[1]), punch1=str(table.value_pair[-3][0]),
                                        punch2=str(table.value_pair[-2][0])))
                                    f.write("R Bottom 2 Box ({label1}//{label2}) ; {col}-1,2\n".format(
                                        label1=table.value_pair[0][1], label2=table.value_pair[1][1], col=str(loop[1])))
                            else:
                                if table.data_col_range:
                                    f.write(
                                        "R Top 2 Box ({label1}//{label2}) ; R({col1}:{col2},{punch1},{punch2})\n".format(
                                            label1=table.value_pair[-2][1], label2=table.value_pair[-1][1],
                                            col1=str(loop[1]), col2=str(loop[2]), punch1=str(table.value_pair[-2][0]),
                                            punch2=str(table.value_pair[-1][0])))
                                    f.write("R Bottom 2 Box ({label1}//{label2}) ; R({col1}:{col2},1,2)\n".format(
                                        label1=table.value_pair[0][1], label2=table.value_pair[1][1], col1=str(loop[1]),
                                        col2=str(loop[2])))
                                else:
                                    f.write("R Top 2 Box ({label1}//{label2}) ; {col}-{punch1},{punch2}\n".format(
                                        label1=table.value_pair[-2][1], label2=table.value_pair[-1][1],
                                        col=str(loop[1]), punch1=str(table.value_pair[-2][0]),
                                        punch2=str(table.value_pair[-1][0])))
                                    f.write("R Bottom 2 Box ({label1}//{label2}) ; {col}-1,2\n".format(
                                        label1=table.value_pair[0][1], label2=table.value_pair[1][1], col=str(loop[1])))
                        else:
                            if table.move_scale:
                                if table.data_col_range:
                                    f.write("R Top 2 Box ({label1}//{label2}) ; R({col1}:{col2},1,2)\n".format(
                                        label1=table.value_pair[0][1], label2=table.value_pair[1][1], col1=str(loop[1]),
                                        col2=str(loop[2])))
                                    f.write(
                                        "R Bottom 2 Box ({label1}//{label2}) ; R({col}:{col2},{punch1},{punch2})\n".format(
                                            label1=table.value_pair[-3][1], label2=table.value_pair[-2][1],
                                            col1=str(loop[1]), col2=str(loop[2]), punch1=str(table.value_pair[-3][0]),
                                            punch2=str(table.value_pair[-2][0])))
                                else:
                                    f.write("R Top 2 Box ({label1}//{label2}) ; {col}-1,2\n".format(
                                        label1=table.value_pair[0][1], label2=table.value_pair[1][1], col=str(loop[1])))
                                    f.write("R Bottom 2 Box ({label1}//{label2}) ; {col}-{punch1},{punch2}\n".format(
                                        label1=table.value_pair[-3][1], label2=table.value_pair[-2][1],
                                        col=str(loop[1]), punch1=str(table.value_pair[-3][0]),
                                        punch2=str(table.value_pair[-2][0])))
                            else:
                                if table.data_col_range:
                                    f.write("R Top 2 Box ({label1}//{label2}) ; R({col1}:{col2},1,2)\n".format(
                                        label1=table.value_pair[0][1], label2=table.value_pair[1][1], col1=str(loop[1]),
                                        col2=str(loop[2])))
                                    f.write(
                                        "R Bottom 2 Box ({label1}//{label2}) ; R({col1}:{col2},{punch1},{punch2})\n".format(
                                            label1=table.value_pair[-2][1], label2=table.value_pair[-1][1],
                                            col1=str(loop[1]), col2=str(loop[2]), punch1=str(table.value_pair[-2][0]),
                                            punch2=str(table.value_pair[-1][0])))
                                else:
                                    f.write("R Top 2 Box ({label1}//{label2}) ; {col}-1,2\n".format(
                                        label1=table.value_pair[0][1], label2=table.value_pair[1][1], col=str(loop[1])))
                                    f.write("R Bottom 2 Box ({label1}//{label2}) ; {col}-{punch1},{punch2}\n".format(
                                        label1=table.value_pair[-2][1], label2=table.value_pair[-1][1],
                                        col=str(loop[1]), punch1=str(table.value_pair[-2][0]),
                                        punch2=str(table.value_pair[-1][0])))
                    f.write("*\n")
                    loop_pair_index += 1
                    table.table_range.append(table_number)
                    table_number += 1
            elif table.is_numeric:
                # Writing T lines
                f.write('Table ' + str(table_number) + '\n')
                f.write('T ' + table.name + '\n')
                f.write('T ' + table.qtext.replace("/","//") + '\n')
                f.write('T Respondents: {base}\n'.format(base=table.base))

                # Writing Q lines
                if table.data_col_range:
                    f.write(
                        'Q {range1}:{range2}n$ \n'.format(range1=str(table.data_col[0]), range2=str(table.data_col[1])))
                else:
                    #print(table.name)
                    f.write('Q {range1}n$ \n'.format(range1=str(table.data_col[0])))

                # Writing O lines
                f.write('O span {col1}:{col2} \n'.format(col1=str(table.data_col[0]), col2=str(table.data_col[1])))
                f.write('R Mean ; A({col1}:{col2}) ; freq fdp 1\n'.format(col1=str(table.data_col[0]),
                                                                          col2=str(table.data_col[1])))
                f.write(
                    'R Median ; PC({col1}:{col2},50) ; freq fdp 0\n'.format(col1=str(table.data_col[0]),
                                                                            col2=str(table.data_col[1])))
                f.write("*\n")
                table.table_range.append(table_number)
                table_number += 1
            elif table.is_multi:
                # Writing T lines
                f.write('Table ' + str(table_number) + '\n')
                f.write('T ' + table.name + '\n')
                f.write('T ' + table.qtext.replace("/","//") + '\n')
                f.write('T Respondents: {base}\n'.format(base=table.base))

                # Writing Q lines
                print(table.name,table.loop_pair)
                f.write('Q {range1}:{range2}n$ \n'.format(range1=str(table.loop_pair[0][1]),
                                                          range2=str(table.loop_pair[-1][1])))

                for loop in table.loop_pair:
                    f.write('R {rowtext} ; {col}-1\n'.format(rowtext=loop[0], col=loop[1]))

                f.write("*\n")
                table.table_range.append(table_number)
                table_number += 1

            else:
                f.write('Table ' + str(table_number) + '\n')
                f.write('T ' + table.name + '\n')
                f.write('T ' + table.qtext.replace("/","//") + '\n')
                f.write('T Respondents: {base}\n'.format(base=table.base))

                if table.data_col_range:
                    f.write(
                        'Q {range1}:{range2}n$ \n'.format(range1=str(table.data_col[0]), range2=str(table.data_col[1])))
                else:
                    #print(table.name)
                    f.write('Q {range1}n$ \n'.format(range1=str(table.data_col[0])))

                # Writing R Lines
                if table.reverse_scale:
                    if table.move_scale:
                        for value in reversed(table.value_pair[:-1]):
                            if table.data_col_range:
                                f.write('R {rowtext} ; R({col1}:{col2},{punch})'.format(rowtext=value[1],
                                                                                        col1=str(table.data_col[0]),
                                                                                        col2=str(table.data_col[1]),
                                                                                        punch=value[0]))
                            else:
                                f.write(
                                    'R {rowtext} ; {col}-{punch}'.format(rowtext=value[1], col=str(table.data_col[0]),
                                                                         punch=str(value[0])))
                            if 'No Response' in value[1]:
                                f.write(' ; szr nor')
                            else:
                                for n in nor:
                                    if n in value[1]:
                                        f.write(' ; nor')
                            f.write('\n')
                        if table.data_col_range:
                            f.write('R {rowtext} ; R({col1}:{col2},{punch})'.format(rowtext=table.value_pair[-1][1],
                                                                                    col1=str(table.data_col[0]),
                                                                                    col2=str(table.data_col[1]),
                                                                                    punch=str(table.value_pair[-1][0])))
                        else:
                            f.write(
                                'R {rowtext} ; {col}-{punch}'.format(rowtext=table.value_pair[-1][1],
                                                                     col=str(table.data_col[0]),
                                                                     punch=str(table.value_pair[-1][0])))
                        f.write('\n')
                    else:
                        for value in reversed(table.value_pair):
                            if table.data_col_range:
                                f.write('R {rowtext} ; R({col1}:{col2},{punch})'.format(rowtext=value[1],
                                                                                        col1=str(table.data_col[0]),
                                                                                        col2=str(table.data_col[1]),
                                                                                        punch=value[0]))
                            else:
                                f.write(
                                    'R {rowtext} ; {col}-{punch}'.format(rowtext=value[1], col=str(table.data_col[0]),
                                                                         punch=str(value[0])))
                            if 'No Response' in value[1]:
                                f.write(' ; szr nor')
                            else:
                                for n in nor:
                                    if n in value[1]:
                                        f.write(' ; nor')
                            f.write('\n')
                else:
                    for value in table.value_pair:
                        if table.data_col_range:
                            f.write('R {rowtext} ; R({col1}:{col2},{punch})'.format(rowtext=value[1],
                                                                                    col1=str(table.data_col[0]),
                                                                                    col2=str(table.data_col[1]),
                                                                                    punch=value[0]))
                        else:
                            f.write('R {rowtext} ; {col}-{punch}'.format(rowtext=value[1], col=str(table.data_col[0]),
                                                                         punch=str(value[0])))
                        if 'No Response' in value[1]:
                            f.write(' ; szr nor')
                        else:
                            for n in nor:
                                if n in value[1]:
                                    f.write(' ; nor')
                        f.write('\n')

                # Writing Nets
                if table.is_scale:
                    if table.reverse_scale:
                        if table.move_scale:
                            if table.data_col_range:
                                f.write("R Top 2 Box ({label1}//{label2}) ; R({col1}:{col2},{punch1},{punch2})\n".format(
                                    label1=table.value_pair[-3][1], label2=table.value_pair[-2][1],
                                    col1=str(table.data_col[0]),
                                    col2=str(table.data_col[1]), punch1=str(table.value_pair[-3][0]),
                                    punch2=str(table.value_pair[-2][0])))
                                f.write("R Bottom 2 Box ({label1}//{label2}) ; R({col1}:{col2},1,2)\n".format(
                                    label1=table.value_pair[0][1], label2=table.value_pair[1][1],
                                    col1=str(table.data_col[0]),
                                    col2=str(table.data_col[1])))
                            else:
                                f.write("R Top 2 Box ({label1}//{label2}) ; {col}-{punch1},{punch2}\n".format(
                                    label1=table.value_pair[-3][1], label2=table.value_pair[-2][1],
                                    col=str(table.data_col[0]),
                                    punch1=str(table.value_pair[-3][0]), punch2=str(table.value_pair[-2][0])))
                                f.write("R Bottom 2 Box ({label1}//{label2}) ; {col}-1,2\n".format(
                                    label1=table.value_pair[0][1], label2=table.value_pair[1][1],
                                    col=str(table.data_col[0])))
                        else:
                            if table.data_col_range:
                                f.write("R Top 2 Box ({label1}//{label2}) ; R({col1}:{col2},{punch1},{punch2})\n".format(
                                    label1=table.value_pair[-2][1], label2=table.value_pair[-1][1],
                                    col1=str(table.data_col[0]),
                                    col2=str(table.data_col[1]), punch1=str(table.value_pair[-2][0]),
                                    punch2=str(table.value_pair[-1][0])))
                                f.write("R Bottom 2 Box ({label1}//{label2}) ; R({col1}:{col2},1,2)\n".format(
                                    label1=table.value_pair[0][1], label2=table.value_pair[1][1],
                                    col1=str(table.data_col[0]),
                                    col2=str(table.data_col[1])))
                            else:
                                f.write("R Top 2 Box ({label1}//{label2}) ; {col}-{punch1},{punch2}\n".format(
                                    label1=table.value_pair[-2][1], label2=table.value_pair[-1][1],
                                    col=str(table.data_col[0]),
                                    punch1=str(table.value_pair[-2][0]), punch2=str(table.value_pair[-1][0])))
                                f.write("R Bottom 2 Box ({label1}//{label2}) ; {col}-1,2\n".format(
                                    label1=table.value_pair[0][1], label2=table.value_pair[1][1],
                                    col=str(table.data_col[0])))
                    else:
                        if table.move_scale:
                            if table.data_col_range:
                                f.write("R Top 2 Box ({label1}//{label2}) ; R({col1}:{col2},1,2)\n".format(
                                    label1=table.value_pair[0][1], label2=table.value_pair[1][1],
                                    col1=str(table.data_col[0]),
                                    col2=str(table.data_col[1])))
                                f.write(
                                    "R Bottom 2 Box ({label1}//{label2}) ; R({col}:{col2},{punch1},{punch2})\n".format(
                                        label1=table.value_pair[-3][1], label2=table.value_pair[-2][1],
                                        col1=str(table.data_col[0]), col2=str(table.data_col[1]),
                                        punch1=str(table.value_pair[-3][0]),
                                        punch2=str(table.value_pair[-2][0])))
                            else:
                                f.write("R Top 2 Box ({label1}//{label2}) ; {col}-1,2\n".format(
                                    label1=table.value_pair[0][1], label2=table.value_pair[1][1],
                                    col=str(table.data_col[0])))
                                f.write("R Bottom 2 Box ({label1}//{label2}) ; {col}-{punch1},{punch2}\n".format(
                                    label1=table.value_pair[-3][1], label2=table.value_pair[-2][1],
                                    col=str(table.data_col[0]),
                                    punch1=str(table.value_pair[-3][0]), punch2=str(table.value_pair[-2][0])))
                        else:
                            if table.data_col_range:
                                f.write("R Top 2 Box ({label1}//{label2}) ; R({col1}:{col2},1,2)\n".format(
                                    label1=table.value_pair[0][1], label2=table.value_pair[1][1],
                                    col1=str(table.data_col[0]),
                                    col2=str(table.data_col[1])))
                                f.write(
                                    "R Bottom 2 Box ({label1}//{label2}) ; R({col1}:{col2},{punch1},{punch2})\n".format(
                                        label1=table.value_pair[-2][1], label2=table.value_pair[-1][1],
                                        col1=str(table.data_col[0]), col2=str(table.data_col[1]),
                                        punch1=str(table.value_pair[-2][0]),
                                        punch2=str(table.value_pair[-1][0])))
                            else:
                                f.write("R Top 2 Box ({label1}//{label2}) ; {col}-1,2\n".format(
                                    label1=table.value_pair[0][1], label2=table.value_pair[1][1],
                                    col=str(table.data_col[0])))
                                f.write("R Bottom 2 Box ({label1}//{label2}) ; {col}-{punch1},{punch2}\n".format(
                                    label1=table.value_pair[-2][1], label2=table.value_pair[-1][1],
                                    col=str(table.data_col[0]),
                                    punch1=str(table.value_pair[-2][0]), punch2=str(table.value_pair[-1][0])))
                f.write("*\n")
                table.table_range.append(table_number)
                table_number += 1
    print("There are {tnumber} tables.\n".format(tnumber=table_number))
    f.close()


def print_sumgentabs(tables,path):
    """
    :param tables: Input list of table variables
    :return: prints out to new file.
    """
    sum_table_number = input("Please enter first sum table number: ")
    sum_table_number = int(sum_table_number)
    sum_gen_tab_number = 5501
    sum_gen_tab_list = []

    with open(path + "/sumgentabs.txt", "w", encoding="utf-8") as f:
        for table in tables:
            if (table.is_loop or table.split_loop_head) and not table.is_multi:
                if table.is_numeric:
                    sum_gen_tab_number += 1
                    f.write("Table {table_number}\n".format(table_number=str(sum_table_number)))
                    f.write("T {var_name}_SUM_1\n".format(var_name=table.name))
                    f.write("T Mean Summary\n")
                    f.write("T {qtext}\n".format(qtext=table.qtext.replace("/","//")))
                    f.write('T Respondents: {base}\n'.format(base=table.base))

                    # Writing Q line
                    #print(table.name)
                    f.write(
                        "Q {col1}:{col2}n$\n".format(col1=str(table.loop_pair[0][1]), col2=str(table.loop_pair[-1][2])))

                    # Writing R lines
                    for loop in table.loop_pair:
                        f.write("R {rowtext} ; A({col1}:{col2}) ; freq fdp 1\n".format(rowtext=loop[0], col1=loop[1],
                                                                                       col2=loop[2]))

                    table.sum_table_numbers.append(sum_table_number)
                    sum_table_number = (int(int(sum_table_number) / 10) * 10) + 11
                    f.write("*\n")
                elif table.is_scale:
                    table.sum_table_numbers = [sum_table_number, sum_table_number + 8]
                    # T Lines
                    f.write("Table {table_number}\n".format(table_number=str(sum_gen_tab_number)))
                    sum_gen_tab_list.append(sum_gen_tab_number)
                    sum_gen_tab_number += 1
                    f.write("T {var_name}_SUM_{gen_num}\n".format(var_name=table.name, gen_num="{1}"))
                    f.write("T {2}\n")
                    f.write("T {qtext}\n".format(qtext=table.qtext.replace("/","//")))
                    f.write('T Respondents: {base}\n'.format(base=table.base))

                    if table.data_col_range:
                       ##if table.split_loop_head:
                       ##    f.write("Q ")
                       ##    for loop in table.loop_pair:
                       ##        if loop ==
                        f.write("Q {col1}:{col2}n$\n".format(col1=str(table.loop_pair[0][1]), col2=str(table.loop_pair[-1][2])))
                    else:
                        f.write("Q {col1}:{col2}n$\n".format(col1=str(table.loop_pair[0][1]), col2=str(table.loop_pair[-1][1])))




                    # Row Lines
                    for loop in table.loop_pair:
                        if table.data_col_range:
                            f.write(
                                "R {rowtext} ; R({col1}:{col2},{gen_num}) {col1}:{col2}n$ ; vb d{row_number}\n".format(
                                    rowtext=loop[0], col1=loop[1], col2=loop[2], row_number=len(table.loop_pair),
                                    gen_num="{5}"))
                        else:
                            f.write("R {rowtext} ; {col}-{gen_num} {col}n$ ; vb d{row_number}\n".format(rowtext=loop[0],
                                                                                                        col=loop[1],
                                                                                                        row_number=len(
                                                                                                            table.loop_pair),
                                                                                                        gen_num="{5}"))

                    # Row Base Lines
                    for loop in table.loop_pair:
                        if table.data_col_range:
                            f.write("R BASE: {rowtext} ; {col1}:{col2}n$ ; nopr\n".format(rowtext=loop[0], col1=loop[1],
                                                                                          col2=loop[2], row_number=len(
                                    table.loop_pair)))
                        else:
                            f.write("R BASE: {rowtext} ; {col}n$ ; nopr\n".format(rowtext=loop[0], col=loop[1],
                                                                                  row_number=len(table.loop_pair)))

                    # X lines
                    f.write("X gentab {first_sum}th{last_sum}\n".format(first_sum=str(sum_table_number),
                                                                        last_sum=str(sum_table_number + 3)))
                    f.write("X step 1 from 1\n")
                    f.write("X step 2\n")

                    sum_values = ["Top Box", "Top 2 Box", "Bottom 2 Box", "Bottom Box"]

                    if table.reverse_scale:
                        f.write("X \"Top Box ({rt1})\"\n".format(rt1=table.value_pair[table.t2b[1]][1]))
                        f.write("X \"Top 2 Box ({rt1}//{rt2})\"\n".format(rt1=table.value_pair[table.t2b[0]][1],rt2=table.value_pair[table.t2b[1]][1]))
                        f.write("X \"Bottom 2 Box ({rt1}//{rt2})\"\n".format(rt1=table.value_pair[table.b2b[0]][1],rt2=table.value_pair[table.b2b[1]][1]))
                        f.write("X \"Bottom Box ({rt1})\"\n".format(rt1=table.value_pair[table.b2b[0]][1]))

                    else:
                        f.write("X \"Top Box ({rt1})\"\n".format(rt1=table.value_pair[table.t2b[0]][1]))
                        f.write("X \"Top 2 Box ({rt1}//{rt2})\"\n".format(rt1=table.value_pair[table.t2b[0]][1],rt2=table.value_pair[table.t2b[1]][1]))
                        f.write("X \"Bottom 2 Box ({rt1}//{rt2})\"\n".format(rt1=table.value_pair[table.b2b[0]][1],rt2=table.value_pair[table.b2b[1]][1]))
                        f.write("X \"Bottom Box ({rt1})\"\n".format(rt1=table.value_pair[table.b2b[1]][1]))





                    f.write("X step 5\n")

                    if table.reverse_scale:
                        f.write("X \"{sum_punch}\"\n".format(sum_punch=str(table.t2b[1] + 1)))
                        f.write("X \"{sum_punch},{sum_punch2}\"\n".format(sum_punch=str(table.t2b[0] + 1),
                                                                          sum_punch2=str(table.t2b[1] + 1)))
                        f.write("X \"{sum_punch},{sum_punch2}\"\n".format(sum_punch=str(table.b2b[0] + 1),
                                                                          sum_punch2=str(table.b2b[1] + 1)))
                        f.write("X \"{sum_punch}\"\n".format(sum_punch=str(table.b2b[0] + 1)))

                    else:
                        f.write("X \"{sum_punch}\"\n".format(sum_punch=str(table.t2b[0] + 1)))
                        f.write("X \"{sum_punch},{sum_punch2}\"\n".format(sum_punch=str(table.t2b[0] + 1),
                                                                          sum_punch2=str(table.t2b[1] + 1)))
                        f.write("X \"{sum_punch},{sum_punch2}\"\n".format(sum_punch=str(table.b2b[0] + 1),
                                                                          sum_punch2=str(table.b2b[1] + 1)))
                        f.write("X \"{sum_punch}\"\n".format(sum_punch=str(table.b2b[1] + 1)))

                    table.sum_table_numbers.append(sum_table_number)
                    table.sum_table_numbers.append(sum_table_number + 3)
                    sum_table_number = (int(int(sum_table_number) / 10) * 10) + 11
                    f.write("*\n")
                else:
                    table.sum_table_numbers = [sum_table_number, sum_table_number + 9]
                    # T Lines
                    f.write("Table {table_number}\n".format(table_number=str(sum_gen_tab_number)))
                    sum_gen_tab_list.append(sum_gen_tab_number)
                    sum_gen_tab_number += 1
                    f.write("T {var_name}_SUM_{gennumber}\n".format(var_name=table.name, gennumber="{1}"))
                    f.write("T {2}\n")
                    f.write("T {qtext}\n".format(qtext=table.qtext.replace("/","//")))
                    f.write('T Respondents: {base}\n'.format(base=table.base))

                    if table.data_col_range:
                        f.write("Q {col1}:{col2}n$\n".format(col1=str(table.loop_pair[0][1]), col2=str(table.loop_pair[-1][2])))
                    else:
                        f.write("Q {col1}:{col2}n$\n".format(col1=str(table.loop_pair[0][1]), col2=str(table.loop_pair[-1][1])))


                    # Row Lines
                    print(table.name)
                    for loop in table.loop_pair:
                        if table.data_col_range:
                            f.write(
                                "R {rowtext} ; R({col1}:{col2},{gen_num}) {col1}:{col2}n$ ; vb d{row_number}\n".format(
                                    rowtext=loop[0], col1=loop[1], col2=loop[2], row_number=len(table.loop_pair),
                                    gen_num="{5}"))
                        else:
                            f.write("R {rowtext} ; {col}-{gen_num} {col}n$ ; vb d{row_number}\n".format(rowtext=loop[0],
                                                                                                        col=loop[1],
                                                                                                        row_number=len(
                                                                                                            table.loop_pair),
                                                                                                        gen_num="{5}"))

                    # Row Base Lines
                    for loop in table.loop_pair:
                        if table.data_col_range:
                            f.write("R BASE: {rowtext} ; {col1}:{col2}n$ ; nopr\n".format(rowtext=loop[0], col1=loop[1],
                                                                                          col2=loop[2], row_number=len(
                                    table.loop_pair)))
                        else:
                            f.write("R BASE: {rowtext} ; {col}n$ ; nopr\n".format(rowtext=loop[0], col=loop[1],
                                                                                  row_number=len(table.loop_pair)))

                    # X lines
                    f.write("X gentab {first_sum}th{last_sum}\n".format(first_sum=str(sum_table_number),
                                                                        last_sum=str(sum_table_number + len(
                                                                            table.value_pair) - 1)))
                    f.write("X step 1 from 1\n")
                    f.write("X step 2\n")

                    for n in table.value_pair:
                        f.write("X \"{sum}\"\n".format(sum=n[1]))

                    f.write("X step 5\n")
                    for n in table.value_pair:
                        f.write("X \"{sum}\"\n".format(sum=n[0]))

                    table.sum_table_numbers.append(sum_table_number)
                    table.sum_table_numbers.append(sum_table_number + len(table.value_pair) - 1)
                    sum_table_number = (int(int(sum_table_number) / 10) * 10) + 11
                    f.write("*\n")
        f.write("Table 5500\n")
        for x in sum_gen_tab_list:
            f.write("X gen {table_num}\n".format(table_num=x))
        f.close()


def print_gentabs(tables,path):
    """
    :param tables: list of variables
    :return: None
    This function prints all non-summary gentabs
    """
    gen_tab_number = 5001
    gentab_list = []

    with open(path + "/gentabs.txt", "w", encoding="utf-8") as f:
        for table in tables:
            if (table.is_loop or table.split_loop_head) and not table.is_multi:
                if table.is_numeric:
                    f.write('Table ' + str(gen_tab_number) + '\n')
                    gentab_list.append(gen_tab_number)
                    gen_tab_number += 1
                    f.write('T ' + table.name + "_{1}\n")
                    f.write('T {2}\n')
                    f.write('T ' + table.qtext.replace("/","//") + '\n')
                    f.write('T Respondents: {base}\n'.format(base=table.base))

                    # Writing Q lines
                    f.write('Q {5}:{6}n$ \n')

                    # Writing O lines
                    f.write('O span {5}:{6} \n')
                    f.write('R Mean ; A({5}:{6}) ; freq fdp 1\n')
                    f.write('R Median ; PC({5}:{6},50) ; freq fdp 0\n')

                    # Writing X lines
                    f.write("X gentab ")
                    for t in table.table_range:
                        f.write(str(t) + " ")
                    f.write("\n")

                    f.write("X Step 1 from 1\n")
                    f.write("X step 2\n")
                    for loop in table.loop_pair:
                        f.write("X \"{loop_text}\"\n".format(loop_text=loop[0]))

                    f.write("X step 5\n")
                    for loop in table.loop_pair:
                        f.write("X \"{loop_col1}\"\n".format(loop_col1=loop[1]))

                    f.write("X step 6\n")
                    for loop in table.loop_pair:
                        f.write("X \"{loop_col2}\"\n".format(loop_col2=loop[2]))

                    f.write("*\n")
                else:
                    f.write('Table ' + str(gen_tab_number) + '\n')
                    gentab_list.append(gen_tab_number)
                    gen_tab_number += 1
                    f.write('T ' + table.name + "_{1}\n")
                    f.write('T {2}\n')
                    f.write('T ' + table.qtext.replace("/","//") + '\n')
                    f.write('T Respondents: {base}\n'.format(base=table.base))

                    # Writing Q lines
                    if table.data_col_range:
                        f.write("Q {5}:{6}n$\n")
                    else:
                        f.write("Q {5}n$\n")

                    # Writing R Lines
                    if not table.reverse_scale:
                        for value in table.value_pair:
                            if table.data_col_range:
                                f.write("R {rowtext} ; R({gen5}:{gen6},{punch})".format(rowtext=value[1],gen5="{5}",gen6="{6}",punch=value[0]))
                                if 'No Response' in value[1]:
                                    f.write(' ; szr nor')
                                else:
                                    for n in nor:
                                        if n in value[1]:
                                            f.write(' ; nor')
                                f.write('\n')
                            else:
                                f.write("R {rowtext} ; {gen5}-{punch}".format(rowtext=value[1],gen5="{5}",punch=value[0]))
                                if 'No Response' in value[1]:
                                    f.write(' ; szr nor')
                                else:
                                    for n in nor:
                                        if n in value[1]:
                                            f.write(' ; nor')
                                f.write('\n')
                    else:
                        for value in reversed(table.value_pair):
                            if table.data_col_range:
                                f.write("R {rowtext} ; R({gen5}:{gen6},{punch})".format(rowtext=value[1],gen5="{5}",gen6="{6}",punch=value[0]))
                                if 'No Response' in value[1]:
                                    f.write(' ; szr nor')
                                else:
                                    for n in nor:
                                        if n in value[1]:
                                            f.write(' ; nor')
                                f.write('\n')
                            else:
                                f.write("R {rowtext} ; {gen5}-{punch}".format(rowtext=value[1],gen5="{5}",punch=value[0]))
                                if 'No Response' in value[1]:
                                    f.write(' ; szr nor')
                                else:
                                    for n in nor:
                                        if n in value[1]:
                                            f.write(' ; nor')
                                f.write('\n')



                    if table.is_scale:
                        if table.data_col_range:
                            f.write("R Top 2 Box ({rowtext1}//{rowtext2}) ; R({gen5}:{gen6},{punch1},{punch2})\n".format(gen6="{6}",rowtext1=table.value_pair[table.t2b[0]][1],rowtext2=table.value_pair[table.t2b[1]][1],gen5="{5}",punch1=table.value_pair[table.t2b[0]][0],punch2=table.value_pair[table.t2b[1]][0]))
                            f.write("R Bottom 2 Box ({rowtext1}//{rowtext2}) ; R({gen5}:{gen6},{punch1},{punch2})\n".format(gen6="{6}",rowtext1=table.value_pair[table.b2b[0]][1],rowtext2=table.value_pair[table.b2b[1]][1],gen5="{5}",punch1=table.value_pair[table.b2b[0]][0],punch2=table.value_pair[table.b2b[1]][0]))

                        else:
                            f.write("R Top 2 Box ({rowtext1}//{rowtext2}) ; {gen5}-{punch1},{punch2}\n".format(rowtext1=table.value_pair[table.t2b[0]][1],rowtext2=table.value_pair[table.t2b[1]][1],gen5="{5}",punch1=table.value_pair[table.t2b[0]][0],punch2=table.value_pair[table.t2b[1]][0]))
                            f.write("R Bottom 2 Box ({rowtext1}//{rowtext2}) ; {gen5}-{punch1},{punch2}\n".format(rowtext1=table.value_pair[table.b2b[0]][1],rowtext2=table.value_pair[table.b2b[1]][1],gen5="{5}",punch1=table.value_pair[table.b2b[0]][0],punch2=table.value_pair[table.b2b[1]][0]))

                    # Writing X lines
                    f.write("X gentab ")
                    for t in table.table_range:
                        f.write(str(t) + " ")
                    f.write("\n")

                    f.write("X Step 1 from 1\n")
                    f.write("X step 2\n")
                    for loop in table.loop_pair:
                        f.write("X \"{loop_text}\"\n".format(loop_text=loop[0]))

                    f.write("X step 5\n")
                    for loop in table.loop_pair:
                        f.write("X \"{loop_col1}\"\n".format(loop_col1=loop[1]))

                    if table.data_col_range:
                        f.write("X step 6\n")
                        for loop in table.loop_pair:
                            f.write("X \"{loop_col2}\"\n".format(loop_col2=loop[2]))
                    f.write("*\n")
        f.write("Table 5000\n")
        for x in gentab_list:
            f.write("X gen {table_num}\n".format(table_num=x))
        f.close()


def print_9999(tables,path):
    """
    This function prints out 9999 table with sum tables after tables
    :param tables: list of tables
    :return:
    """

    with open(path + "/9999.txt", "w", encoding="utf-8") as f:
        f.write("Table 9999\n")
        f.write('X set pline 2000\n')
        f.write('X set using off\n')
        f.write('X set qual off\n')
        f.write('X set suppress .1\n')
        f.write('X ^--\n')
        f.write('X set qual off\n')

        prev_tab = 0
        current_tab = 1
        run_order = "1"

        order = []
        for table in tables:
            if (table.is_loop or table.split_loop_head) and not table.is_multi:
                loop_tables = str(table.table_range[0]) + "th" + str(table.table_range[-1])
                order.append(loop_tables)
                if table.is_numeric:
                    order.append(table.sum_table_numbers[0])
                else:
                    loop_sumtables = str(table.sum_table_numbers[0]) + "th" + str(table.sum_table_numbers[0]+9)
                    order.append(loop_sumtables)
            else:
                order.append(table.table_range[0])

        print(order)

        for i in range(0,len(order)):
            if i == 0:
                run_order = str(order[i])
            elif i == len(order)-1:
                if isinstance(order[i], int):
                    if isinstance(order[i - 1], int):
                        if order[i] == order[i - 1] + 1:
                            run_order += "th" + str(order[i]) + " "
                        else:
                            run_order += " " + str(order[i]) + " "
                else:
                    run_order += str(order[i])
            elif isinstance(order[i],int):
                if isinstance(order[i-1],int):
                    if isinstance(order[i+1],int):
                        if order[i] == order[i-1]+1:
                            continue
                        else:
                            print(order[i], order[i - 1])
                            run_order += " " + str(order[i])
                    else:
                        if order[i] == order[i-1]+1:
                            print(order[i], order[i-1])
                            run_order += "th" + str(order[i]) + " "
                        else:
                            run_order += " " + str(order[i]) + " "
                else:
                    if isinstance(order[i+1],int):
                        run_order += str(order[i])
                    else:
                        run_order += str(order[i]) + " "
            elif isinstance(order[i],str):
                run_order += str(order[i]) + " "

        f.write('X run ' + run_order + ' b 9001 off excel (name \'[jobname]\' sheet \'Total\' combine ini)\n')
        f.write('X run ' + run_order + ' b 9001 off excel (name \'[jobname]\' sheet \'SORT\' combine)\n')
        f.write('X ^--\n')
        f.write('X set using off\n')
        f.write('X set qual off\n')
        f.close()

def print_grids(tables,path):
    """
    :param tables: list of variables
    :return: none
    This function prints grid tables in case needed
    """
    grid_number = 4000
    with open(path + "/gridtables.txt", "w", encoding="utf-8") as f:

        for table in tables:
            if (table.is_loop or table.split_loop_head) and not table.is_numeric and not table.is_multi:
                f.write('*\n')
                f.write('Table {tnum}\n'.format(tnum=str(grid_number)))
                grid_number += 1
                f.write('T {name}_GRID\n'.format(name=table.name))
                f.write('T Grid Table\n')
                f.write('T {text}\n'.format(text=table.qtext.replace("/","//")))
                f.write('T Respondents: {Base}\n'.format(Base=table.base))

                # Writing O Lines
                f.write('O F 28 6 1 0 ZPC \' * \' ZPA \' - \' ZC \' - \' NOFREQ PDP 0 PCTS BLEED NOTABNO\n')
                f.write('R Base: Unweighted     ;all ;nor freq novp nosigma nosgtest nottest now\n')
                f.write('R Base: Weighted       ;all ;nor freq novp nosigma nosgtest nottest\n')

                # Writing R Lines
                for value in table.value_pair:
                    if not table.data_col_range:
                        f.write('R {text} ; [1]-{punch}\n'.format(text=value[1],punch=value[0]))
                    else:
                        f.write('R {text} ; R([1],{punch})\n'.format(text=value[1],punch=value[0]))



                # Writing C Lines
                for loop in table.loop_pair:
                    if not table.data_col_range:
                        f.write("C {text} ; {qual}n$ ; def 1 '{qual}'\n".format(text=loop[0],qual=loop[1]))
                    else:
                        f.write("C {text} ; {qual}:{qual2}n$ ; def 1 '{qual}:{qual2}'\n".format(text=loop[0],qual=loop[1],qual2=loop[2]))

def print_datamap(tables):
    with open("TableOfContents.txt", "w", encoding="utf-8") as f:
        for table in tables:
            if table.is_multi:
                loop_index = 0
                for loop in table.loop_pair:
                    f.write("{var}: {col}\n".format(var=table.loop_names[loop_index],col=loop[1]))
                    loop_index += 1
            elif table.is_loop:
                    loop_index = 0
                    for loop in table.loop_pair:
                        if not table.data_col_range:
                            f.write("{var}: {col}\n".format(var=table.loop_names[loop_index], col=loop[1]))
                        else:
                            f.write("{var}: {col}:{col2}\n".format(var=table.loop_names[loop_index], col=loop[1],col2=loop[2]))
                        loop_index += 1
            else:
                if not table.data_col_range:
                    f.write("{var}: {col}\n".format(var=table.name, col=table.data_col[0]))
                else:
                    f.write("{var}: {col}:{col2}\n".format(var=table.name, col=table.data_col[0], col2=table.data_col[1]))
