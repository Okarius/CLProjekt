import pandas as pd
import numpy as np
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('utf-8')
    

#ReadAllFiles
tweets = pd.read_csv('data/data.tsv', sep='\t', encoding='utf-8')
f = open("data/wordLevelNGrams/unigramsWordLevel.txt","r")
unigrams = f.readlines()
unigrams =[i.replace("\n","") for i in unigrams]
f.close()
f = open("data/wordLevelNGrams/bigramsWordLevel.txt","r")
bigrams = f.readlines()
bigrams =[i.replace("\n","") for i in bigrams]
f.close()


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


def findLanguage(word):
    for i in range(len(tweetsArray)):
        if word in tweetsArray[i]: 
            print str(tweetsArray[i]) + " " + str(len(tweetsArray[i]))
            print str(languageArray[i]) + " " + str(len(languageArray[i]))
            return languageArray[i][tweetsArray[i].index(word)]
    return 1

#get Language of words
languages = []
for word in wordList:
    languages.append(findLanguage(word))
    
    
    
#check if Unigram in word.  
hasUniGramDic = {}
for word in wordList:
    unigramList = []
    for uni in unigrams:
        if uni in word:
            unigramList.append(1)
        else:
            unigramList.append(0)
    hasUniGramDic[word] = unigramList

#buildTable
colomns=["word"] + unigrams + ["label"]
data = []
for word in wordList:
    data.append([word] + hasUniGramDic[word] + [findLanguage(word)])
table= pd.DataFrame(data=data, columns=colomns)    
table.to_csv("wordLevelAbolutUnigramTable.csv", sep='\t')



#build table for relativUnigrams
hasUniGramDic = {}
for word in wordList:
    unigramList = []
    for uni in unigrams:
        if uni in word:
            unigramList.append(1/len(word))
        else:
            unigramList.append(0)
    hasUniGramDic[word] = unigramList


#buildTable
colomns=["word"] + unigrams + ["label"]
data = []
for word in wordList:
    data.append([word] + hasUniGramDic[word] + [findLanguage(word)])
table= pd.DataFrame(data=data, columns=colomns)    
table.to_csv("wordLevelRelativeUnigramTable.csv", sep='\t')
