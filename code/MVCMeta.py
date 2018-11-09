import os
import json
import time
myEncoder = lambda o:o.__dict__
class MVCMeta:
    def __init__(self,databaseName,repoPath=None):
        self.repoPath = repoPath
        self.databaseName = databaseName
        self.currentVersion = 0
        self.previousVersion = 0
        self.latestVersion = 0
        self.isStageOccupied = False
        self.isStatusCheckDone = False
        self.isReverted = False
        self.isRevertedFrom = None
        self.versionList = []
        self.versions = 0
        self.modifiedFiles = {}
        self.localTimeOfCreation = None
    def updateMeta(self):
        pass
    def setRepoPath(self,path):
        self.repoPath = path
    def createMetaData(self):
        os.mkdir(self.repoPath+'/.mvc',0o777)
        os.mkdir(self.repoPath+'/.mvc/stage',0o777)
        os.mkdir(self.repoPath+'/.mvc/master',0o777)
        os.mkdir(self.repoPath+'/.mvc/user',0o777)
        os.mkdir(self.repoPath+'/.mvc/temp',0o777)
        os.mkdir(self.repoPath+'/.mvc/temp/cVUnmodifiedFiles',0o777)
        m = open(self.repoPath+'/.mvc/index.json','w+')
        self.localTimeOfCreation = time.asctime(time.localtime(time.time()))
        m.write(self.toJSON())
        m.close()
    def toJSON(self):
        return json.dumps(self,default=myEncoder,indent=4)
    def fromJSON(self,jsonData):
        self.__dict__ = json.loads(jsonData)