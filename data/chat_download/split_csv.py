import csv
import os
import pandas as pd
import glob

folder_name = "/home/niraj/Downloads/data/chatbox_data/medcram"
def rewrite_csv(filename,rows,fieldnames):
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        print(f"New CSV file '{filename}' created successfully.")


def append_csv(filename, rows, fieldnames):
    with open(filename, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Check if the file is empty. If it is, write the header first.
        file_empty = file.tell() == 0
        if file_empty:
            writer.writeheader()

        writer.writerows(rows)
    print(f"New rows added to '{filename}' successfully.")


def split_row_in_csv_char(filename,q):
    filename_to = os.path.join(folder_name,f"{q}_chat.csv")
    print(filename_to)
    rows_q= []
    rows = []
    with open(filename, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        for row in reader:
            if q in row['msg']:
                rows_q.append(row)
            else:
                rows.append(row)
        print(len(rows),len(rows_q))
        if len(rows_q)!=0:
            rewrite_csv(filename,rows,fieldnames)
            append_csv(filename_to,rows_q,fieldnames)

def split_row_in_csv_char_with_limit(filename,q,l,name):
    filename_to = os.path.join(folder_name,f"{name}_chat.csv")
    print(filename_to)
    rows_q= []
    rows = []
    with open(filename, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        for row in reader:
            if q in row['msg'] and len(row["msg"].strip().split())>=l:
                rows_q.append(row)
            else:
                rows.append(row)
        print(len(rows),len(rows_q))
        if len(rows_q)!=0:
            rewrite_csv(filename,rows,fieldnames)
            append_csv(filename_to,rows_q,fieldnames)



def split_row_in_csv(filename,name,line):
    key_words = line.split(',')
    filename_to = os.path.join(folder_name, f"{name}_chat.csv")
    print(key_words)
    rows_tut= []
    rows = []
    with open(filename, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        for row in reader:
            words = row['msg'].split()
            if  len(list(set(words).intersection(key_words)))!=0:
                line = " ".join(words)
                row['msg'] = line
                rows_tut.append(row)
            else:
                rows.append(row)
        print(len(rows),len(rows_tut))
        rewrite_csv(filename,rows,fieldnames)
        append_csv(filename_to,rows_tut,fieldnames)


def split_row_in_csv_first(filename):
    name = "aux"
    line = "if,can,is,are,was,were,do,does,have,could,may,will,shall,should,would,am,did,has,had"
    key_words = line.split(',')
    filename_to = os.path.join(folder_name, f"{name}_chat.csv")
    print(key_words)
    rows_tut= []
    rows = []
    with open(filename, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        for row in reader:
            words = row['msg'].split()
            if len(words)<=1:
                pass
            elif words[0] in key_words:
                line = " ".join(words)
                row['msg'] = line
                rows_tut.append(row)
            else:
                rows.append(row)
        print(len(rows),len(rows_tut))
        rewrite_csv(filename,rows,fieldnames)
        append_csv(filename_to,rows_tut,fieldnames)

def main():
    filename = "/home/niraj/Downloads/data/chatbox_data/campusx/ques.csv"
    df = pd.read_csv(filename)
    print(df.shape)
    split_row_in_csv_char(filename,q=" do ")
    # split_row_in_csv(filename,"wh",line="what,when,why,who,whom,which,whose,where,how")

    # kwords = "ky,kya,kyaa,kab,kb,kyo,kyon,kyu,kyun,kyoki,kaun,kon,kisko,kiska,kaunsa,konsa,kaha,kahan,kaise,kitna,kitne,kese,kiya,kia,kyse,kis,kisn,kidhr,kiski,kita,kitni,kh,konsi"
    # split_row_in_csv(filename,"kh",line=kwords)


    # split_row_in_csv_first(filename)  # auxilliary

    # keywords =  "if,can,is,are,was,were,do,does,have,could,may,will,shall,should,would,am,did,has,had"
    # key_words = keywords.split(',')
    # pron = ["u","you","we","i","sir"]
    # for keyword in key_words:
    #     for pr in pron:
    #         key = (" " + keyword + " " + pr+" ")
    #         split_row_in_csv_char(filename,key)

    # for i in range(0,len(key_words)):
    #     if key_words[i]!="can":
    #         key_words[i] = key_words[i]+"n"+" "+"t"
    #     else:
    #         key_words[i] = key_words[i] + " " + "t"
    # print(key_words)
    # pron = ["u","you","we","i","sir"]
    # for keyword in key_words:
    #     for pr in pron:
    #         key = (" " + keyword + " " + pr+" ")
    #         split_row_in_csv_char(filename,key)
    # line = "what,when,why,who,whom,which,whose,where,how"
    # key_words = line.split(',')
    # for key_word in key_words:
    #     q = " "+key_word
    #     split_row_in_csv_char(filename,q)
    # split_row_in_csv_char(filename, " na ")
    # split_row_in_csv_char(filename, "na ")  # random
    # split_row_in_csv_char(filename, " difference between ")
    # split_row_in_csv_char(filename, " vs ")
    # split_row_in_csv(filename,"koi",line="koi")
    # split_row_in_csv(filename, "if", line="if")
    # split_row_in_csv_char(filename, " if ")
    # split_row_in_csv(filename, "ya", line="ya")
    # split_row_in_csv_char(filename, " ya ")
    # split_row_in_csv(filename, "agr", line="agr,agar")
    # split_row_in_csv_char_with_limit(filename, " agr ")
    # split_row_in_csv_char_with_limit(filename, " agar ")
    # split_row_in_csv(filename, "or", line="or")
    # split_row_in_csv_char_with_limit(filename, " or ",9,"or1")







main()