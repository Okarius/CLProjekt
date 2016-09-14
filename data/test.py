#!/usr/bin/python
# -*- coding: utf-8 -*-
from nltk import tokenize
import pandas as pd
import re
import unicodedata
import string
import Queue
import threading
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')
outFile = "test.tsv"
tweetStringFile = 'Provided/testTweets.tsv'
tweetOffsetFile = 'Provided/en_es_test_data.tsv'
class TaggedTweet:
#A taggedTweet contains the tweet, an array with every word, and the correspondingg labels, the TweetID
#Most Important feature: Word-Label list through self.labels and self.words  labels[i] labels word[i]
    def __init__(self, _tweetString, _infoArray):
        self.tweetString = _tweetString
        self.infoArray = _infoArray
        self.tweetId =  _infoArray[0]["tweetId"]
        self.labels = [] 
        self.words = []
        self.badEntry = False
        if self.infoArray[len(self.infoArray)-1]["end"]+1 > len(_tweetString): #check if last end is longer than tweet
            self.badEntry = True #if this is the case, dont use this tweet
        if "  " in _tweetString:
            self.badEntry = True #if this is the case, dont use this tweet
        if "   " in _tweetString:
            self.badEntry = True #if this is the case, dont use this tweet
        if "    " in _tweetString:
            self.badEntry = True #if this is the case, dont use this tweet


    def initializeWords(self):      
        for t in self.infoArray:
            word = ""
            self.labels.append(str(t["label"]))
            for i in range(t["start"], t["end"]+1):
                word += str(self.tweetString[i].encode("utf-8"))
            self.words.append(word)
        if (" " in self.words):
            self.badEntry = True #if this is the case, dont use this tweet
    
tweets = pd.read_csv('tweetsStringData.tsv', sep='\t', encoding='utf-8')
tweetInfo = pd.read_csv('Provided/en_es_training_offsets.tsv', sep='\t', encoding='utf-8')
#tweets = pd.read_csv('tweets.tsv', sep='\t', encoding='utf-8')
#tweetInfo = pd.read_csv('idizesLang.tsv', sep='\t', encoding='utf-8')
tweetStrings = []#tweets['tweet']
#tweetStrings =  [ x for x in tweetStrings if "Not Found" not in str(x).encode("utf-8")]
#tweetStartStopArray will contain:
#A list. Each element will contain a list of rows corresponding to a tweet id.
#Goal is a list for every tweetId (with its row-content in the off-set data)
tweetStartStopArray = []
#savecount = 0
#startCopy = False
lastStop = 0
def getAllTweetInfos(tweetId,q):
    tweetIDInfo = []
    found = False
    global lastStop
    for j in range(lastStop,len(tweetInfo)):
        secondTweetId = tweetInfo["tweetId"][j]
        if(tweetId == secondTweetId):#search all rows where the tweet id fits
            tweetIDInfo.append(tweetInfo.loc[j])
            found = True
        if found and tweetId != secondTweetId:
            lastStop = j
            found = False
            break
            
    q.put(tweetIDInfo)
    #return tweetIDInfo            
   

for i in range(len(tweets)):
#    print tweets["tweet"][i]
    tweet = str(tweets["tweet"][i]).encode("utf-8")
    tweetId = tweets["tweetId"][i]
    tweetStrings.append(tweet)
    q = Queue.Queue()outFile = "test.tsv"
    threading.Thread(target=getAllTweetInfos, args=(tweetId, q)).start()
    result = q.get()
    tweetStartStopArray.append(result)
    #           startCopy = True
    #        if startCopy and tweetId != tweetInfo["tweetId"][j]:
    #            savecount = j
    #            startCopy = False
    #            break
       # tweetStartStopArray.append(async_result.get())




allTaggedTweets = []#This will be filled with taggedTweets
for i in range(len(tweetStartStopArray)):
    tweetIndex = list(tweets["tweetId"]).index(tweetStartStopArray[i][0]["tweetId"])
    newTaggedTweet = TaggedTweet(tweets["tweet"][tweetIndex],tweetStartStopArray[i])#give tweet and The list of rows to TaggedTweet
    if not newTaggedTweet.badEntry: # some entry have a longe "stop" than tweet is long
        newTaggedTweet.initializeWords() #set words and labels 
        if not newTaggedTweet.badEntry: # some entry have a longe "stop" than tweet is long
            allTaggedTweets.append(newTaggedTweet)


#Tweets to TSV
#id;tweetString;tweetWordArray;taggedLanguages
#1 english, 2 spanish, 0 other
f = open("data.tsv","w")
f.write("id\ttweetString\ttweetWordArray\ttaggedLanguages\n")
iD = 0
for t in allTaggedTweets:
    stringToWrite = ""
    stringToWrite = str(iD)+"\t"+t.tweetString+"\t"
    
    tweetWordArray = ""
    taggedLanguagesArray = ""
    for i in range(len(t.labels)):
        taggedLanguagesArray =taggedLanguagesArray+  t.labels[i] + " "
        tweetWordArray =tweetWordArray+  t.words[i] + " "
    
    stringToWrite =stringToWrite + tweetWordArray+"\t"+ taggedLanguagesArray  +  "\n"
    f.write(stringToWrite)
    iD = iD +1
    
f.close()