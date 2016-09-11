# Code switching detection in multilingual twitter data

Code-switching is the phenomenon by which multilingual speakers switch back and forth between their common languages in written or spoken communication. 

We developed a tool which can automatically annotate words in a sentence to be either english or spanish.
We trained our model on data provided from the *First Workshop on Computational Approaches to Code Switching*, which can be obtained from [EMNLP 2014's website](http://emnlp2014.org/workshops/CodeSwitch/call.html). Due to copyright restrictions, the organisers could not provide the text of the tweets, hence we also developed a tool that parses the offset data format and downloads the actual text. That is thoroughly described in [Data](#Data) and [Preprocessing](#Preprocessing).

The project started as student term project in a Machine learning for computational linguists class at Universitiy of Tuebingen.


## Data

* Download the Spanish-English Training data (11,400 tweets), Test data (3,060 tweets), and Trial data (20 tweets) from http://emnlp2014.org/workshops/CodeSwitch/call.html.  These tab separated files contain the tagging (offset file) with the following coloums: `TweetID`, `UserID`, `Start`, `Stop` and `Language`

* Download the tweeter feetching tool from http://emnlp2014.org/workshops/CodeSwitch/scripts/twitter.zip.
** Usage: `python collect_tweets.py -i <inputFile.tsv> -o <outputFile.tsv>`
** Using en_es_training_offsets.tsv as the input file, we get a "string file" with 3 columns: `TweetID`, `UserID`, and `Tweet`.
** Now we have a file with the tweets (string file from the previous step) and another one with the language annotation for each word (offset file). Both contain the tweetID.

## Preprocessing
After downloading the ofset file and the actual tweets, use our script `read_tweets.py` and set the variables at the top of the script:
* `tweetStringFile` -> string file with the tweets (tsv)
* `tweetOffsetFile` -> offset file with the language annotations (tsv)
* `isTrainingsFile` -> True/False
* `outFile` -> output file 

If needed coloumns are ennumerated. The `fixout_offeset.py` script will delete lots of tweets as they could not be found, were empty, or modified (string is shorter/longer than deffined by the offset file) in the time between annotation and feetching. 

The remaining tweets are processed, resulting in an ouput tsv file with the following columns: `TweetString`, `TweetArray`, and `Languages`:
* `TweetString`: the tweet as normal string
* `TweetArray`: every word separately - the "Start" and "Stop" markers in the offset file tell how
* `Languages`: gives the language for every word according to the offset file

Using that we can create the `UnigramFeatureTable` and `BigramFeatureTable`.

The script `unigrams_word_level.py` fetches all possible unigrams from the string file. These are typed manualy into python scripts to avoid encoding errors. 

The `create_unigram_tables.py` script and `create_bigram_talbes.py` are mostly same. They look up which unigrams (or bigrams as combinations of these unigrams) occure within the words in the training dataset. 

The bigram- and unigram table can are used to train the machine learning algorithm.




 
 
