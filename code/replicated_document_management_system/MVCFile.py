import os
import json
myEncoder = lambda o:o.__dict__
class MVCFile:
    def __init__(self):
        # if path==None:
        #     print("expects repository path")
        # self.setRepoPath(path)
        # index = open(path+'/.mvc/index.json','r')
        # self.indexDict = json.load(index)
        # index.close()
        pass
    def setRepoPath(self,path):
        self.repoPath = path
    def status(self):
        pass
    def toJSON(self):
        return json.dumps(self,default=myEncoder,sort_keys=True,indent=4)
    def fromJSON(self,jsonData):
        self.__dict__ = json.loads(jsonData)