import pandas as pd
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('utf-8')

tweets = pd.read_csv('data/outOffset.tsv', sep='\t', encoding='utf-8')
tweetStrings = []
unigrams = set()
for i in range(len(tweets)):
    tweet = str(tweets["tweet"][i]).decode("utf-8")
    if "Not Found" not in tweet: #some tweets are Not Found
        unigrams = unigrams | set(tweet)
        
        
unigramsList = list(unigrams)
f = open("unigramsWordLevel.txt", "w")
for i in range(len(unigrams)):
    f.write(unigrams.pop()+ "\n")
f.close()


f = open("bigramsWordLevel.txt", "w")
for u in unigramsList:
    for utwo in unigramsList:
        f.write( u + utwo + "\n")
f.close()




f = open("trigramsWordLevel.txt", "w")
for u in unigramsList:
    for utwo in unigramsList:
            for uthree in unigramsList:
                f.write( u + utwo + uthree + "\n")
f.close()