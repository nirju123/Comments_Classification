# Seperateing Query and Non-Query Comments of Youtube live videos 
---
## Background:
- Growing from its gaming roots, live-streaming video is now ubiquitous.
- In mid-March 2020, Google reported a 300-500% increase in searches for live-streaming platforms. Furthermore, data from YouTube revealed that watch time for live streams had increased by 250%.
- All told, between March and April 2020, the live-streaming sector grew by 45%, with the industry being up by 99% year over year.
- Marketing strategies have evolved with live videos, changing how brands interact with their audiences, with 28% of marketers now investing more in live streaming to tap into this burgeoning market.  


## Problem:
- Response is very essential part of good communication. If we can reduce the response time for queries, it will in turn improve 
communication which will improve user experience and can boost user engagement with live content.
- Currently livestream platforms, list all of user's posted comment together like praise, wish, random comments and spam with
 queries of users where user is expecting a response , if we can seperately list queries comments ,
  - It will be improve creator's readability and reduce time of response ,
  - Even for users it will be easier to focus on important conversation .

---
## Solution:
1. Idea is to make a Machine learning model to classify comments, which are question of viewer to creator or fellow viewers and
which are random comments.
2. Can be integrated with live video watching platforms like YouTube, Twitch for better user experience.

---
## Execution:
Trained a  Machine learning model to classify comments as Queries and Non-Queries (both hindi and english)

## Dataset:
- I used Chat Downloader a python library that allows user to  retrieve chat messages from livestreams, videos, clips and past broadcasts without authentication.
- Chat Downloader was used to scrape comments on youtube live of various channels. ( Python scripts in folder named chat_download inside data folder)
- Once all chat downloaded , chats where seperated as query and non-query using following methods:
  - First , a large of query comments were easily identifiable as query due to ( all Python scripts in folder named chat_download inside data folder)
    - persence of wh-words of english `what,when,why,who,whom,which,whose,where,how`
    - presence of auxiliary verb at starting of sentence `if,can,is,are,was,were,do,does,have,could,may,will,shall,should,would,am,did,has,had`
    - presence of wh-words for hindi `ky,kya,kyaa,kab,kb,kyo,kyon,kyu,kyun,kyoki,kaun,kon,kisko,kiska,kaunsa,konsa,kaha,kahan,kaise,kitna,kitne,kese,kiya,kia,kyse,kis,kisn,kidhr,kiski,kita,kitni,kh,konsi`
  - After this remaining comments were seperated using Prompt engineering ( all Python scripts in folder named gemini inside data folder)
    - Activated api for google gemini models, particularly gemini 1.5 pro which has a daily free limit of 1500 api calls
    - I made a prompt which used to send a set of 10 consecutive comments to api for classification results for all 10 comments , result as list of 10 integer
      - 1 for query
      - 0 for non-query
      - -1 for comments which can not be classified by model due to safety reasons
    - On the basis of response, corresponding comments used to be saved in query file, non-query or safety file.
    - The model was complex enough to handle such a task with reasonable accuracy, it took almost 3 days to go across all the remaining comments.
- Then all seperates files were merged with correct labels into a single file named all.csv. Comments in safety file ignored, but it can be labeled using human intervention.
  
Final data is stored in all.csv in data folder.

Frequency of  various labels after droping duplicates: 
- `class`  `Frequency`    `  Type   `
- `class 0` `25886`   `Non-Query comments`
- `class 1` `22815`     `Query comments`

## Process:
- Cleaned the text
  - removed html tags
  - removed urls etc 
- Created following new features 
  - string_length, total_words, unique_words 
  - column deoteing presence of wh-words of hindi or english, or presence of ? 
  - len(text)/(count of words)
- Experimented with various text embedding techniques
  - Bag of words
  - TFIDF
  - Google Word2Vec
  - Google Word2Vec + TFIDF
- Text embeddings were concatenated with previously created features to prepare X_train, X_test
- Trained following Machine learning algorithms on data due to their superior performance in past projects
  - Random Forrest
  - Xgboost
- At end Xgboost + TFIDF has best performance followed by Xgboost+(Google Word2Vec + TFIDF).

## Results:
### Model with best performance in terms of accuracy:
- only Word2Vec + Xgboost = 95.11 %
- Word2Vec + TF-IDF +Xgboost  = 97.72 % lesser than tfidf only
- Bag of words +Xgboost = 97%
- TFIDF + Xgboost = 98%
###### Random forrest algorithms had slightly less accuracy in each case, around a difference of 0.2 to 0.5.

###### Performace of best TFIDF + Xgboost:
- Class 0:
  - Precision: 0.97
  - Recall: 0.99
  - F1-Score: 0.98
  - Support: 5161
- Class 1:
  - Precision: 0.99
  - Recall: 0.97
  - F1-Score: 0.98
  - Support: 4580


- Overall Accuracy: 0.98

######  True Positive Results
![image](https://github.com/nirju123/Comments_Classification/blob/main/output_image/true_pos.png)  
######  True Negative Results
![image](https://github.com/nirju123/Comments_Classification/blob/main/output_image/true_neg.png)
######  False Positive Results
![image](https://github.com/nirju123/Comments_Classification/blob/main/output_image/false_pos.png)
######  False Negative Results
![image](https://github.com/nirju123/Comments_Classification/blob/main/output_image/false_neg.png)












