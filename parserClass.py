import re
import numpy as np
import document
indexRegex = re.compile("\.I (\d)+")
TRegex=re.compile("\.T\n")
BRegex=re.compile("\.B\n")
ARegex=re.compile("\.A\n")
KRegex=re.compile("\.K\n")
WRegex=re.compile("\.W\n")
XRegex=re.compile("\.X\n")
NRegex=re.compile("\.N\n")
tabRegex = [TRegex,BRegex,ARegex,KRegex,WRegex,XRegex,NRegex,indexRegex]

def initDocumentFromDict(id,dicoAttributes):
    titre=""
    date=""
    auteur=""
    keywords=""
    text=""
    links=""
    N=""
    for key in dicoAttributes:
        if key==0:
            titre=dicoAttributes[key]
        if key==1:
            date=dicoAttributes[key]
        if key==2:
            auteur=dicoAttributes[key]
        if key==3:
            keywords=dicoAttributes[key]
        if key==4:
            text=dicoAttributes[key]
        if key==5:
            links=dicoAttributes[key]
        if key==6:
            N=dicoAttributes[key]
    doc=document.Document(id,titre,date,auteur,keywords,text,links,N)
    return doc


def parse(filepath):
    dicoFinal=dict()
    tabBool=[0,0,0,0,0,0,0,0]
    #filepath="cacm/cacm.txt"
    file=open(filepath,"r")
    i=0
    dicoAttributes=dict()
    buffer=""
    for line in file:
        """if i==200:
            break"""
        if (np.sum(tabBool)==1):
            buffer+=line
        find=re.search(indexRegex,line)
        for ind in range(len(tabRegex)):
            find2=re.search(tabRegex[ind],line) #On cherche si l'on rencontre une des balises
            if find2 is not None:
                try:
                    attribute=tabBool.index(1) #On regarde si on a déjà trouvé une balise (dans ce cas, on peut récupérer l'attribut)
                except ValueError:
                    tabBool[ind]=1
                    continue
                tabBool[attribute]=0
                tabBool[ind]=1 #On marque la balise trouvée
                if (attribute!=7): #Le traitement de la balise .I est effectué séparément
                    l=len(buffer)-len(line)
                    buffer=buffer[:l-1] #On enlève la balise située à la fin de l'attribut
                    dicoAttributes[attribute]=buffer #On place l'attribut dans un dictionnaire
                buffer=""
        if find is not None: #On traite le cas de la balise .I ici
            if len(dicoAttributes)==0: #On rentre dans ce if uniquement lors de la première itération
                currentID=int(line[3:])
                continue
            d=initDocumentFromDict(currentID,dicoAttributes) #On crée un document à partir du dictionnaire d'attributs
            dicoFinal[currentID]=d
            #print("ATTRIBUTES:" +str(dicoAttributes))
            #d.show()
            currentID=int(line[3:])
            dicoAttributes=dict()
        i+=1
    #print("Document #{}: {}".format(currentID,dicoAttributes[0]))
    return dicoFinal

class Parser:
    def __init__(self,filepath):
        self.dico = parse(filepath)
