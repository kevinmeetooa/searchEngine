#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 14:02:18 2020

@author: 3530508
"""
from tme1 import getTfsForDoc
import math
import collections
import statistics

class Weighter:
    def __init__(self,index,indexInverse):
        self.index=index
        self.indexInverse=indexInverse
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
        return getTfsForDoc(self.index,stem)
    
    def getWeightsForQuery2(self,query):
        dicoRes=dict()
        for doc in self.index:
            dicoTemp=dict()
            for word in query:
                if word in self.index[doc]:
                    dicoTemp[word]=1
                else:
                    dicoTemp[word]=0
            dicoRes[doc]=dicoTemp
        return dicoRes
    
    def getWeightsForQuery(self,query):
        dicoRes=dict()
        for word in query:
            dicoRes[word]=1
        return dicoRes
    
class TFWeighter(Weighter):

        
    def getWeightsForDoc(self,idDoc):
        return self.index[idDoc]
    
    def getWeightsForStem(self,stem):
        return getTfsForDoc(self.index,stem)
    
    def findWord(self,query,doc):
        cpt=0
        for word in query:
            if word in self.index[doc]:
                cpt+=1
        return cpt
    
    def getWeightsForQuery2(self,query):
        dicoRes=dict()
        for doc in self.index:
            dicoTemp=dict()
            for word in query:
                if word in self.index[doc]:
                    dicoTemp[word]=self.index[doc][word]
                else:
                    dicoTemp[word]=0
            dicoRes[doc]=dicoTemp
        return dicoRes
    
    def getWeightsForQuery(self,query):
        dicoRes=dict()
        freq=collections.Counter(query)
        for word in query:
            dicoRes[word]=freq[word]
        return dicoRes
            
class TFIDFWeighter(Weighter):
        
    def getWeightsForDoc(self,idDoc):
        return self.index[idDoc]
    
    def getWeightsForStem(self,stem):
        return getTfsForDoc(self.index,stem)
    
    def findWord(self,query,doc):
        cpt=0
        for word in query:
            if word in self.index[doc]:
                cpt+=1
        return cpt
    
    def getWeightsForQuery2(self,query):
        dicoRes=dict()
        for doc in self.index:
            dicoTemp=dict()
            for word in query:
                idf=math.log((1+len(self.index))/(1+len(self.indexInverse[word])))
                dicoTemp[word]=idf
            dicoRes[doc]=dicoTemp
        return dicoRes
    
    def getWeightsForQuery(self,query):
        dicoRes=dict()
        freq=collections.Counter(query)
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
        dicoRes=dict()
        indexInverse = getTfsForDoc(self.index,stem)
        for doc in self.index:
            if doc in indexInverse:
                dicoRes[doc]=1+math.log(indexInverse[doc])
        return dicoRes
    
    def findWord(self,query,doc):
        cpt=0
        for word in query:
            if word in self.index[doc]:
                cpt+=1
        return cpt
    
    def getWeightsForQuery2(self,query):
        dicoRes=dict()
        for doc in self.index:
            dicoTemp=dict()
            for word in query:
                idf=math.log((1+len(self.index))/(1+len(self.indexInverse[word])))
                dicoTemp[word]=idf
            dicoRes[doc]=dicoTemp
        return dicoRes   

    def getWeightsForQuery(self,query):
        dicoRes=dict()
        freq=collections.Counter(query)
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
        dicoRes=dict()
        indexInverse = getTfsForDoc(self.index,stem)
        for doc in self.index:
            if doc in indexInverse:
                idf=math.log((1+len(self.index))/(1+len(indexInverse)))
                dicoRes[doc]=(1+math.log(indexInverse[doc]))*idf
        return dicoRes
    
    def findWord(self,query,doc):
        cpt=0
        for word in query:
            if word in self.index[doc]:
                cpt+=1
        return cpt
    
    def getWeightsForQuery2(self,query):
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
        return dicoRes      
    
    def getWeightsForQuery(self,query):
        dicoRes=dict()
        freq=collections.Counter(query)
        for word in query:
            if word in self.indexInverse:
                idf=math.log((1+len(self.index))/(1+len(self.indexInverse[word])))
                dicoRes[word]=1+math.log(freq[word])*idf
        return dicoRes


class IRModel:
    def __init__(self,index,indexInverse):
        self.index=index
        self.indexInverse=indexInverse
        
    def getScores(self,query):
        raise NotImplementedError
        
    def getRanking(self,query):
        return {k: v for k, v in sorted(self.getScores(query).items(), key=lambda item: item[1],reverse=True)}
    
    
class Vectoriel(IRModel):
    
    def __init__(self,index,indexInverse,weighter,normalized):
        self.index=index
        self.indexInverse=indexInverse
        self.weighter=weighter
        self.normalized=normalized

    def scoreProdScal(self,query):
        dicoRes=dict()
        arrayQuery = self.weighter.getWeightsForQuery(query)
        for doc in self.index:
            prodScal=0
            arrayDoc=self.weighter.getWeightsForDoc(doc)
            for queryword in arrayQuery:
                if queryword in arrayDoc:
                    prodScal += arrayDoc[queryword]*arrayQuery[queryword]
            dicoRes[doc]=prodScal
        return dicoRes

    def scoreCosinus(self,query):
        dicoRes=dict()
        arrayQuery = self.weighter.getWeightsForQuery(query)
        queryNorm=math.sqrt(sum([term**2 for term in arrayQuery.values()]))
        for doc in self.index:
            prodScal=0
            arrayDoc=self.weighter.getWeightsForDoc(doc)
            for queryword in arrayQuery:
                if queryword in arrayDoc:
                    prodScal += arrayDoc[queryword]*arrayQuery[queryword]
            norm=self.weighter.dicoNormes[doc]*queryNorm
            dicoRes[doc]=prodScal/norm
        return dicoRes
    
    def getScores(self,query): #Slmt sur les documents qui contiennent les termes de la requête
        if self.normalized:
            return self.scoreCosinus(query)
        return self.scoreProdScal(query)

class ModeleLangue(IRModel):
    def __init__(self,index,indexInverse,lmbda):
        self.index=index
        self.indexInverse=indexInverse
        self.lmbda=lmbda

    def getScores(self,query):
        dicoRes=dict()
        for doc in self.index:
            proba=1
            for word in query:
                if word in self.indexInverse:
                    tfWord = sum(self.indexInverse[word].values())
                    totalTf = sum([sum(e.values()) for e in self.indexInverse.values()])
                    probaCollection=tfWord/totalTf
                    if doc in self.indexInverse[word]:
                        tfWordDoc=self.indexInverse[word][doc]
                        docLength=sum(self.index[doc].values())
                        probaDoc=tfWordDoc/docLength
                    else:
                        continue
                    proba *= (1-self.lmbda)*probaDoc + self.lmbda*probaCollection
            dicoRes[doc] = proba
        return dicoRes

class Okapi(IRModel):
    def __init__(self,index,indexInverse,b,k1):
        self.index=index
        self.indexInverse=indexInverse
        self.b=b
        self.k1=k1

    def getScores(self,query):
        dicoRes = dict()
        dAvg = statistics.mean([sum(e.values()) for e in self.indexInverse.values()])
        for doc in self.index:
            total=0
            for word in query:
                if word not in self.indexInverse:
                    continue
                nbDocsContainingWord = len(self.indexInverse[word])
                idf = math.log((len(self.index)-nbDocsContainingWord+0.5)/(nbDocsContainingWord+0.5))
                if doc in self.indexInverse[word]:
                    tf = self.indexInverse[word][doc]
                else:
                    continue
                numerateur = tf * (self.k1+1)
                denominateur = tf + self.k1 * (1-self.b+self.b*(sum(self.index[doc].values())/dAvg))
                print("word: {} -- numerateur/denominateur for doc {}: {} and {} ".format(word, doc, numerateur,denominateur))
                total += (idf*numerateur)/denominateur
            dicoRes[doc] = total
        return dicoRes