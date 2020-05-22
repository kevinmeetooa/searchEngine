#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 14:02:18 2020

@author: 3530508
"""
import math
import collections
import statistics
import porter

def queryPreprocessing(query):
    """
    Preprocess d'une query sous forme de string pour renvoyer un tableau de mots
    """
    arrayQuery = "".join(c for c in query if c.isalnum() or c.isspace()).split()
    #print(arrayQuery)
    res=[]
    for word in arrayQuery:
        word = porter.stem(word.lower()) #On stem les mots car ils sont stemmés dans l'index
        res.append(word)
    return res


class Weighter:

    def __init__(self,index):
        self.index=index.index
        self.indexInverse=index.indexInverse
        self.indexObject=index
        self.initDocNorm()
        
    def getWeightsForDoc(self,idDoc):
        raise NotImplementedError

    def getWeightsForStem(self,stem):
        raise NotImplementedError
    
    def getWeightsForQuery(self,query):
        raise NotImplementedError

    def initDocNorm(self):
        self.dicoNormes=dict()
        for doc in self.index:
            wordWeights=self.getWeightsForDoc(doc).values()
            norm=sum([word**2 for word in wordWeights])
            norm=math.sqrt(norm)
            self.dicoNormes[doc]=norm

class BinaryWeighter(Weighter):

    def getWeightsForDoc(self,idDoc):
        return self.index[idDoc]
    
    def getWeightsForStem(self,stem):
        stem = porter.stem(stem.lower())
        return self.indexObject.getTfsForDoc(stem)
    
    """def getWeightsForQuery2(self,query):
        dicoRes=dict()
        for doc in self.index:
            dicoTemp=dict()
            for word in query:
                if word in self.index[doc]:
                    dicoTemp[word]=1
                else:
                    dicoTemp[word]=0
            dicoRes[doc]=dicoTemp
        return dicoRes"""
    
    def getWeightsForQuery(self,query):
        query = queryPreprocessing(query)
        dicoRes=dict()
        for word in query:
            dicoRes[word]=1
        return dicoRes
    
class TFWeighter(Weighter):

    def getWeightsForDoc(self,idDoc):
        return self.index[idDoc]
    
    def getWeightsForStem(self,stem):
        stem = porter.stem(stem.lower())
        return self.indexObject.getTfsForDoc(stem)
    
    def findWord(self,query,doc):
        query = queryPreprocessing(query)
        cpt=0
        for word in query:
            if word in self.index[doc]:
                cpt+=1
        return cpt
    
    """def getWeightsForQuery2(self,query):
        dicoRes=dict()
        for doc in self.index:
            dicoTemp=dict()
            for word in query:
                if word in self.index[doc]:
                    dicoTemp[word]=self.index[doc][word]
                else:
                    dicoTemp[word]=0
            dicoRes[doc]=dicoTemp
        return dicoRes"""
    
    def getWeightsForQuery(self,query):
        query = queryPreprocessing(query)
        dicoRes=dict()
        freq=collections.Counter(query)
        for word in query:
            dicoRes[word]=freq[word]
        return dicoRes
            
class TFIDFWeighter(Weighter):
        
    def getWeightsForDoc(self,idDoc):
        return self.index[idDoc]
    
    def getWeightsForStem(self,stem):
        stem = porter.stem(stem.lower())
        return self.indexObject.getTfsForDoc(stem)
    
    def findWord(self,query,doc):
        query = queryPreprocessing(query)
        cpt=0
        for word in query:
            if word in self.index[doc]:
                cpt+=1
        return cpt
    
    """def getWeightsForQuery2(self,query):
        dicoRes=dict()
        for doc in self.index:
            dicoTemp=dict()
            for word in query:
                idf=math.log((1+len(self.index))/(1+len(self.indexInverse[word])))
                dicoTemp[word]=idf
            dicoRes[doc]=dicoTemp
        return dicoRes"""
    
    def getWeightsForQuery(self,query):
        query = queryPreprocessing(query)
        dicoRes=dict()
        for word in query:
            if word in self.indexInverse:
                idf=math.log((1+len(self.index))/(1+len(self.indexInverse[word])))
                dicoRes[word]=idf
        return dicoRes
    
class logTFWeighter(Weighter):
        
    def getWeightsForDoc(self,idDoc):
        dicoRes=dict()
        index=self.index[idDoc]
        for word in index:
            dicoRes[word]=1+math.log(index[word])
        return dicoRes
    
    def getWeightsForStem(self,stem):
        stem = porter.stem(stem.lower())
        dicoRes=dict()
        indexInverse = self.indexObject.getTfsForDoc(stem)
        for doc in self.index:
            if doc in indexInverse:
                dicoRes[doc]=1+math.log(indexInverse[doc])
        return dicoRes
    
    def findWord(self,query,doc):
        query = queryPreprocessing(query)
        cpt=0
        for word in query:
            if word in self.index[doc]:
                cpt+=1
        return cpt
    
    """def getWeightsForQuery2(self,query):
        dicoRes=dict()
        for doc in self.index:
            dicoTemp=dict()
            for word in query:
                idf=math.log((1+len(self.index))/(1+len(self.indexInverse[word])))
                dicoTemp[word]=idf
            dicoRes[doc]=dicoTemp
        return dicoRes  """

    def getWeightsForQuery(self,query):
        query = queryPreprocessing(query)
        dicoRes=dict()
        for word in query:
            if word in self.indexInverse:
                idf=math.log((1+len(self.index))/(1+len(self.indexInverse[word])))
                dicoRes[word]=idf
        return dicoRes            

class logTFIDFWeighter(Weighter):
        
    def getWeightsForDoc(self,idDoc):
        dicoRes=dict()
        index=self.index[idDoc]
        for word in index:
            idf=math.log((1+len(self.index))/(1+len(self.indexInverse[word])))
            dicoRes[word]=(1+math.log(index[word]))*idf
        return dicoRes
    
    def getWeightsForStem(self,stem):
        stem =  porter.stem(stem.lower())
        dicoRes=dict()
        indexInverse = self.indexObject.getTfsForDoc(stem)
        for doc in self.index:
            if doc in indexInverse:
                idf=math.log((1+len(self.index))/(1+len(indexInverse)))
                dicoRes[doc]=(1+math.log(indexInverse[doc]))*idf
        return dicoRes
    
    def findWord(self,query,doc):
        query = queryPreprocessing(query)
        cpt=0
        for word in query:
            if word in self.index[doc]:
                cpt+=1
        return cpt
    
    """def getWeightsForQuery2(self,query):
        dicoRes=dict()
        for doc in self.index:
            dicoTemp=dict()
            for word in query:
                idf=math.log((1+len(self.index))/(1+len(self.indexInverse[word])))
                if word in self.index[doc]:
                    dicoTemp[word]=self.index[doc][word]*idf
                else:
                    dicoTemp[word]=0
            dicoRes[doc]=dicoTemp
        return dicoRes """
    
    def getWeightsForQuery(self,query):
        query = queryPreprocessing(query)
        dicoRes=dict()
        freq=collections.Counter(query)
        for word in query:
            if word in self.indexInverse:
                idf=math.log((1+len(self.index))/(1+len(self.indexInverse[word])))
                dicoRes[word]=1+math.log(freq[word])*idf
        return dicoRes

