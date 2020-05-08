from tme3 import *
import IRModelClass
import parserClass
import indexClass
filepath = ".\\cisi/cisi.txt"

dataCisi = parserClass.Parser(filepath)
textData=[e.getText().replace("\n"," ") for e in dataCisi.dico.values()]
textId=[e.getId() for e in dataCisi.dico.values()]
dictTextCisi={key:value for (key,value) in zip(textId,textData)}

index = indexClass.Index(dicoDocs=dictTextCisi)
dicoIndex, indexInverse = index.index, index.indexInverse
okapi = IRModelClass.Okapi(index,0.75,1.2)


fichierRequetes = "cisi/cisi.qry"
fichierJugements = "cisi/cisi.rel"
query = QueryParser(fichierRequetes,fichierJugements)

acc = Precision(3)
avgAcc = PrecisionMoyenne()
rappel = Rappel(3)
fmesure = FMesure(3)
map = MAP()
rec = ReciprocalRank()
mrr = MRR()
ndcg = NDCG(5)
avgndcg = AVGNDCG(5)

arrayMesuresSingleQuery = [acc,avgAcc,rappel,fmesure,rec,ndcg]
arrayMesuresModele = [map,mrr,avgndcg]
numRequete = 3
querytest = query.getArrayQuery()[numRequete]
arrayQueries = list(query.getArrayQuery().values())
arrayArrayResults=buildResultsFromArrayQueries(okapi,arrayQueries)
print("Mesures sur la requête n°{}:".format(numRequete))
for mes in arrayMesuresSingleQuery:
    mes.displayScore(list(okapi.getRanking(querytest.getText())),querytest)
print("\nMesures de la qualité du modèle:")
for mes in arrayMesuresModele:
    mes.displayScore(arrayArrayResults,arrayQueries)
print("\n")
displayAll3Mesures(okapi,query,3)
bestB, bestk1 = gridSearchPipeline(okapi,index,arrayQueries,3,0.5,1,minB=1,maxB=1.5)