#!/usr/bin/env python 
# -*- encoding: utf-8 -*-
import urllib2
import pandas as pd
from bs4 import BeautifulSoup
import time
import bleach
from sklearn.linear_model import LogisticRegression
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('utf-8')
####Help Funktion to predict a tweet####
def getBigramRowToWord(bigrams, word):
    bigramList = []
    for bi in bigrams:
        if bi in word:
            bigramList.append(1)
        else:
            bigramList.append(0)
    
    return bigramList
def predictWord(lr, word, bigrams):
    return lr.predict(getBigramRowToWord(bigrams,word))[0]
#########################################

#This function is necessary to work with tweets with multiple lines
def buildTweetFromScraperContent(content):
    string = ""
    for c in content:
        string = string + str(c)
    return string    
    
######Setup LogisticRegression###########    
train_data = pd.read_csv("bigram_wl_abs.csv", sep='\t') #readBigramTable
usefullUnigrams = [".",")","!","@","#","+","-","*","'",":",";","^",">","<","|","(","\"","[","]","…","☆","♡","&","“",",","$","","_","ə","ɛ","ʌ","ʃ",
"á", "é", "í", "ó", "ú","ü","ñ", "¿",
"1","2","3","4","5","6","7","8","9","0",
"a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
bigrams =[]
for i in range(len(usefullUnigrams)):
    for j in range(len(usefullUnigrams)):
        bigrams.append(usefullUnigrams[i]+usefullUnigrams[j]) ##create bigrams to read in table columns

X_train = train_data[bigrams]
y_train = train_data['label']
lr = LogisticRegression(C=50, penalty='l2', tol= 0.001) #Simple LogisticRegression without anything
lr.fit(X_train, y_train)
print "ready to work"
#########################################
newOffsetFile = open("newOffset.tsv","w")#write down new offsetFile




##Read old OffsetFile
f = open("../data/en_es_test_data.tsv")
oldOffsetLines = f.readlines()
f.close()
##



oldTweetId = ""
workingTweet = "\t\t\t\t\t\t"
badTweet= False
for l in oldOffsetLines:#read Every offsetLine
    splited = l.split("\t")
    tweetId = splited[0]
    userId= splited[1]
    start = splited[2]
    end = splited[3]
    if tweetId != oldTweetId:
        ##Webscrapping
        print "http://twitter.com/"+userId+"/status/"+tweetId
        oldTweetId = tweetId
        try: #try and except since there are a lot of 404 tweets
            response = urllib2.urlopen("http://twitter.com/"+userId+"/status/"+tweetId)#openTweet
            time.sleep(1) #sleep to not get banned 	                 
            html = response.read()#read HTML code
            soup = BeautifulSoup(html)#initialize BS
            mydivs = soup.find_all("p", class_="TweetTextSize TweetTextSize--26px js-tweet-text tweet-text")#Find all tweets, only the tweets not the comments or answers!
            tweetWithLinks = buildTweetFromScraperContent(mydivs[0].contents)        
            workingTweet =bleach.clean(tweetWithLinks, tags = ["img"], strip = True) #remove everything, like links. but keep the imgs
            if "<img" in workingTweet: #if the tweet has a img it is useless
                badTweet= True
            else:
                badTweet = False
        except:
            badTweet = True
    if not badTweet:
        word = workingTweet[int(start):int(end)+1]
        line =  tweetId + "\t"+userId+"\t"+start+"\t"+end+"\t"+str(predictWord(lr,word,bigrams))+ "\n"
    else:
        line =  tweetId + "\t"+userId+"\t"+start+"\t"+end+"\t"+"BadTweet"+ "\n"
    newOffsetFile.write(line)
#js-tweet-text-container