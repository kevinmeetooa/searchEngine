class Document:
    def __init__(self,id,title="",date="",author="",keywords="",text="",links="",N=""):
        self.id=id
        self.title=title
        self.date=date
        self.author=author
        self.keywords=keywords
        self.text=text
        self.links=links
        self.N=N
        
    def show(self):
        res="id: {}\n"\
        "text: {}\n"\
        "title: {}\n"\
        "date: {}\n"\
        "author: {}\n"\
        "keywords: {}\n"\
        "links: {}\n"\
        "N: {}".format(self.id,self.text,self.title,self.date,self.author,self.keywords,self.links,self.N)
        print(res)

    def getText(self):
        return self.text
    def getId(self):
        return self.id
    def getTitle(self):
        return self.title
    def getDate(self):
        return self.date
    def getAuthor(self):
        return self.author
    def getKeywords(self):
        return self.keywords
    def getLinks(self):
        return self.links
    def getN(self):
        return self.N
