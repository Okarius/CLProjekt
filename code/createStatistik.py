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
def elementToArray(element):
    return element.split(" ")

table = pd.read_csv("data/data.tsv", sep='\t')
languages = [i.split(" ") for i in table["taggedLanguages"]]
languages = [i for i in languages if len(i)> 4]
surrounding = []

for l in languages:
    l.remove("")
    for i in range(1,len(l)-2):
        newList = [l[i-1],l[i],l[i+2]]
    if not "" in newList:
        surrounding.append(newList)
        
        

countChangedWhileSurrounded = 0
notChangedWhileSurroundend = 0
countAll = 0
for i in surrounding:
    if i[0] == i[2]:
        countAll = countAll+1
        if i[0] != i[1]:
            countChangedWhileSurrounded = countChangedWhileSurrounded+1
        if i[0] == i[1]:
            notChangedWhileSurroundend = notChangedWhileSurroundend +1
            
print (float(countChangedWhileSurrounded) /countAll)
print (float(notChangedWhileSurroundend) /countAll)




surrounding = []
languages = [i.split(" ") for i in table["taggedLanguages"]]
languages = [i for i in languages if len(i)> 4]
for l in languages:
    l.remove("")
    newList= []
    newList = [l[len(l)-1],l[len(l)-2],l[len(l)-3]]
    if not "" in newList:
        surrounding.append(newList)


countChangedAtEnd = 0
countNotChangedAtEnd = 0
for i in surrounding:
    if i[0] == i[1]and i[0] == i[2]:
        countChangedAtEnd = countChangedAtEnd+1
    else:        
        countNotChangedAtEnd = countNotChangedAtEnd +1
print ("changed at end")
print (float(countChangedAtEnd) /len(surrounding))
print (float(countNotChangedAtEnd) /len(surrounding))


