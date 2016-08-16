import gensim
from gensim.models import word2vec, Phrases
import unicodedata


class nGramGenerator:
    def __init__(self, _allFiles):
            self.allFiles = _allFiles
    

    #return all bi or uni grams
    def getBiOrTriGramsNames(self,nGram):
        allNGrams=[]
        bigram = Phrases(list(self.allFiles))


        for sentences in self.allFiles:
            if nGram == 2:
                nModel =  bigram[sentences]
            elif nGram == 3:
                trigram =Phrases(bigram[list(self.allFiles)])
                nModel = trigram[sentences]
            allNGrams.extend(nModel)
        return (set(allNGrams))

    #long term goal is it to return a table with every tweet and its relative nGram probabilitys
    def getNGramFeatures(self,nGram):
        allNGrams = self.getAllNGramsNames(nGram)
       # return self.getAllRelNGramCount(allNGrams)

        
        
