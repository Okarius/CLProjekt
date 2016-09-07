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




def getBigramRowToWord(bigrams, word):
    bigramList = []
    for bi in bigrams:
        if bi in word:
            bigramList.append(1)
        else:
            bigramList.append(0)
            
    return bigramList


folder = "data/wordLevelNGrams/nGramTables/"
train_data = pd.read_csv(folder+ 'wordLevelAbsolutBiGramTable.csv', sep='\t')

usefullUnigrams = [".",")","!","@","#","+","-","*","'",":",";","^",">","<","|","(","\"","[","]","…","☆","♡","&","“",",","$","","_","ə","ɛ","ʌ","ʃ",
"á", "é", "í", "ó", "ú","ü","ñ", "¿",
"1","2","3","4","5","6","7","8","9","0",
"a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",
"A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"
]
bigrams =[]
for i in range(len(usefullUnigrams)):
    for j in range(len(usefullUnigrams)):
        bigrams.append(usefullUnigrams[i]+usefullUnigrams[j])

#X_train = train_data[usefullUnigrams]
X_train = train_data[bigrams]

y_train = train_data['label']


lr = LogisticRegression(C=50, penalty='l2', tol= 0.001)
lr.fit(X_train, y_train)
pred = lr.predict([getBigramRowToWord(bigrams,"test")]) 
print pred
#im using cross_validation with 10 folds and 4 jobs parallel (working on 4 cores)
scores= cross_validation.cross_val_score(lr , X_train , y_train, cv=20, n_jobs = 16)
print('Accuracy ' + str(metrics.accuracy_score(y_train, pred)))
print("Mean = "+str(mean(scores)))
print("Standard deviation = "+str(std(scores)))

#unigrams
#Accuracy 0.681329423265
#Mean = 0.674928649324
#Standard deviation = 0.0151458650052

#bigrams
#Accuracy 0.843064071803
#Mean = 0.755262126689
#Standard deviation = 0.0128295537983


