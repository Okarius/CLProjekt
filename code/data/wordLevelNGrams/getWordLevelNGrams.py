import pandas as pd
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('utf-8')
#This file is used to get all unigrams
#since there are a lot of funny special characters
#i just tapped them in the file i needed them to prevent coding errors

tweets = pd.read_csv('../trainingsTweets.tsv', sep='\t', encoding='utf-8')
tweetStrings = []
unigrams = set()
for i in range(len(tweets)):
    tweet = str(tweets["tweet"][i]).decode("utf-8")
    if "Not Found" not in tweet: #some tweets are Not Found
        unigrams = unigrams | set(tweet)


f = open("unigramsWordLevel.txt","r")
unigrams = f.readlines()
unigrams =[i.replace("\n","") for i in unigrams]
f.close()

