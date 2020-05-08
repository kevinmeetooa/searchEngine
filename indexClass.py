import porter
import collections
import math
import re
punctuationRegex = re.compile('[^a-zA-Z0-9]')
blacklist = ["the", "a", "an", "on", "behind", "under", "there", "in", "on"]

def parseWords(listeDocs):
    dicoIndex = dict()
    indexInverse = dict()
    for i in range(len(listeDocs)):
        word = ""
        res = []
        for char in listeDocs[i]:
            if char == " " and len(word) > 0:
                if word in blacklist:
                    word = ""
                    continue
                word = porter.stem(word)
                res.append(word)
                if word in indexInverse:
                    dicoFreq = indexInverse[word]
                    if i in dicoFreq:
                        dicoFreq[i] = dicoFreq[i] + 1
                    else:
                        dicoFreq[i] = 1
                    indexInverse[word] = dicoFreq
                else:
                    tempDict = dict()
                    tempDict[i] = 1
                    indexInverse[word] = tempDict
                word = ""
                continue
            if char != " ":
                word += char
        dicoIndex[i] = collections.Counter(res)
    return (dicoIndex, indexInverse)


def parseWordsFromDict(dicoDocs):
    dicoIndex = dict()
    indexInverse = dict()
    for elt in dicoDocs:
        word = ""
        res = []
        for char in dicoDocs[elt]:
            if char == " " and len(word) > 0:
                if word in blacklist:
                    word = ""
                    continue
                word = porter.stem(word.lower())
                word = punctuationRegex.sub("", word)
                res.append(word)
                if word in indexInverse:
                    dicoFreq = indexInverse[word]
                    if elt in dicoFreq:
                        dicoFreq[elt] = dicoFreq[elt] + 1
                    else:
                        dicoFreq[elt] = 1
                    indexInverse[word] = dicoFreq
                else:
                    tempDict = dict()
                    tempDict[elt] = 1
                    indexInverse[word] = tempDict
                word = ""
                continue
            if char != " ":
                word += char
        dicoIndex[elt] = collections.Counter(res)
    return (dicoIndex, indexInverse)


class Index:
    def __init__(self, listeDocs=None, dicoDocs=None):
        self.dicoDocs = dicoDocs
        if dicoDocs==None:
            index, indexInverse = parseWords(listeDocs)
            self.index = index
            self.indexInverse = indexInverse
        else:
            index, indexInverse = parseWordsFromDict(dicoDocs)
            self.index = index
            self.indexInverse = indexInverse


    def TFIDF(self, numdoc, nbdoc):
        dicoIndex, indexInverse = self.index, self.indexInverse
        dicotfidf = dict()
        for word in indexInverse:
            idf = math.log((1 + nbdoc) / (1 + len(indexInverse[word])))
            dicodoc = dicoIndex[numdoc]
            tf = dicodoc[word]
            tfidf = tf * idf
            dicotfidf[word] = tfidf
        return dicotfidf

    def getTfsForDoc(self, term):
        dicoIndex = self.index
        indexInverse = dict()
        for doc in dicoIndex:
            if term in dicoIndex[doc]:
                indexInverse[doc] = dicoIndex[doc][term]
        return indexInverse

    def getTfsForStem(self, numdoc):
        indexInverse = self.indexInverse
        dicoRes = dict()
        for word in indexInverse:
            if numdoc in indexInverse[word]:
                dicoRes[word] = indexInverse[word][numdoc]
        return dicoRes

    def getStrDoc(self,numDoc):
        if self.dicoDocs is not None:
            return self.dicoDocs[numDoc]


