import pandas as pd
import csv
import os
import glob
from classify import classify
import time


folder_q = "/home/niraj/Downloads/data/chatbox_data/gemini/ques"
folder_r = "/home/niraj/Downloads/data/chatbox_data/gemini/rand"
folder_z = "/home/niraj/Downloads/data/chatbox_data/gemini/safety"

max_requests_per_minute = 950
# Calculate the interval in seconds between each request
interval = 60 / max_requests_per_minute
def get_filename(file_path):
    return os.path.basename(file_path)
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


def split_row_in_csv(filepath):
    print(filepath)
    filename = get_filename(filepath)
    filename_q = os.path.join(folder_q,filename)
    filename_r = os.path.join(folder_r, filename)
    filename_z = os.path.join(folder_z,filename)
    nq = 0
    nr = 0
    nz = 0
    n = 0
    list_sentence = []
    with open(filepath, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        for row in reader:
            n+=1
            if n<89184:
                pass
            else:
                if len(row["msg"].strip().split())>=4:
                    list_sentence.append(row["msg"])

            if len(list_sentence)==10:
                rows1 = []
                rows2 = []
                rows3 = []
                try:
                    ans = classify(list_sentence)
                    for i in range(0,10):
                        if ans[i]==1:
                            nq+=1
                            print(list_sentence[i], "->", 1, " ", n, "--", nq, "--", nz, "--", nr)
                            Dict = {"msg": list_sentence[i]}
                            rows1.append(Dict)
                        elif ans[i]==0:
                            nr+=1
                            print(list_sentence[i], "->", 0, " ", n, "--", nq, "--", nz, "--", nr)
                            Dict = {"msg": list_sentence[i]}
                            rows2.append(Dict)
                        else:
                            nz+=1
                            print(list_sentence[i], "->", -1, " ", n, "--", nq, "--", nz, "--", nr)
                            Dict = {"msg": list_sentence[i]}
                            rows3.append(Dict)
                    append_csv(filename_q, rows1, fieldnames)
                    append_csv(filename_r, rows2, fieldnames)
                    append_csv(filename_z, rows3, fieldnames)
                except Exception as e:
                    print(e)
                    nz+=10
                    rows_excep = []
                    for item in list_sentence:
                        Dict = {"msg": item}
                        rows_excep.append(Dict)
                    append_csv(filename_z, rows_excep, fieldnames)
                list_sentence.clear()
                time.sleep(interval)


def all_csv_files(file_pattern):
    # Get a list of all CSV files matching the file pattern
    all_files = glob.glob(file_pattern)
    for file in all_files:
        df = pd.read_csv(file)
        # print(df.sample(10))
        print(file,df.shape)
        # split_row_in_csv(file)


# Example usage
all_csv_files( '/home/niraj/Downloads/data/chatbox_data/medcram/*.csv')







