# -*- coding: utf-8 -*-
#Table to create the bigram table for our trainingsdata
import pandas as pd
import numpy as np
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('utf-8')

#ReadAllFiles
tweets = pd.read_csv('../../../data/data.tsv', sep='\t', encoding='utf-8')
usefullUnigrams = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
bigrams =[]
for i in range(len(usefullUnigrams)):
    for j in range(len(usefullUnigrams)):
        bigrams.append(usefullUnigrams[i]+usefullUnigrams[j])
spanishTrigrams=["que","ent","nte","con","est","ado","par","los","era",
                 "ien","men","per","sta","ara","una","por"]
englishTrigrams=["the","and","tha","ent","ing","ion","tio","for","nde",
                 "has","nce","edt","tis","oft","sth","men"]

multigrams = usefullUnigrams + bigrams+ spanishTrigrams+englishTrigrams
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
    multigramsList = []
    for bi in multigrams:
        if bi in word:
            multigramsList.append(1)
        else:
            multigramsList.append(0)
    hasUniGramDic[word] = multigramsList

#buildTable
colomns=["word"] + multigrams + ["label"]
data = []
for word in wordList:
    data.append([word] + hasUniGramDic[word] + [findLanguage(word)])
table= pd.DataFrame(data=data, columns=colomns)    
table.to_csv("wordLevelAbsolutMultiGramTable.csv", sep='\t')


