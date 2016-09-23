#Some tweets are invalid since they are not found or null
#those get deleted

import pandas as pd
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('utf-8')
tweets = pd.read_csv('outOffsetCOPY.tsv', sep='\t', encoding='utf-8')
tweetsInfo = pd.read_csv('en_es_training_offsetsCOPY.tsv', sep='\t', encoding='utf-8')

        
tweets =  tweets[pd.isnull(tweets["tweet"]) == False]       
tweets =  tweets[tweets["tweet"] != "Not Found"]       


tweets.to_csv("tweetsStringData.tsv", sep='\t')
