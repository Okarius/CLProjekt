# -*- coding: utf-8 -*-

import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn import cross_validation
import numpy as np
from numpy import mean, std
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('utf-8')


class predictedTweet:
    def getDifferences(self):
        count = 0
        for i in range(len(self.predicted)):
            if self.predicted[i] != self.actualLanguages[i]:
                count = count +1
            else:
                if "other" in self.predicted[i]:
                    self.correctOthers  = self.correctOthers+1
                if "ne" in self.predicted[i]:
                    self.correctNe=  self.correctNe+1
                if "mixed" in self.predicted[i]:
                    self.correctMixed =self.correctMixed+1
                if "ambiguous" in self.predicted[i]:
                    self.correctAmbiguous= self.correctAmbiguous+1
                if "lang" in self.predicted[i]:
                    self.correctLang = self.correctLang+1
                if "lang1" in self.predicted[i]:
                    self.correctEng = self.correctEng +1
                if "lang2" in self.predicted[i]:
                    self.correctSpan = self.correctSpan+1

        return count
    def __init__(self,predicted, actualLanguages, tweet):
        self.predicted = predicted
	self.tweet = tweet
        self.correctOthers  = 0
        self.correctNe= 0
        self.correctMixed =0
        self.correctAmbiguous= 0
        self.correctLang = 0
        self.correctEng = 0
        self.correctSpan =0
        self.actualLanguages = actualLanguages
        self.differences = self.getDifferences()
        self.wordsLeng = len(self.predicted)
        self.numberOfOther = self.actualLanguages.count("other")
        self.numberOfNe = self.actualLanguages.count("ne")
        self.numberOfMixed = self.actualLanguages.count("mixed")
        self.numberOfAmbiguous = self.actualLanguages.count("ambiguous")
        self.numberOfLang = self.actualLanguages.count("lang1") + self.actualLanguages.count("lang2")
        self.numberOfSpan = self.actualLanguages.count("lang2")
        self.numberOfEng=self.actualLanguages.count("lang1")

####Help Funktion to predict a tweet####
def getBigramRowToWord(bigrams, word):
    bigramList = []
    for bi in bigrams:
        if bi in word:
            bigramList.append(1)
        else:
            bigramList.append(0)
    
    return bigramList
def predictWords(lr, words, bigrams):
    predicted = []#["lang1","lang2","lang1"]
    for i in words:
        predicted.append(lr.predict(getBigramRowToWord(bigrams,i))[0])        
    return predicted
#########################################



folder = "wordLevelNGrams/nGramTables/"
train_data = pd.read_csv(folder+ 'wordLevelAbsolutBiGramTable.csv', sep='\t') #readBigramTable
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







###Evaluate Linear Regression###
test_data = pd.read_csv('../data/data.tsv', sep='\t')
taggedLanguages = list(test_data[len(test_data["taggedLanguages"])-5000:]["taggedLanguages"])
taggedLanguages = [i.split(" ") for i in taggedLanguages]
words = list(test_data[len(test_data["taggedLanguages"])-5000:]["tweetWordArray"])
words =[i.split(" ") for i in words]
for i in range(len(words)):
    words[i] = [j.lower() for j in words[i]]#ONLY LOWER CASE WORDS!!!!

#####Evaluate all words############
f = open("Results/LR_AllWords.csv","w")
predictedTweets = []
for i in range(len(words)):
    prediction = predictWords(lr,words[i],bigrams)
    predictedTweets.append(predictedTweet(prediction,taggedLanguages[i], words[i]))

    allWords = 0
    allDifferences = 0
    allOthers  = 0
    allLang = 0
    (others,nes,mixed,ambiguous,langs,cothers,cne,cmixed,cambiguous,clang,allSpan,allEng,cSpan,cEng) = 0,0,0,0,0,0,0,0,0,0,0,0,0,0
