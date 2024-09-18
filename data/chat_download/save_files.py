import os
import csv


folder_loc = "/home/niraj/Downloads/data/chatbox_data/unacad/chats"
def new_name(name):
    name = name.replace("-", "")
    name = name.replace(".","_")
    name = name.replace(",", "_")
    name = name.replace(" ", "_")
    name = name.replace("/", "_")
    name = name.replace("__", "_")
    return name

def save_as_csv(chats, name,headers):
    filename = os.path.join(folder_loc, f"{name}.csv")


    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write the header
        writer.writerow(headers)

        # Write the data rows
        for chat in chats:
            writer.writerow(chat)

def save_as_txt(data, name):
    # Assuming new_name is a function that processes the name
    name = new_name(name)
    filename = os.path.join(folder_loc, f"{name}.txt")

    # Open the file in write mode
    with open(filename, mode='w', encoding='utf-8') as file:
        # Write each chat as a new line in the text file
        file.write(f"{data}")








