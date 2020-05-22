from tme2 import weighterClass, IRModelClass
from tme1 import parserClass, indexClass

filepath = "./cisi/cisi.txt"

dataCisi = parserClass.Parser(filepath)
textData=[e.getText().replace("\n"," ") for e in dataCisi.dico.values()]
textId=[e.getId() for e in dataCisi.dico.values()]
dictTextCisi={key:value for (key,value) in zip(textId,textData)}

index = indexClass.Index(dicoDocs=dictTextCisi)
dicoIndex, indexInverse = index.index, index.indexInverse

weighter = weighterClass.TFIDFWeighter(index)
print(weighter.findWord("The relationships between the organization and control of knowledge",3)) #Extrait du texte 3
print(weighter.getWeightsForQuery("testing query for logtfidf weighter testing testing testing"))
print(weighter.getWeightsForDoc(3))
print(weighter.getWeightsForStem("truly"))

okapi = IRModelClass.Okapi(index, 0.75, 1.2)
print(okapi.getScores("The relationships between the organization and control of knowledge"))
print(okapi.getRanking("The relationships between the organization and control of knowledge"))
#Le meilleur document renvoyé par getRanking est le document 3, ce qui est cohérent