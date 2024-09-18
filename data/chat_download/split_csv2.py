import csv
import os
import pandas as pd
import glob

folder_name = "/home/niraj/Downloads/data/chatbox_data/campusx/t"
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


def split_row_in_csv(filename,key_word):
    filename_to = os.path.join(folder_name, f"{key_word}_chat.csv")
    print(key_word)
    rows_tut= []
    rows = []
    with open(filename, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        for row in reader:
            words = row['msg'].split()
            if  key_word in words:
                line = " ".join(words)
                row['msg'] = line
                rows_tut.append(row)
            else:
                rows.append(row)
        print(len(rows),len(rows_tut))
        if len(rows_tut)!=0:
            rewrite_csv(filename,rows,fieldnames)
            append_csv(filename_to,rows_tut,fieldnames)



def main():
    filename = "/home/niraj/Downloads/data/chatbox_data/campusx/t/ques.csv"
    df = pd.read_csv(filename)
    print(df.shape)

    line = "if,or"
    key_words = line.split(',')

    for key_word in key_words:
        split_row_in_csv(filename,key_word)

    file_pattern = "/home/niraj/Downloads/data/chatbox_data/campusx/t/*.csv"
    all_files = glob.glob(file_pattern)

    for file in all_files:
        df = pd.read_csv(file)
        print(file,df.shape)




main()