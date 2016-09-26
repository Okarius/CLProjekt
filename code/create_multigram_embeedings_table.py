# -*- coding: utf-8 -*-

#Table to create the bigram table for our trainingsdata
import pandas as pd
import numpy as np
import sys
import re

#uncomment for systems with non-utf8 default locale
#reload(sys)
#sys.setdefaultencoding('utf-8')

# read files
tweets = pd.read_csv('../data/data.tsv', sep='\t', encoding='utf-8')


# features definitions
unigrams= [".",")","!","@","#","+","-","*","'",":",";","^",">","<","|","(","\"",
          "[","]","…","☆","♡","&","“",",","$","ə","ɛ","ʌ","ʃ", "¿",
          "1","2","3","4","5","6","7","8","9","0"]

letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m",
           "n","o","p","q","r","s","t","u","v","w","x","y","z",
           "á", "é", "í", "ó", "ú","ü","ñ"]

capLetters = [i.upper() for i in letters]

bigrams =[]
for i in range(len(letters)):
    for j in range(len(letters)):
        bigrams.append(letters[i]+letters[j])
        
        
#spanishTrigrams=["que","ent","nte","con","est","ado","par","los","era",
#                 "ien","men","per","sta","ara","una","por"]
#englishTrigrams=["the","and","tha","ent","ing","ion","tio","for","nde",
#                 "has","nce","edt","tis","oft","sth","men"]

spanishTrigrams=["que","nte","con","est","ado","par","los","era",
                 "ien","per","sta","ara","una","por"]
englishTrigrams=["the","and","tha","ing","ion","tio","for","nde",
                 "has","nce","edt","tis","oft","sth"]

multigrams = unigrams + letters + bigrams + spanishTrigrams + englishTrigrams
    
wordList =[] #all words
tweetLength = [] #lengths

for s in tweets["tweetWordArray"]:
    #tweetWords = re.split(" +",s.lower().strip())
    tweetWords = re.split(" +",s.strip())
    wordList.extend(tweetWords)
    tweetLength.append(len(tweetWords))
    
languageList =[] 
for s in tweets["taggedLanguages"]:
    languageList.extend(re.split(" +",s.strip()))
    

#get language of words
languagesDict = {}
pos = 0
for i in range(len(tweets)):
    j_max = tweetLength[i];
    for j in range(j_max):
        langs = [] #len prev next cur
        
        langs.append(j_max)

        if j == 0:
            langs.append("start")
        else:
            ppos=pos-1
            langs.append(languageList[ppos])
        
        if j == j_max-1:
            langs.append("end")
        else:
            npos=pos+1
            langs.append(languageList[npos])
            
        langs.append(languageList[pos])
        
        word = wordList[pos];
        languagesDict[word] = langs
        pos = pos + 1
    
  

#check if ngram is present in word  
multigramsDict = {}
for word in wordList:
    multigramsList = []
    for mg in multigrams:
        if mg in word.lower():
            multigramsList.append(1)
        else:
            multigramsList.append(0)
    for l in capLetters:
        if l in word:
            multigramsList.append(1)
        else:
            multigramsList.append(0)
    multigramsDict[word] = multigramsList

#build table
colomns=["word"] + multigrams + capLetters + ["D#tLen"] + ["D#prev"] + ["D#next"] + ["c#label"]

data = []
for word in wordList:
    data.append([word] + multigramsDict[word] + languagesDict[word])
table= pd.DataFrame(data=data, columns=colomns)   

table.to_csv("../data/multigram_embedings.csv", sep='\t', index=False)
