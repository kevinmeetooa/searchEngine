from parserClass import parse
dataCisi=parse(".\\cisi/cisi.txt")
textData=[e.getText().replace("\n"," ") for e in dataCisi.values()]
textId=[e.getId() for e in dataCisi.values()]
dictTextCisi={key:value for (key,value) in zip(textId,textData)}