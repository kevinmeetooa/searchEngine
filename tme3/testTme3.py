from tme3 import *
from tme2 import IRModelClass
from tme1 import parserClass, indexClass

jeuDonnees = "cisi" #Remplacer par "cacm" OU "cisi"
print("Jeu de données: {}".format(jeuDonnees))

filepath = ".\\" + jeuDonnees +"/"+ jeuDonnees+".txt"

dataCisi = parserClass.Parser(filepath)
textData=[e.getText().replace("\n"," ") for e in dataCisi.dico.values()]
textId=[e.getId() for e in dataCisi.dico.values()]
dictTextCisi={key:value for (key,value) in zip(textId,textData)}

index = indexClass.Index(dicoDocs=dictTextCisi)
dicoIndex, indexInverse = index.index, index.indexInverse
okapi = IRModelClass.Okapi(index, 0.75, 1.2)


fichierRequetes = jeuDonnees+"/"+jeuDonnees+".qry"
fichierJugements = jeuDonnees+"/"+jeuDonnees+".rel"
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
print("\nCalcul des valeurs moyennes de précision, rappel, f-mesure...")
displayAll3Mesures(okapi,query,50)
print("\nDébut du gridSearch...")
bestB, bestk1 = gridSearchPipeline(okapi,index,arrayQueries,3,0.5,1,minB=1,maxB=1.5)