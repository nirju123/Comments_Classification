import pandas as pd

from model import  model
from tenacity import retry, stop_after_attempt, wait_fixed
import re


def extract_integers(text, size=10):
    # Define a regex pattern to match integers (both positive and negative)
    pattern = r'-?\d+'

    # Use re.findall() to find all matching integers in the text
    matches = re.findall(pattern, text)

    # Convert the matches to integers
    integers = list(map(int, matches))

    # Return the first 'size' integers
    return integers[:size]



@retry(stop=stop_after_attempt(2), wait=wait_fixed(30))
def classify(list_sentence):
    prompt = f"""   I will send you a list of ten statements ,statements can be in hindi or english , misspellings allowed you need to
                    individually classify those ten statements as 0 or 1 . you will return a list of ten integers . if  in the statement 
                    any question is asked the value at index i in the list returned will be 1 else you will return a value of 0 .
                    you will not return anything else other than list .
                    Now you have to classify given below list of statements as 0 or 1 :
                    list :{list_sentence} 
                    if it is something you can not classify due to safety or any other concern value at index i
                    should be -1 . 
                    if you are confused classify it as 0 .
                    Note:
                    An interrogative statement is one that asks a question and typically ends with a question mark 
                    (e.g., "What is your name?" or "tum kya kar rahe ho").                      
            """
    ans = model(prompt)

    return  extract_integers(ans)


def qwords(text):
    line = "if,can,is,are,was,were,do,have,could,may,will,shall,should,would,am,did,has,had"
    key_words = line.split(',')
    print(key_words)
    words = text.split()
    return (len(list(set(words).intersection(key_words))) != 0)

def analyze(filename):
    df = pd.read_csv(filename)
    print(df.sample(10))
    print(df.shape)

# analyze("/home/niraj/Downloads/data/chatbox_data/gemini/mc_all_chat.csv")