for i in predictedTweets:
    allWords = allWords + i.wordsLeng
    allDifferences= allDifferences + i.differences
    others = others +i.numberOfOther
    nes = nes +i.numberOfNe 
    mixed = mixed+i.numberOfMixed
    ambiguous = ambiguous+  i.numberOfAmbiguous
    langs = langs+ i.numberOfLang 
    cothers = cothers+ i.correctOthers  
    cne = cne+ i.correctNe
    cmixed = cmixed+ i.correctMixed 
    cambiguous = cambiguous + i.correctAmbiguous
    clang = clang+ i.correctLang
    cSpan = cSpan + i.correctSpan
    cEng = cEng + i.correctEng
    allSpan = allSpan + i.numberOfSpan
    allEng = allEng + i.numberOfEng

f.write("allWords: "+str(allWords)+ "\n")
f.write("allWrongLabelledWords: "+str(allDifferences)+ "\n")
f.write("allOthers: "+str(others)+ "\n")
f.write("allNe: "+str(nes)+ "\n")
f.write("allMixed: "+str(mixed)+ "\n")
f.write("allAmbiguous: "+str(ambiguous)+ "\n")
f.write("allLanguages: "+str(langs)+ "\n")
f.write("AccuracyOther: "+str(float(cothers)/others) + "\n")
f.write("AccuracyNe: "+str(float(cne)/nes)+ "\n")
f.write("AccuracyMixed: "+str(float(cmixed)/mixed)+ "\n")
f.write("AccuracyAmbiguous: "+str(float(cambiguous)/ambiguous)+ "\n")
f.write("AccuracyLanguages : "+str(float(clang)/langs)+ "\n")
f.write("AccuracySpanish : "+str(float(cSpan)/allSpan)+ "\n")
f.write("AccuracyEnglish : "+str(float(cEng)/allEng)+ "\n")
f.close()
#####################################
f = open("Results/LR_SentenceLength.csv","w")
f.write("SentenceLength;Accuracy;Tweets;relOtherAmount;relLanguages\n")

###Evaluation by sentence length####
for j in range(3,18):
    size = j
    testTaggedLanguages = []
    testWords = []
    count = 0
    for i in range(len(taggedLanguages)):
        if len(taggedLanguages[i]) == size:
            testWords.append(words[i])
            testTaggedLanguages.append(taggedLanguages[i])
            count  = count +1
    
    predictedTweets = []
    for i in range(len(testWords)):
        prediction = predictWords(lr,testWords[i],bigrams)
        predictedTweets.append(predictedTweet(prediction,testTaggedLanguages[i], words[i]))

    allWords = 0
    allDifferences = 0
    allOthers  = 0
    allLang = 0
    for i in predictedTweets:
        allWords = allWords + i.wordsLeng
        allDifferences= allDifferences + i.differences
        allOthers  = allOthers + i.numberOfOther
        allLang = allLang + i.numberOfLang
    TruePos = allWords-allDifferences
    acc = float(TruePos) / allWords
    relOtherAmount = float(allOthers) / allWords
    relLanguages = float(allLang) / allWords
    f.write(str(size)+";"+str(acc)+";"+str(count)+";"+str(relOtherAmount)+";"+str(relLanguages)+"\n")


f.close()
##################################
##########Print tweets###########
f = open("Results/LR_LabelledTweets.csv","w")
f.write("tweet;correctLabel;predictedLabel\n")
for i in predictedTweets:
	writeMe = ''.join(map(str, i.tweet))+";"
	for j in i.predicted:
		writeMe = writeMe + j + " "
	writeMe = writeMe +";"
	for j in i.actualLanguages:
		writeMe = writeMe + j + " "
	writeMe = writeMe + "\n"
	f.write(writeMe)


f.close()
###############################


##Results with folding##
#unigrams
#Accuracy 0.681329423265
#Mean = 0.674928649324
#Standard deviation = 0.0151458650052

#bigrams
#Accuracy 0.843064071803
#Mean = 0.755262126689
#Standard deviation = 0.0128295537983


