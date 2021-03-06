# -*- coding: utf-8 -*-
#Table to create the bigram table for our trainingsdata
import pandas as pd
import numpy as np
import sys

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('utf-8')

#ReadAllFiles
tweets = pd.read_csv('../data/data.tsv', sep='\t', encoding='utf-8')


smallSimulation = True
useOrange = False

usefullUnigrams = [".",")","!","@","#","+","-","*","'",":",";","^",">","<","|","(","\"","[","]","…","☆","♡","&","“",",","$","","_","ə","ɛ","ʌ","ʃ",
"á", "é", "í", "ó", "ú","ü","ñ", "¿",
"1","2","3","4","5","6","7","8","9","0",
"a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",
]

if smallSimulation == False:
    print ("nice")
    usefullUnigrams = usefullUnigrams + ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
bigrams =[]
for i in range(len(usefullUnigrams)):
    for j in range(len(usefullUnigrams)):
        bigrams.append(usefullUnigrams[i]+usefullUnigrams[j])


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


#get all Words    
wordSet = set()
for s in tweetsArray:
    wordSet = wordSet | set(s)
wordList = list(wordSet)
wordList.remove("")
if smallSimulation == False:
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
    
    
    
#check if Unigram in word.  
hasUniGramDic = {}
for word in wordList:
    bigramList = []
    for bi in bigrams:
        if bi in word:
            bigramList.append(1)
        else:
            bigramList.append(0)
    hasUniGramDic[word] = bigramList

#buildTable
if useOrange == True:
    bigrams=["D#"+b for b in bigrams]
    colomns=["m#word"] + bigrams + ["c#label"]
else:
    colomns=["word"] + bigrams + ["label"]

    
data = []
for word in wordList:
    data.append([word] + hasUniGramDic[word] + [findLanguage(word)])
table= pd.DataFrame(data=data, columns=colomns)    
table.to_csv("bigram_wl_abs.csv", sep='\t', index=False)


##build table for relativUnigrams
#hasUniGramDic = {}
#for word in wordList:
    #unigramList = []
    #for bi in bigrams:
        #if bi in word:
            #unigramList.append(1/len(word))
        #else:
            #unigramList.append(0)
    #hasUniGramDic[word] = unigramList


##buildTable
#colomns=["word"] + bigrams + ["label"]
#data = []
#for word in wordList:
    #data.append([word] + hasUniGramDic[word] + [findLanguage(word)])
#table= pd.DataFrame(data=data, columns=colomns)    
#table.to_csv("wordLevelRelativeBigramTable1.csv", sep='\t')
