1. Download the Data from : 
http://emnlp2014.org/workshops/CodeSwitch/call.html


2. 
Download:
Spanish-English Training data (11,400 tweets)
en_es_training_offsets.tsv contains the tagging (OffsetFile) 

Spanish-English Test data (3,060 tweets)

Spanish-English Trial data (20 tweets)
This Tsv contains:
TweetID		UserID		Start		Stop		Language
!!!!!!!(add "tweetId	userId	start	end	label" as first row)!!!!!!!


3.
Download:
emnlp2014.org/workshops/CodeSwitch/scripts/twitter.zip
contains collect_tweets.py
This is used via:
python collect_tweets.py -i <inputFile.tsv> -o <outputFile.tsv>



Using the en_es_training_offsets.tsv will produce a .tsv file.  (StringFile)
The columns are:
TweetID 	UserID		Tweet
!!!!!!!((add  tweetId	userId		tweet as first row)!!!!!!!

Now we have a File with the Tweets (step3) and one which shows the language for each word (step2)


4.
User our Script:  "readTweets.py"
set the File names at the top of the script:
outFile -> Output
tweetStringFile -> tsv with the tweets
tweetOffsetFile -> tsv with the languages
isTrainingsFile = True/False


This Script tranforms the two provided files to a tsv file with the following columns:
TweetString	TweetArray	Languages

TweetString the tweet as normal string
TweetArray every word sepparated. The Start Stop markers in the "offsetFile.tsv" tell how.
Languages gives the languages for every word. The which language is taken is given in the "offsetFile.tsv". 


First off all deletes this file a lot of tweets:
They could be "Not Found", "Empty", String is shorter/longer than in the offset file, It could happen that the offset file has more / less words than the actual tweets.

The remaining tweets get be processed as follows:
Offset and String file both contain the TweetId.
I pick the TweetID from the StringFile. Lookup every corresponding row in the OffSetFile. Create an tweet and language array. Those will be put in the table.
That way i have for every tweetID the string, word-array and the language-array. 



5. use the script unigramsWordLevel.py this will create all unigrams from the StringFile
Those are late typed manualy into python scripts since otherwise it thors encoding errors.


6.
Create the UnigramFeatureTable and BigramFeatureTable.

The createBigramTables.py and createUniGramTalbes.py are mostly the same script.
They search every used word (using the processed File from step4).
Then they will look up if the bigrams/unigrams occure in the word. The results gets insert into a table.



Stepts 1-6 (except 4) are necessary to perform for the trainings- and test-data


7.
Use the bigram- /unigramtable to train the machine learning algorithm.




 
 
