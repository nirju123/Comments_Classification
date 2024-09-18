import pandas as pd
from save_files import save_as_csv, new_name
import os
from chat_downloader import ChatDownloader
import multiprocessing
import time
import random

def parse_message(log):
    # Split at the first occurrence of ' | ' to get time and the rest
    time, _, remainder = log.partition("|")

    # Split the remainder at the first occurrence of ': ' to get user_name and user_message
    user_name, _, user_message = remainder.partition(":")

    return [time, user_name, user_message]

def download_and_save_chat(row, name, n, t):
    try:
        chat = ChatDownloader().get_chat(row["url"])
        msgs = []
        for message in chat:
            msg = chat.format(message)
            print(msg, " ", f"{n}/{t}")
            msgs.append(parse_message(msg))
        save_as_csv(msgs, name, headers=["time", "username", "msg"])
    except Exception as e:
        print(f"An error occurred: {e}")
def get_chat(filename):
    df = pd.read_csv(filename)
    n = 0
    t = df.shape[0]

    for index, row in df.iterrows():
        print(index, row["title"], row["url"])
        n += 1
        try:
            name = new_name(row["title"]) + str(n)
            folder_loc = "/home/niraj/Downloads/data/chatbox_data/unacad/chats"
            filename = os.path.join(folder_loc, f"{name}.csv")
            if os.path.exists(filename):
                print("File does exist")
            else:
                p = multiprocessing.Process(target=download_and_save_chat, args=(row,name,n,t))
                p.start()

                # Wait for the process to finish, but with a timeout
                p.join(timeout=180)
                if p.is_alive():
                    print("Function took too long, skipping to next iteration and moveing to next iteration")
                    p.terminate()  # Terminate the process
                else:
                    print("Function completed within 7 seconds.")
        except Exception as e:
            print(e)



urls = [
        "/home/niraj/Downloads/data/chatbox_data/unacad/chats/url/un_ias_eng_url.csv",
        "/home/niraj/Downloads/data/chatbox_data/unacad/chats/url/un_neet_url.csv"
        ]
for url in urls:
    print(url)
    get_chat(url)

# "/home/niraj/Downloads/data/chatbox_data/unacad/chats/url/un_jee_url.csv",
# "/home/niraj/Downloads/data/chatbox_data/unacad/chats/url/un_ias_url.csv",