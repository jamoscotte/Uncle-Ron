# This file contains functions for the Banner Creator for Uncle

import re
import nltk

def write_col_headers(ban,f,ban_num):
    ch_index = 2
    f.write("Table {table_num}\n".format(table_num=str(9000 + ban_num)))
    chdf = ban["CH"]
    print(chdf)
    for i in range(1,len(chdf)):
        if isinstance(chdf[i],str):
            if i == 1:
                header = chdf[i]
                col1 = i+1
            else:
                if i == len(chdf) -1:
                    f.write(
                        "T &cc{range1}:{range2} {label}\n".format(range1=str(col1).zfill(3), range2=str(i).zfill(3), label=header))
                    header = chdf[i]
                else:
                    f.write("T &cc{range1}:{range2} {label}\n".format(range1=str(col1).zfill(3), range2=str(i).zfill(3),
                                                                      label=header))
                    header = chdf[i]
                    col1 =i+1
        else:
            if i == len(chdf) - 1:
                f.write(
                    "T &cc{range1}:{range2} {label}\n".format(range1=str(col1).zfill(3), range2=str(i+1).zfill(3), label=header))


def write_RO_lines(f):
    f.write("O F 28 6 1 0 ZPC ' * ' ZPA ' - ' ZC ' - ' NOFREQ PDP 0 PCTS BLEED NOTABNO\n")
    f.write('R Base: Unweighted     ;all                    ;nor freq novp nosigma nosgtest nottest now\n')
    f.write('R Base: Weighted       ;all                    ;nor freq novp nosigma nosgtest nottest\n')

def write_C_lines(ban,variables,f):

    f.write("C All ; ALL\n")
    ctdf = ban["CT"]
    cqdf = ban["CQ"]

    for i in range(1,len(ctdf)):
        ctext = ctdf[i]
        cqual = cqdf[i]

        f.write("C {col_text} ; ".format(col_text=ctext))

        andor_split = re.split(r'( AND |&| and | or | OR )', cqual)
        for qual in andor_split:
            if (qual == ' AND ') or (qual == '&') or (qual == ' and ') or (qual == ' or ') or (qual == ' OR '):
                f.write(qual)
                continue
            else:
                var_split = qual.replace(' ','').split("=")
                var_found = False
                for v in variables:
                    if var_found == True:
                        break
                    if v.name in qual:
                        if (len(var_split[0].replace(" ",'')) - len(v.name.replace(' ','')) > 1) or (len(v.name.replace(' ','')) - len(var_split[0].replace(" ",'')) > 1):
                            nested = input("Do these variables match? Input: {v1}  Potential Match: {v2} \n (Y,N)?".format(v1=var_split[0],v2=v.name))
                            if nested.lower() == 'n':
                                continue
                        var_found = True
                        if not v.is_loop and v.name == var_split[0]:
                            if v.data_col_range:
                                f.write("R({col1}:{col2},{punch}) ".format(col1=v.data_col[0],col2=v.data_col[1],punch=var_split[1].replace('C','').replace('-',':')))
                            else:
                                print(qual,var_split,v.data_col)
                                f.write("{col1}-{punch} ".format(col1=v.data_col[0],punch=var_split[1].replace('C','').replace('-',':')))
                        else:
                            closest_loop = [0,0,0]
                            loop_index = 0
                            for loop in v.loop_names:
                                if closest_loop[0] == 0:
                                    var_dist = nltk.edit_distance(qual, loop)
                                    closest_loop = [loop,var_dist,loop_index]
                                    loop_index += 1
                                else:
                                    var_dist = nltk.edit_distance(qual,loop)
                                    if var_dist < closest_loop[1]:
                                        closest_loop = [loop,var_dist,loop_index]
                                    loop_index += 1
                            print(closest_loop)
                            if v.data_col_range:
                                f.write("R({col1}:{col2},{punch}) ".format(col1=v.loop_pair[closest_loop[2]][1],col2=v.loop_pair[closest_loop[2]][2],punch=var_split[1].replace('C','').replace('-',':')))
                            else:
                                if v.is_multi:
                                    f.write("{col1}-1 ".format(col1=v.loop_pair[closest_loop[2]][1]))

                                else:
                                    f.write("{col1}-{punch} ".format(col1=v.loop_pair[closest_loop[2]][1],punch=var_split[1].replace('C','').replace('-',':')))
                        break
                if not var_found:
                    f.write("{missing}={punch} cant be identified ".format(missing=var_split[0],punch=var_split[1].replace('C','').replace('-',':')))
        f.write("\n")