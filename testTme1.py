import parserClass
import indexClass
filepath = ".\\cisi/cisi.txt"

dataCisi = parserClass.Parser(filepath)
textData=[e.getText().replace("\n"," ") for e in dataCisi.dico.values()]
textId=[e.getId() for e in dataCisi.dico.values()]
dictTextCisi={key:value for (key,value) in zip(textId,textData)}

doc1=" the new home has been saled on top forecasts "
doc2=" the home sales rise in july "
doc3=" there is an increase in home sales in july "
doc4=" july encounter a new home sales rise "
listeDocs=[doc1,doc2,doc3,doc4]

def buildDocCollectionSimple(dataCisi):
    for (k,v) in dataCisi.items():
        print("id: {}, texte: {}".format(v.getId(),v.getText()))


index = indexClass.Index(listeDocs=listeDocs)
dicoIndex, indexInverse = index.index, index.indexInverse
print(indexInverse)
print(dicoIndex)

index2 = indexClass.Index(dicoDocs=dictTextCisi)
dicoIndex, indexInverse = index2.index, index2.indexInverse
print(indexInverse)
print(index2.getStrDoc(3))