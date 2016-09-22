# -*- coding: utf-8 -*-

#Table to create the bigram table for our trainingsdata
import pandas as pd
import numpy as np
import sys

#uncomment for systems with non-utf8 default locale
#reload(sys)
#sys.setdefaultencoding('utf-8')

# read files
tweets = pd.read_csv('../data/data.tsv', sep='\t', encoding='utf-8')


# features definitions
unigrams= [".",")","!","@","#","+","-","*","'",":",";","^",">","<","|","(",
          "\"","[","]","…","☆","♡","&","“",",","$","","_","ə","ɛ","ʌ","ʃ",
          "á", "é", "í", "ó", "ú","ü","ñ", "¿",
          "1","2","3","4","5","6","7","8","9","0"]

letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m",
                   "n","o","p","q","r","s","t","u","v","w","x","y","z"]

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
                 "has","nce","edt","tis","oft","sth","men"]

multigrams = unigrams + letters + bigrams + spanishTrigrams + englishTrigrams


#GetListsWithContent
tweetsString =[] 
for s in tweets["tweetString"]:
    tweetsString.append(s)
    
tweetsArray =[] 
for s in tweets["tweetWordArray"]:
    tweetsArray.append(s.split(" "))
    
languageArray =[] 
for s in tweets["taggedLanguages"]:
    languageArray.append(s.split(" "))


#get all words    
wordSet = set()
for s in tweetsArray:
    wordSet = wordSet | set(s)
wordList = list(wordSet)
wordList.remove("")
wordList = [i.lower() for i in wordList]

def findLanguage(word):
    for i in range(len(tweetsArray)):
        if word in tweetsArray[i]: 
            return languageArray[i][tweetsArray[i].index(word)]
    return 1

#get Language of words
languages = []
for word in wordList:
    languages.append(findLanguage(word))
    
    
    
#check if unigram in word.  
hasUniGramDic = {}
for word in wordList:
    multigramsList = []
    for bi in multigrams:
        if bi in word:
            multigramsList.append(1)
        else:
            multigramsList.append(0)
    hasUniGramDic[word] = multigramsList

#build table
colomns=["word"] + multigrams + ["label"]
data = []
for word in wordList:
    data.append([word] + hasUniGramDic[word] + [findLanguage(word)])
table= pd.DataFrame(data=data, columns=colomns)    
table.to_csv("../data/multigram_wl_abs.csv", sep='\t', index=False)


