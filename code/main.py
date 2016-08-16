from nltk import tokenize
import pandas as pd
from nGramGenerator import *
import re
import unicodedata
import string


tweets = pd.DataFrame.from_csv('out.tsv', sep='\t', encoding='utf-8')
tweetList = list(tweets['Tweet'])

#to work better with it i split the tweets at every whitespace
splittedtweetList=[] #this will become an array where every tweet is an array of words ("it's" will be a single word yet)
for tweet in tweetList:
    if(tweet >2): # somehow there are empty tweets, those will be filtered out
        #also it is necessary to decode everything, since we have spanish letters
        decodedTweet = unicodedata.normalize('NFKD', tweet).encode('ascii','ignore')
        if(not decodedTweet.find("Not Found")> -1): #some tweets are "Not Found"
            splittedtweetList.append(decodedTweet.split(' '))


NGramGen = nGramGenerator(splittedtweetList)
bigramKeys = NGramGen.getBiOrTriGramsNames(2)
trigramKeys = NGramGen.getBiOrTriGramsNames(3)
