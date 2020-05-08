import statistics
import math
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

class IRModel:
    def __init__(self, index):
        self.index = index.index
        self.indexInverse = index.indexInverse

    def getScores(self, query):
        raise NotImplementedError

    def getRanking(self, query):
        return {k: v for k, v in sorted(self.getScores(query).items(), key=lambda item: item[1], reverse=True)}

class Vectoriel(IRModel):
    def __init__(self, index, weighter, normalized):
        self.index = index.index
        self.indexInverse = index.indexInverse
        self.weighter = weighter
        self.normalized = normalized

    def scoreProdScal(self, query):
        dicoRes = dict()
        arrayQuery = self.weighter.getWeightsForQuery(query)
        for doc in self.index:
            prodScal = 0
            arrayDoc = self.weighter.getWeightsForDoc(doc)
            for queryword in arrayQuery:
                if queryword in arrayDoc:
                    prodScal += arrayDoc[queryword] * arrayQuery[queryword]
            dicoRes[doc] = prodScal
        return dicoRes

    def scoreCosinus(self, query):
        dicoRes = dict()
        arrayQuery = self.weighter.getWeightsForQuery(query)
        queryNorm = math.sqrt(sum([term ** 2 for term in arrayQuery.values()]))
        for doc in self.index:
            prodScal = 0
            arrayDoc = self.weighter.getWeightsForDoc(doc)
            for queryword in arrayQuery:
                if queryword in arrayDoc:
                    prodScal += arrayDoc[queryword] * arrayQuery[queryword]
            norm = self.weighter.dicoNormes[doc] * queryNorm
            if (prodScal == 0 or norm == 0):
                dicoRes[doc] = 0
            else:
                dicoRes[doc] = prodScal / norm
        return dicoRes

    def getScores(self, query):  # Slmt sur les documents qui contiennent les termes de la requête
        if self.normalized:
            return self.scoreCosinus(query)
        return self.scoreProdScal(query)


class ModeleLangue(IRModel):
    def __init__(self, index , lmbda):
        self.index = index.index
        self.indexInverse = index.indexInverse
        self.lmbda = lmbda
        self.totalTf = sum([sum(e.values()) for e in self.indexInverse.values()])

    def getScores(self, query):
        query = queryPreprocessing(query)
        dicoRes = dict()
        for doc in self.index:
            proba = 1
            for word in query:
                if word in self.indexInverse:
                    tfWord = sum(self.indexInverse[word].values())
                    probaCollection = tfWord / self.totalTf
                    if doc in self.indexInverse[word]:
                        tfWordDoc = self.indexInverse[word][doc]
                        docLength = sum(self.index[doc].values())
                        probaDoc = tfWordDoc / docLength
                    else:
                        continue
                    proba *= (1 - self.lmbda) * probaDoc + self.lmbda * probaCollection
            dicoRes[doc] = proba
        return dicoRes


class Okapi(IRModel):
    def __init__(self, index , b, k1):
        self.index = index.index
        self.indexInverse = index.indexInverse
        self.b = b
        self.k1 = k1
        #print("Initialisation avec b: {} et k1: {}".format(b,k1))
        self.dAvg = statistics.mean([sum(e.values()) for e in self.indexInverse.values()])

    def getScores(self, query):
        query = queryPreprocessing(query)
        dicoRes = dict()
        for doc in self.index:
            total = 0
            for word in query:
                if word not in self.indexInverse:
                    continue
                nbDocsContainingWord = len(self.indexInverse[word])
                idf = math.log((len(self.index) - nbDocsContainingWord + 0.5) / (nbDocsContainingWord + 0.5))
                if doc in self.indexInverse[word]:
                    tf = self.indexInverse[word][doc]
                else:
                    continue
                numerateur = idf * tf * (self.k1 + 1)
                denominateur = tf + self.k1 * (1 - self.b + self.b * (sum(self.index[doc].values()) / self.dAvg))
                total += numerateur / denominateur
            dicoRes[doc] = total
        return dicoRes