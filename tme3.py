import re
import time
import numpy as np
import math
from statistics import mean
from weighterClass import queryPreprocessing
from IRModelClass import Okapi

spaceRegex=re.compile("\s+(\d+)\s+(\d+)")
indexRegex = re.compile("\.I (\d)+")
TRegex=re.compile("\.T\n")
BRegex=re.compile("\.B\n")
ARegex=re.compile("\.A\n")
KRegex=re.compile("\.K\n")
WRegex=re.compile("\.W\n")
XRegex=re.compile("\.X\n")
NRegex=re.compile("\.N\n")
tabRegex = [TRegex,BRegex,ARegex,KRegex,WRegex,XRegex,NRegex,indexRegex]
class Query:
    def __init__(self,id,text,listeDocs):
        self.id=id
        self.text=text
        self.listeDocs=listeDocs

    def getId(self):
        return self.id

    def getText(self):
        return self.text

    def getListeDocs(self):
        return self.listeDocs

class QueryParser:
    def __init__(self,fichierRequetes,fichierJugements):
        self.fichierRequetes=fichierRequetes
        self.fichierJugements=fichierJugements

    def getArrayQuery(self):
        file = open(self.fichierJugements, "r")
        dicoRes = dict()
        for line in file:
            find = spaceRegex.match(line)
            doc = int(find.group(1))
            res = int(find.group(2))
            if doc in dicoRes:
                dicoRes[doc].append(res)
            else:
                dicoRes[doc] = [res]
        dicoFinal = dict()
        tabBool = [0, 0, 0, 0, 0, 0, 0, 0]
        # filepath="cacm/cacm.txt"
        file = open(self.fichierRequetes, "r")
        i = 0
        dicoAttributes = dict()
        buffer = ""
        for line in file:
            """if i==200:
                break"""
            if (np.sum(tabBool) == 1):
                buffer += line
            find = re.search(indexRegex, line)
            for ind in range(len(tabRegex)):
                find2 = re.search(tabRegex[ind], line)  # On cherche si l'on rencontre une des balises
                if find2 is not None:
                    try:
                        attribute = tabBool.index(
                            1)  # On regarde si on a déjà trouvé une balise (dans ce cas, on peut récupérer l'attribut)
                    except ValueError:
                        tabBool[ind] = 1
                        continue
                    tabBool[attribute] = 0
                    tabBool[ind] = 1  # On marque la balise trouvée
                    if (attribute != 7):  # Le traitement de la balise .I est effectué séparément
                        l = len(buffer) - len(line)
                        buffer = buffer[:l - 1]  # On enlève la balise située à la fin de l'attribut
                        dicoAttributes[attribute] = buffer  # On place l'attribut dans un dictionnaire
                    buffer = ""
            if find is not None:  # On traite le cas de la balise .I ici
                if len(dicoAttributes) == 0:  # On rentre dans ce if uniquement lors de la première itération
                    currentID = int(line[3:])
                    continue
                if currentID in dicoRes:
                    qry = Query(currentID,dicoAttributes[4],dicoRes[currentID])
                    dicoFinal[currentID] = qry
                    # print("ATTRIBUTES:" +str(dicoAttributes))
                    # d.show()
                currentID = int(line[3:])
                dicoAttributes = dict()
            i += 1
        # print("Document #{}: {}".format(currentID,dicoAttributes[0]))
        return dicoFinal


class EvalMesure:
    def evalQuery(self,liste,query):
        raise NotImplementedError

    def displayScore(self,liste,query):
        print("{} score: {}".format(self.__class__.__name__,self.evalQuery(liste,query)))

class Precision(EvalMesure):
    def __init__(self,k):
        self.k=k
    def evalQuery(self,liste,query):
        listeDocs=query.getListeDocs()
        cpt=0
        for i in range (min(len(liste),self.k)):
            if liste[i] in listeDocs:
                cpt+=1
        return cpt/self.k #Proportion de documents pertinents au rang k

class Rappel(EvalMesure):
    def __init__(self,k):
        self.k=k
    def evalQuery(self,liste,query):
        listeDocs=query.getListeDocs()
        #print("List of relevant docs: {}".format(listeDocs))
        #print("Argument list: {}".format(liste))
        cpt=0
        for i in range (min(len(liste),self.k)):
            if liste[i] in listeDocs:
                cpt+=1
        return cpt/len(listeDocs) #On divise par le nombre de documents pertinents

class FMesure(EvalMesure):
    def __init__(self,k):
        self.k=k
    def evalQuery(self,liste,query):
        precision=Precision(self.k)
        precisionScore=precision.evalQuery(liste,query)
        rappel=Rappel(self.k)
        rappelScore=rappel.evalQuery(liste,query)
        if precisionScore+rappelScore==0:
            return 0
        return (2*precisionScore*rappelScore)/(precisionScore+rappelScore)

class PrecisionMoyenne(EvalMesure):
    def __init__(self):
        pass
    def evalQuery(self,liste,query):
        listeDocs=query.getListeDocs()
        #print("List of relevant docs: {}".format(listeDocs))
        #print("Argument list: {}".format(liste))
        cpt=0
        i=0
        n=len(listeDocs)
        precisionArray=[]
        while (i<len(liste)):
            if (len(precisionArray) == len(listeDocs)):
                break
            currentDoc = liste[i]
            if currentDoc in listeDocs:
                precision = Precision(i+1)
                precisionScore = precision.evalQuery(liste,query)
                precisionArray.append(precisionScore)
            i += 1
        #print(precisionArray)
        return mean(precisionArray)

