# -*- coding: utf-8 -*-

#Table to create the bigram table for our trainingsdata
import pandas as pd
import numpy as np
import sys
import re

#uncomment for systems with non-utf8 default locale
#reload(sys)
#sys.setdefaultencoding('utf-8')

#enter string which should be tagged
in_str = "hello world amigos :-) español is a nice lenguaje ♡"


#tokenization
wordList = [] 
words = re.split(" +",in_str.strip())
numWords = len(words)
wordList.extend(words)


#features definitions
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
        

spanishTrigrams=["que","nte","con","est","ado","par","los","era",
                 "ien","per","sta","ara","una","por"]
englishTrigrams=["the","and","tha","ing","ion","tio","for","nde",
                 "has","nce","edt","tis","oft","sth"]

multigrams = unigrams + letters + bigrams + spanishTrigrams + englishTrigrams
    

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

languagesDict = {}
for word in wordList:
    langs = [] #len prev next cur
    langs.append(numWords)
    langs.append('')
    langs.append('')
    langs.append('')
    languagesDict[word] = langs

#build table
colomns=["word"] + multigrams + capLetters + ["D#tLen"] + ["D#prev"] + ["D#next"] + ["c#label"]

data = []
for word in wordList:
    data.append([word] + multigramsDict[word] + languagesDict[word])

table= pd.DataFrame(data=data, columns=colomns)   

table.to_csv("../data/test_multigrams.csv", sep='\t', index=False)
