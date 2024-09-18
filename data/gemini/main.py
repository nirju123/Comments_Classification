import os
from apikey import API_KEY
from model import  model

def classify(topic, question):
    prompt = f"""
                    We have a list of questions for  you, the questions can be in hindi or english,
                    there could be misspellings in the questions asked, the questions are being asked
                    by students in class of {topic}, your job is to identify whether the question is 
                    asked to teacher or it is a noise among students, below are few example of questions 
                    and there correct classification as Noise or Question :
                    Examples:
                    Question 1:"Is it good?"  
                    Answer: Nosie
                    Question 2:"HOW DO YOU DEAL WITH TECH BURNOUTS?"
                    Answer: Question              
                    Question 3:"My deployment failed. How do I solve it?"
                    Answer: Question          
                    Question 4:"kaha mar gaya salle, wait kar raha hun,"  
                    Answer: Noise     
                    Now you have to classify given below question as Question or Noise:
                    Question :{question}  
                    Also the name of the tutor is Harkirat Singh teaching on youtube . 
            """
    model(prompt)
def main():
    question = "  Hi harkirat please can you tell me how can you sit for long hours while coding "
    classify('Testing in Production',question)


main()