class MAP(EvalMesure):
    def __init__(self):
        pass
    def evalQuery(self, arrayArrayResults, arrayQueries):
        precisionMoy = PrecisionMoyenne()
        avgPrecArray=[]
        if (len(arrayArrayResults) != len(arrayQueries)):
            print("Erreur MAP: les 2 listes n'ont pas les mêmes dimensions")
            return
        for i in range (len(arrayQueries)):
            currentAvgPrec = precisionMoy.evalQuery(arrayArrayResults[i],arrayQueries[i])
            avgPrecArray.append(currentAvgPrec)
        #print(avgPrecArray)
        return mean(avgPrecArray)

class ReciprocalRank(EvalMesure):
    def __init__(self):
        pass
    def evalQuery(self,liste,query):
        listeDocs=query.getListeDocs()
        #print("List of relevant docs: {}".format(listeDocs))
        #print("Argument list: {}".format(liste))
        cpt=0
        i=0
        n=len(listeDocs)
        precisionArray=[]
        while (i<len(liste)):
            currentDoc = liste[i]
            if currentDoc in listeDocs:
                return 1/(i+1)
            i += 1
        return 0

class MRR(EvalMesure):
    def __init__(self):
        pass
    def evalQuery(self, arrayArrayResults, arrayQueries):
        recRank = ReciprocalRank()
        recRankArray=[]
        if (len(arrayArrayResults) != len(arrayQueries)):
            print("Erreur MAP: les 2 listes n'ont pas les mêmes dimensions")
            return
        for i in range (len(arrayQueries)):
            currentRecRank = recRank.evalQuery(arrayArrayResults[i],arrayQueries[i])
            recRankArray.append(currentRecRank)
        #print(recRankArray)
        return mean(recRankArray)

class NDCG(EvalMesure):
    def __init__(self,p):
        self.p=p

    def evalQuery(self,liste,query):
        listeDocs=query.getListeDocs()
        #print("List of relevant docs: {}".format(listeDocs))
        #print("Argument list: {}".format(liste))
        somme=0
        IDCG=0
        for i in range (min(self.p,len(liste))):
            IDCG += 1 / math.log2(i + 2)
            doc =  liste[i]
            if doc in listeDocs:
                somme += 1/math.log2(i+2)
        return somme/IDCG

class AVGNDCG(EvalMesure):
    def __init__(self,p):
        self.p=p

    def evalQuery(self, arrayArrayResults, arrayQueries):
        ndcg = NDCG(self.p)
        ndcgArray=[]
        if (len(arrayArrayResults) != len(arrayQueries)):
            print("Erreur MAP: les 2 listes n'ont pas les mêmes dimensions")
            return
        for i in range (len(arrayQueries)):
            currentndcg = ndcg.evalQuery(arrayArrayResults[i],arrayQueries[i])
            ndcgArray.append(currentndcg)
        #print(ndcgArray)
        return mean(ndcgArray)


def buildResultsFromArrayQueries(modele,arrayQueries):
    res=[]
    for query in arrayQueries:
        #print("Id: {}".format(query.getId()))
        result=list(modele.getRanking(queryPreprocessing(query.getText())))
        res.append(result)
    return res

def displayAll3Mesures(modele,qp,k):
    #qp = QueryParser("cisi/cisi.qry", "cisi/cisi.rel")
    res = qp.getArrayQuery()
    precision=Precision(k)
    rappel=Rappel(k)
    fmes=FMesure(k)
    precisionArray=[]
    rappelArray=[]
    FMesureArray=[]
    for elt in res.values():
        query=elt.getText()
        listeDocs=elt.getListeDocs()
        arrayReturned = list(modele.getRanking(queryPreprocessing(query)))[:k]
        precisionArray.append(precision.evalQuery(arrayReturned,elt))
        rappelArray.append(rappel.evalQuery(arrayReturned, elt))
        FMesureArray.append(fmes.evalQuery(arrayReturned,elt))
    print("Precision: {}\nRappel: {}\nF-Mesure: {}".format(mean(precisionArray),mean(rappelArray),mean(FMesureArray)))


def gridSearchPipeline(modele,index,arrayQueries,pas,minA,maxA,minB=0,maxB=1):
    dicoIndex = index.index
    indexInverse = index.indexInverse
    map=MAP()
    modele = modele.__class__.__name__
    """print(minA)
    print(maxA)
    print(pas)"""
    arrayA=np.linspace(minA,maxA,pas)
    arrayB=np.linspace(minB,maxB,pas)
    """print(arrayA)
    print(arrayB)"""
    bestA=-1
    bestB=-1
    bestScore=0
    arrayScores=[]
    if modele=="Okapi":
        #print("Enter")
        for parametreA in arrayA:
            for parametreB in arrayB:
                modele=Okapi(index,parametreA,parametreB)
                arrayArrayResults=buildResultsFromArrayQueries(modele,arrayQueries)
                currentMAP=map.evalQuery(arrayArrayResults,arrayQueries)
                print("MAP pour b: {} et k1: {} = {}".format(parametreA,parametreB,currentMAP))
                arrayScores.append(currentMAP)
                if currentMAP>bestScore:
                    bestA=parametreA
                    bestB=parametreB
                    bestScore=currentMAP
        print("Meilleur b: {}\nMeilleur k1: {}\nMeilleur score: {}".format(bestA,bestB,bestScore))
        #print(arrayScores)
        return (bestA,bestB)