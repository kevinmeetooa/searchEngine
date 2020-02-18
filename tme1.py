import porter
import collections
import math
doc1=" the new home has been saled on top forecasts "
doc2=" the home sales rise in july "
doc3=" there is an increase in home sales in july "
doc4=" july encounter a new home sales rise "
listeDocs=[doc1,doc2,doc3,doc4]
blacklist=["the", "a", "an", "on", "behind", "under", "there", "in", "on"]

def parseWords(listeDocs):
    dicoIndex=dict()
    indexInverse=dict()
    for i in range (len(listeDocs)):
        word=""
        res=[]
        for char in listeDocs[i]:
            if char==" " and len(word)>0:
                if word in blacklist:
                    word=""
                    continue
                word=porter.stem(word)
                res.append(word)
                if word in indexInverse:
                    dicoFreq=indexInverse[word]
                    if i in dicoFreq:
                        dicoFreq[i]=dicoFreq[i]+1
                    else:
                        dicoFreq[i]=1
                    indexInverse[word]=dicoFreq
                else:
                    tempDict=dict()
                    tempDict[i]=1
                    indexInverse[word]=tempDict
                word=""
                continue
            if char!=" ":
                word+=char
        dicoIndex[i]=collections.Counter(res)
    return (dicoIndex,indexInverse)
    
def TFIDF(dicoIndex,indexInverse,numdoc,nbdoc):
    dicotfidf=dict()
    for word in indexInverse:
        idf=math.log((1+nbdoc)/(1+len(indexInverse[word])))
        dicodoc=dicoIndex[numdoc]
        tf=dicodoc[word]
        tfidf=tf*idf
        dicotfidf[word]=tfidf
    return dicotfidf

def getTfsForDoc(dicoIndex,term):
    indexInverse=dict()
    for doc in dicoIndex:
        if term in dicoIndex[doc]:
            indexInverse[doc]=dicoIndex[doc][term]
    return indexInverse

def getTfsForStem(indexInverse,numdoc):
    dicoRes=dict()
    for word in indexInverse:
        if numdoc in indexInverse[word]:
            dicoRes[word]=indexInverse[word][numdoc]
    return dicoRes



    
    
dicoIndex,indexInverse=parseWords(listeDocs)
print(TFIDF(dicoIndex,indexInverse,0,len(listeDocs)))
print(indexInverse)
print(dicoIndex)