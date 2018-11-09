import json
myEncoder = lambda o:o.__dict__

class User:
    def __init__(self):
        pass
    def setName(self,name):
        self.name = name
    def getName(self):
        return self.name
    def getMasterVersion(self):
        return self.masterVersion
    def setMasterVersion(self,masterVersion):
        self.masterVersion = masterVersion
    def getAccessList(self):
        return self.accessList
    def toJSON(self):
        return json.dumps(self,default=myEncoder,sort_keys=True,indent=4)
    def fromJSON(self,jsonData):
        self.__dict__ = json.loads(jsonData)
