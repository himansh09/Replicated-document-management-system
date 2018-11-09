'''
diffoscope is package available at diffoscope.org under GPLv3. diffoscope is used to calculate the diff of two text
files and generate html/text output
'''
import json
import os
import shutil
import hashlib
import difflib
import io
import sys
import subprocess
import shlex
import pprint
import gzip
# from classes import diff_match_patch as gdmp
from classes.MVCFile import MVCFile
from classes.MVCMeta import MVCMeta
myEncoder = lambda o:o.__dict__


DELETE_COLOR = u'\u001b[31m' # red test background transparent
ADD_COLOR = '\u001b[32m'
NEW_COLOR = ''
MODIFIED_COLOR = u'\u001b[33m' #  yellow text background transparent
COLOR_RESET = u'\u001b[0m'


class MVC:

    def __init__(self,repoPath='.'):
        fListCwd = os.listdir(repoPath)
        fListCwd.sort()
        # for i in fListCwd:
        #     print(i)
        isMVCFound = False
        for i in fListCwd:
            if i=='.mvc':
                isMVCFound = True
        if isMVCFound==False :
            # os.mkdir('./.mvc',0o777)
            # os.mkdir('./.mvc/stage',0o777)
            # os.mkdir('./.mvc/master',0o777)
            # os.mkdir('./.mvc/user',0o777)
            # index file creation for file ids
            mvcMeta = MVCMeta(os.path.basename(repoPath))
            mvcMeta.setRepoPath(repoPath)
            mvcMeta.createMetaData()
            # m = open('./.mvc/index.json','w+')
            # m.write(mvcMeta.toJSON())
            # m.close()
        else:
            # print("mvc init done already!!")
            pass
        self.repoPath=repoPath
        self.isRepoPathSet = True
        self.currentModifiedFiles = None
        self.setIndexDict()
        print("\nmvc init done on "+self.indexDict['localTimeOfCreation']+"\n")
    def setRepoPath(self,path):
        self.repoPath = path


    def add(self):
        self.status()
        l = input('Enter files numbers(with spaces in between e.g. 1 2 4) you would like to push to stage(0 to quit):')
        l = l.strip()
        e = getCleanInputList(l.split(sep=' '))
        print(e)
        if 0 in e:
            sys.exit()
        else:
            self.pushToStage(e)

    def addFile(self,path,absPath=False):
        sIndexData={}
        if absPath:
            relPath = os.path.relpath(path,start=self.repoPath)
        else:
            relPath = path
        if not os.path.exists(self.repoPath+'/.mvc/stage/sIndex.json'):
            if self.indexDict['currentVersion']==0 and self.indexDict['previousVersion']==0:
                sIndex = open(self.repoPath+'/.mvc/stage/sIndex.json','w+')
                sIndexData['version'] = -1
                sIndexData['files'] = {}
            else:
                latestV = self.indexDict['latestVersion']
                dupIndexFileForStage(self.repoPath,latestV)
                sIndex = open(self.repoPath+'/.mvc/stage/sIndex.json','r+')
                sIndexData = json.load(sIndex)
                self.changeIndexDataForStage(sIndexData)

                deleteFileContents(sIndex)
        else:
            sIndex = open(self.repoPath+'/.mvc/stage/sIndex.json','r+')
            sIndexData = json.load(sIndex)
            # sIndex.seek(0)
            # sIndex.truncate()
            deleteFileContents(sIndex)
        # TODO: add only when diff is not null
        mvcFile = MVCFile()
        gZipFileName = None
        if relPath in sIndexData['files']:
            modifiedFiles = None
            isModified = False
            if self.indexDict['isStatusCheckDone']:
                modifiedFiles = self.indexDict['modifiedFiles']
            else:
                self.status()
                modifiedFiles = self.indexDict['modifiedFiles']
            if relPath in modifiedFiles:
                if modifiedFiles[relPath]['tag']=='m':
                    isModified = True
            if not isModified:
                print("file not modified:"+relPath)
                sys.exit(0)
            oldFileData = sIndexData['files'][relPath]
            mvcFile.repoPath = oldFileData['repoPath']
            mvcFile.name = oldFileData['name']
            mvcFile.filePath = oldFileData['filePath']
            mvcFile.inCurrentVersion = True
            mvcFile.fileVersionReference = None
            mvcFile.baseFileVersion = oldFileData['baseFileVersion']
            mvcFile.isDeleted = False
            mvcFile.lastAvailableInVersion = None
            fileHash = oldFileData['fileHash']
            mvcFile.fileHash = fileHash
            gZipFileName = fileHash+'.gz'
            mvcFile.compressedDiffPatchFileName = gZipFileName
        else:
            # file is new i.e. not in stage index 
            mvcFile.repoPath = self.repoPath
            mvcFile.name = os.path.basename(relPath)
            mvcFile.filePath = './'+relPath
            mvcFile.inCurrentVersion = True
            mvcFile.fileVersionReference = None
            mvcFile.baseFileVersion = None
            mvcFile.isDeleted = False
            mvcFile.lastAvailableInVersion = None
            fileHash = returnBLAKE2Hash(relPath)
            mvcFile.fileHash = fileHash
            if os.path.exists(self.repoPath+'/.mvc/temp/patchedFiles/'+fileHash+'.'+mvcFile.name.split(sep='.')[1]):
                deleteFiles([self.repoPath+'/.mvc/temp/patchedFiles/'+fileHash+'.'+mvcFile.name.split(sep='.')[1]])
            gZipFileName = fileHash+'.gz'
            mvcFile.compressionExtension = '.gz'
            mvcFile.compressedDiffPatchFileName = gZipFileName
        if os.path.exists(self.repoPath+'/.mvc/stage/'+gZipFileName):
            deleteFiles([self.repoPath+'/.mvc/stage/'+gZipFileName])
        if mvcFile.baseFileVersion==None:
            # if the file is added newly for the first time baseFileVersion will be null or None
            if not createGZipFile(self.repoPath+'/'+relPath,self.repoPath+'/.mvc/stage/'+gZipFileName):
                # TODO: exit if compression failed
                pass
        else:
            # compressedBaseFilePath = self.repoPath+'/.mvc/master/'+str(mvcFile.baseFileVersion)+'/'+mvcFile.fileHash+'.gz'
            # tempBaseFilePath = self.repoPath+'/.mvc/temp/patchedFiles/'+mvcFile.fileHash+mvcFile.name.split(sep='.')[1]
            # extractGZipFile(compressedBaseFilePath,tempBaseFilePath)
            # self.applyPatchesToBaseFile(tempBaseFilePath,mvcFile.fileHash,mvcFile.baseFileVersion,self.indexDict['currentVersion'])
            to_be_added_patchFilePath = self.repoPath +'/.mvc/temp/patches/'+fileHash+'.patch'

            if not createGZipFile(to_be_added_patchFilePath,self.repoPath+'/.mvc/stage/'+gZipFileName):
                pass
            pass
        sIndexData['files'][relPath] = mvcFile.__dict__
        json.dump(sIndexData,sIndex,indent=4)
        self.indexDict['isStageOccupied'] = True
        self.saveIndexDict()
        sIndex.close()

    def deleteFile(self,path,absPath=True):
        sIndexData={}
        if absPath:
            relPath = os.path.relpath(path,start=self.repoPath)
        else:
            relPath = path
        if not os.path.exists(self.repoPath+'/.mvc/stage/sIndex.json'):
            if self.indexDict['currentVersion']==0 and self.indexDict['previousVersion']==0:
                sIndex = open(self.repoPath+'/.mvc/stage/sIndex.json','w+')
                sIndexData['version'] = -1
                sIndexData['files'] = {}
            else:
                latestV = self.indexDict['latestVersion']
                dupIndexFileForStage(self.repoPath,latestV)
                sIndex = open(self.repoPath+'/.mvc/stage/sIndex.json','r+')
                sIndexData = json.load(sIndex)
                self.changeIndexDataForStage(sIndexData)

                deleteFileContents(sIndex)
        else:
            sIndex = open(self.repoPath+'/.mvc/stage/sIndex.json','r+')
            sIndexData = json.load(sIndex)
            deleteFileContents(sIndex)
        mvcFile = MVCFile()
        gZipFileName = None
        if relPath in sIndexData['files']:
            oldFileData = sIndexData['files'][relPath]
            mvcFile.repoPath = oldFileData['repoPath']
            mvcFile.name = oldFileData['name']
            mvcFile.filePath = oldFileData['filePath']
            mvcFile.inCurrentVersion = False
            mvcFile.fileVersionReference = None
            mvcFile.isDeleted = True
            lastAvailable = None
            if oldFileData['inCurrentVersion']:
                lastAvailable = self.indexDict['latestVersion']
            else:
                lastAvailable = oldFileData['fileVersionReference']
            mvcFile.lastAvailableInVersion = lastAvailable
            fileHash = oldFileData['fileHash']
            gZipFileName = fileHash+'.gz'
            mvcFile.fileHash = fileHash
            mvcFile.compressedDiffPatchFileName = gZipFileName
        else:
            print('ERROR deletion: File not found!')
            sys.exit()
        sIndexData['files'][relPath] = mvcFile.__dict__
        json.dump(sIndexData,sIndex,indent=4)
        self.indexDict['isStageOccupied'] = True
        self.saveIndexDict()
        sIndex.close()

    def commit(self):
        commitVersion = self.indexDict['latestVersion']+1
        destVerDir = self.repoPath+'/.mvc/master/'+str(commitVersion)
        srcFilePathPrefix = self.repoPath+'/.mvc/stage/'
        os.mkdir(destVerDir,mode=0o777)
        sIndex = open(self.repoPath+'/.mvc/stage/sIndex.json','r+')
        sIndexData = json.load(sIndex)
        deleteFileContents(sIndex)
        sIndex.close()
        deleteFiles([self.repoPath+'/.mvc/stage/sIndex.json'])
        copyFileList=[]
        for file,fileDict in sIndexData['files'].items():
            if fileDict['inCurrentVersion']:
                # fileDict['fileVersionReference']=commitVersion
                copyFileList.append(srcFilePathPrefix+fileDict['compressedDiffPatchFileName'])
                if fileDict['baseFileVersion']==None:
                    fileDict['baseFileVersion'] = commitVersion
        copyFilesToDir(destVerDir,copyFileList)
        deleteFiles(copyFileList)
        commitVerIndexFile = destVerDir+'/'+str(commitVersion)+'.json'
        createFile(commitVerIndexFile)
        sIndexData['version'] = commitVersion
        saveDataToFile(commitVerIndexFile,json.dumps(sIndexData,indent=4))
        self.indexDict['latestVersion']=commitVersion
        self.indexDict['currentVersion'] = commitVersion
        self.indexDict['previousVersion']=commitVersion-1
        self.indexDict['versions'] = self.indexDict['versions']+1
        self.indexDict['versionList'].append(commitVersion)
        self.indexDict['isStageOccupied'] = False
        self.indexDict['isStatusCheckDone'] = False
        self.indexDict['modifiedFiles'] = {}
        self.saveIndexDict()
        self.refreshTempDirectory()

    def status(self,printTree = True):
        self.printTreeWithCount3(self.repoPath,printTree = printTree,numberAll=False,showOnlyModified=False,absPath=True)
        self.indexDict['isStatusCheckDone'] = True
        self.saveIndexDict()
        pass

    def revert(self,rVersion):
        cVersion = self.indexDict['currentVersion']
        if cVersion<rVersion:
            print("ERROR in Revert: Please enter a valid version number")
            sys.exit(0)
        rVerIndexFile = open(self.repoPath+'/.mvc/master/'+str(rVersion)+'/'+str(rVersion)+'.json','r')
        rVerIndex = json.load(rVerIndexFile)
        rVerIndexFile.close()
        cVerIndexFile = None
        if self.indexDict['isStageOccupied']:
            cVerIndexFile = open(self.repoPath+'/.mvc/stage/sIndex.json','r')
        else:
            cVerIndexFile = open(self.repoPath+'/.mvc/master/'+str(cVersion)+'/'+str(cVersion)+'.json','r')
        cVerIndex = json.load(cVerIndexFile)
        cVerIndexFile.close()
        changes = self.returnIndexChanges(rVerIndex,cVerIndex)
        pprint.pprint(changes)
        self.makeReversionChanges(changes)
        self.indexDict['currentVersion'] = rVersion
        self.saveIndexDict()

    def pushToStage(self,inputSet):
        # for i in inputSet:
        #     tag = self.indexDict['modifiedFiles'][i-1]['tag']
        #     filePath = self.indexDict['modifiedFiles'][i-1]['filePath']
        #     if tag == 'n' or tag=='m':
        #         self.addFile(filePath)
        #         self.indexDict['modifiedFiles'][i-1]['tag'] = 'u'
        #         print(' <ADD> :'+filePath + ' is pushed to stage.')
        for f,fv in self.indexDict['modifiedFiles'].items():
            if fv['treeIndex'] in inputSet:
                if fv['tag'] == 'n' or fv['tag'] =='m':
                    filePath = fv['filePath']
                    self.addFile(filePath)
                    self.indexDict['modifiedFiles'][filePath]['tag'] = 'u'
                    print(ADD_COLOR+' <ADD> :'+COLOR_RESET+MODIFIED_COLOR+filePath+COLOR_RESET + ' is pushed to stage.')

        self.saveIndexDict()
    def setIndexDict(self):
        # TODO: change code and make use of MVCMeta class
        index = open(self.repoPath+'/.mvc/index.json','r')
        self.indexDict = json.load(index)
        index.close()

    def saveIndexDict(self):
        index = open(self.repoPath+'/.mvc/index.json','r+')
        deleteFileContents(index)
        json.dump(self.indexDict,index,indent=4)
        index.close()
    def getIndexDict(self):
        return self.indexDict

    def changeIndexDataForStage(self,sIndexData):
        sIndexData['version'] = -1
        for file,fileDict in sIndexData['files'].items():
            if fileDict['inCurrentVersion']:
                fileDict['inCurrentVersion']=False
                fileDict['fileVersionReference'] = self.indexDict['latestVersion'] 
    
    def generateDiffPatchFile(self,oldFileRelPath,newFileRelPath,fileHash):
        diffPatchPath = self.repoPath+'/.mvc/temp/patches/'+fileHash+'.patch'
        diffPatchCommand = 'diff -u '+oldFileRelPath+' '+newFileRelPath+' > '+diffPatchPath
        os.system(diffPatchCommand)
        pass
    def returnIndexChanges(self,index1,index2):
        # index1 -- revert version -- rV
        # index2 -- current version -- cV
        changes={'add':[],'replace':[],'delete':[],'leave':[]}
        for k2,v2 in index2['files'].items():
            if k2 in index1['files']:
                # if file found in revert version
                v1 = index1['files'][k2]
                if (v2['fileVersionReference'] == v1['fileVersionReference']) or (v1['inCurrentVersion'] and v2['fileVersionReference']==index1['version']):
                    # if rV and cV point to same file version
                    changes['leave'].append(k2)
                elif v1['isDeleted']:
                    # if file isDeleted in rV
                    if not v2['isDeleted']:
                        changes['delete'].append(k2)
                    else:
                        changes['leave'].append(k2)
                else:
                    # if file is not isDeleted in rV and not isDeleted in cV
                    if not v2['isDeleted']:
                        changes['replace'].append(k2)
                    else:
                        changes['add'].append(k2)
            else:
                # TODO: check if file exists before delete!!
                changes['delete'].append(k2)
        return changes
    def isNewOrModified(self,path,absPath=True,genPatch=False):
        if not os.path.exists(path):
            print(path)
            print('ERROR file not found!')
        relPath = None
        if absPath:
            relPath = os.path.relpath(path,start=self.repoPath)
        else:
            relPath = path
        tIndexData = None
        if self.indexDict['isStageOccupied']:
            sIndex = open(self.repoPath+'/.mvc/stage/sIndex.json','r')
            tIndexData = json.load(sIndex)
            sIndex.close()
        elif self.indexDict['currentVersion']==0 and self.indexDict['latestVersion']==0:
            return 'n'
        else:
            # print('Here')
            cVersion = self.indexDict['currentVersion']
            cVersionIndex = open(self.repoPath+'/.mvc/master/'+str(cVersion)+'/'+str(cVersion)+'.json','r')
            tIndexData = json.load(cVersionIndex)
            cVersionIndex.close()
        # print(relPath)
        if relPath in tIndexData['files']:
            fileData = tIndexData['files'][relPath]
            if fileData['isDeleted']:
                return 'n'
            fileReference = tIndexData['files'][relPath]['fileVersionReference']
            baseFileReference = tIndexData['files'][relPath]['baseFileVersion']
            fileHash = tIndexData['files'][relPath]['fileHash']
            compressedDiffPatchFileName = tIndexData['files'][relPath]['compressedDiffPatchFileName']
            # in stage 
            if fileData['inCurrentVersion'] and fileData['fileVersionReference']==None and tIndexData['version']==-1:
                fromPath = self.repoPath+'/.mvc/stage/'+compressedDiffPatchFileName
            else:
                # changed from str(fileReference) to str(baseFileReference) for mvcVersion=2
                fromPath = self.repoPath+'/.mvc/master/'+str(baseFileReference)+'/'+compressedDiffPatchFileName
            toPath = None
            fileExtension = tIndexData['files'][relPath]['name'].split(sep='.')[1]
            if len(fileExtension)==0:
                # changed from 'cVUnmodifiedFiles' to  'patchedFiles' for mvcVersion=2
                toPath = self.repoPath+'/.mvc/temp/patchedFiles/'+tIndexData['files'][relPath]['fileHash']
            else:
                toPath = self.repoPath+'/.mvc/temp/patchedFiles/'+tIndexData['files'][relPath]['fileHash']+'.'+fileExtension
            if not os.path.exists(toPath):
                extractGZipFile(fromPath,toPath)
                if baseFileReference!=None and baseFileReference!=self.indexDict['currentVersion']:
                    self.applyPatchesToBaseFile(toPath,fileHash,baseFileReference,self.indexDict['currentVersion'])
                else:
                    # print("prabhath--1")
                    pass
            patchPath=None
            if genPatch:
                patchPath = self.repoPath+'/.mvc/temp/patches/'+fileHash+'.patch'
            
            # if there is a new patch in stage then apply it also!
            if tIndexData['version']==-1:
                stagedPatchPath = self.repoPath+'/.mvc/stage/'+fileHash+'.gz'
                if os.path.exists(stagedPatchPath):
                    tempPatch = self.repoPath +'/.mvc/temp/patchedFiles/'+fileHash+'.patch' 
                    onTempPatchedFile = self.repoPath +'/.mvc/temp/patchedFiles/'+fileHash+'.'+fileExtension
                    extractGZipFile(stagedPatchPath,tempPatch)
                    applyUnixPatch(onTempPatchedFile,tempPatch)



            isModified = self.getBooleanDiffOrGenerateDiffWithPatch(self.repoPath+'/'+relPath,toPath,absPath=True,genHtml=False,genPatch=genPatch,patchPath=patchPath)
            # print(isModified)
            # only when file is in stage and modified
            if fileData['inCurrentVersion'] and fileData['fileVersionReference']==None and tIndexData['version']==-1:
                # TODO: check if file is modified after adding to stage!!!
                if isModified:
                    return 'm'
                else:
                    return 'u'

            if isModified:
                # deleteFiles([toPath])
                pass
            else:
                # deleteFiles([toPath])
                pass
            if isModified:
                return 'm'
            else:
                return ' '
        else:
            return 'n'
    
    def getBooleanDiffOrGenerateDiffWithPatch(self,path1,path2,absPath=True,genText=False,textPath=None,genHtml=False,htmlPath=None,genPatch = False,patchPath = None):
        relPath1 = None # path1 --- modified file
        relPath2 = None # path2 --- temp extracted file
        if absPath:
            relPath1 = os.path.relpath(path1,start=self.repoPath)
            relPath2 = os.path.relpath(path2,start=self.repoPath)
        else:
            relPath1 = path1
            relPath2 = path2
        # diffoscopeCommand = 'diffoscope '+path1+' '+path2+' --text -'
         # NOTE: DIFF of UNIX requires required changes to make file1 to file2 , 
         # so command will be
        #  diff -u path2 path1 # since we need changes to make path2 into path1 file
        unixDiffCommand = 'diff -u '+path2+' '+path1
        diffBit = False
        c = subprocess.run(unixDiffCommand,stdout=subprocess.PIPE,shell=True)
        out = c.stdout.decode('utf-8')
        if len(out)>0:
            diffBit = True
        if diffBit:
            if genHtml and htmlPath!=None:
                diffoscopeHTMLCommand = 'diffoscope '+path1+' '+path2+' --html '+htmlPath
                c = subprocess.run(diffoscopeHTMLCommand,stdout=subprocess.PIPE,shell=True)
            elif genText and textPath!=None:
                diffoscopeTEXTCommand = 'diffoscope '+path1+' '+path2+' --text '+textPath
                # unixDiffCommand = 'diff '+path1+' '+path2
                c = subprocess.run(shlex.split(diffoscopeTEXTCommand),stdout=subprocess.PIPE,shell=True)
            elif genPatch and patchPath!=None:
                # print("prabhath")
                # diffoscopeCommand = 'diffoscope '+path1+' '+path2+' --text -'
                # NOTE: DIFF of UNIX requires required changes to make file1 to file2 , so command will be
                #  diff -u path2 path1 # since we need changes to make path2 into path1 file
                unixDiffPatchCommand = 'diff -u '+path2+' '+path1+' > '+patchPath
                c = subprocess.run(unixDiffPatchCommand,stdout=subprocess.PIPE,shell=True)
                # out = c.stdout.decode('utf-8')
                # if len(out)>0:
                #     diffBit = True
                return diffBit
            else:
                return diffBit
        else:
            return diffBit
                
        return diffBit


    def applyPatchesToBaseFile(self,toPath,fileHash,baseVersion,tillVersion):
        # fileExtension = os.path.basename(toPath).split(sep='.')[1]
        for v in range(baseVersion+1,tillVersion+1):
            p = self.repoPath+'/.mvc/master/'+str(v)+'/'+fileHash+'.gz'
            if os.path.exists(p):
                tempPatchFilePath = self.repoPath+'/.mvc/temp/patchedFiles/'+fileHash+'.patch'
                extractGZipFile(p,tempPatchFilePath)
                applyUnixPatch(toPath,tempPatchFilePath)
                # deleteFiles([tempPatchFilePath])
        
    def makeReversionChanges(self,changes):
        cwd = os.getcwd()
        os.chdir(self.repoPath)
        cV = self.indexDict['currentVersion']
        cVFile = open('./.mvc/master/'+str(cV)+'/'+str(cV)+'.json','r')
        cVIndex = json.load(cVFile)
        cVFile.close()
        cVFiles = cVIndex['files']
        # deletion
        if len(changes['delete'])>0:
            deleteFiles(changes['delete'])
        # replacement
        if len(changes['replace'])>0:
            for rfPath in changes['replace']:
                fData = cVFiles[rfPath]
                fromPath = self.repoPath+'/.mvc/master/'+str(fData['fileVersionReference'])+'/'+str(fData['compressedDiffPatchFileName'])
                toPath = None
                toPath = fData['filePath']
                if os.path.exists(fData['filePath']):
                    extractGZipFile(fromPath,toPath)
                else:
                    basePath,fileName = os.path.split(fData['filePath'])
                    if os.path.exists(basePath):
                        extractGZipFile(fromPath,toPath)
                    else:
                        os.makedirs(basePath)
                        extractGZipFile(fromPath,toPath)
        # addition
        if len(changes['add'])>0:
            for afPath in changes['add']:
                fData = cVFiles[afPath]
                fromPath = self.repoPath+'/.mvc/master/'+str(fData['lastAvailableInVersion'])+'/'+str(fData['compressedDiffPatchFileName'])
                toPath = fData['filePath']
                if os.path.exists(fData['filePath']):
                    extractGZipFile(fromPath,toPath)
                else:
                    basePath,fileName = os.path.split(fData['filePath'])
                    if os.path.exists(basePath):
                        extractGZipFile(fromPath,toPath)
                    else:
                        os.makedirs(basePath)
                        extractGZipFile(fromPath,toPath)
        

        # important ! change cwd from . to old cwd
        os.chdir(cwd)
    def listFiles(self):
        for i in self.indexDict:
            print(i)
    def getListOfIndexedFiles(self):
        files = None
        indexedList = []
        if self.indexDict['isStageOccupied']:
            f = open(self.repoPath+'/.mvc/stage/sIndex.json','r')
            files = f['files']
            f.close()

    def toJSON(self):
        return json.dumps(self,default=myEncoder,sort_keys=True,indent=4)
    def fromJSON(self,jsonData):
        self.__dict__ = json.loads(jsonData)



    def printTreeWithCount3(self,dirPath,absPath=False,printTree = True,genPatch = True,indexedFiles=None,showOnlyStaged=False,showOnlyModified=False,numberAll = False,dirLevel=1,count=0):
        dL=dirLevel
        startCount = int(count)
        fileNumber = int(count)
        bufferSpace = ' '#<1 space>
        dString = (dL-1)*'   ' #<3 spaces>
        rwd =None
        relPath = None
        l = None
        if absPath:
            rwd = dirPath
            # relPath = os.path.basename(dirPath)
            relPath = '.'
            l = os.listdir(dirPath)
        else:
            rwd = os.path.join(self.repoPath,dirPath)
            relPath = dirPath
            l = os.listdir(rwd)
        root=None
        rootName = None
        if dL==1:
            # if absPath:
            rootName = os.path.basename(rwd)
            root = rwd
            # else:
                # rootName = os.path.basename(rwd)
                # root = rwd
        else:
            # if absPath:
            root = rwd
            rootName = os.path.basename(rwd)
            # else:
            #     root = rwd
            #     rootName = os.path.basename(relPath)
        # print('rwd:'+rwd)
        # print('root:'+root)
        if printTree:
            if dL>1:
                dPString = (dL-2)*'   '#<3 spaces>  
                print(bufferSpace+'     '+dPString+'|-['+rootName+']')# 6 spaces(including bufferSpace=<1 space>) for modified bit,space and fileNumber=<3spaces> 
            else:
                print(dString+'     '+'['+rootName+']')#<5 spaces> for m bit,fileNumber=<3spaces> and extra space
        dirs = []
        for f in l:
            normalizedPath = os.path.normpath(os.path.join(root,f))
            relFilePath = os.path.relpath(normalizedPath,self.repoPath)
            if not os.path.isdir(normalizedPath):
                mBit = 'n'
                # print(f)
                # print(os.path.join(root,f))
                mBit = self.isNewOrModified(normalizedPath,absPath=absPath,genPatch=genPatch)
                # print(mBit)
                if mBit=='n' or mBit=='m' or mBit=='u':
                    printString = bufferSpace+mBit+' '+'<'+str(fileNumber+1)+'>'+dString+'|--'+f
                    if printTree:
                        print(MODIFIED_COLOR+printString+COLOR_RESET)
                    # isInModifiedFiles,indexInModifiedFilesList = self.returnBooleanAndIndexIfInModifiedFilesList(normalizedPath)
                    # print(type(asd))
                    # print(asd)
                    # if isInModifiedFiles:
                        # pass
                    modifiedFileIndexDictData = None
                    if relFilePath in self.indexDict['modifiedFiles']:
                        modifiedFileIndexDictData = self.indexDict['modifiedFiles'][relFilePath]
                    if relFilePath in self.indexDict['modifiedFiles'] and modifiedFileIndexDictData['treeIndex']==fileNumber+1:
                        modifiedFileIndexDictData['tag'] = mBit
                        pass
                    elif relFilePath in self.indexDict['modifiedFiles'] and modifiedFileIndexDictData['treeIndex']!=fileNumber+1:
                        modifiedFileIndexDictData['treeIndex'] = fileNumber+1
                        modifiedFileIndexDictData['tag'] = mBit
                    else:
                        self.indexDict['modifiedFiles'][relFilePath] = returnModifiedDict(normalizedPath,self.repoPath,fileNumber+1,mBit)
                    fileNumber = fileNumber+1
                if (not showOnlyModified) and mBit==' ' and printTree:
                    if numberAll:
                        print(bufferSpace+mBit+' '+'<'+str(fileNumber+1)+'>'+dString+'|--'+f)
                        fileNumber = fileNumber+1
                    else:
                        print(bufferSpace+mBit+'    '+dString+'|--'+f)
            else:
                if not (len(f)>1 and f[0]=='.'): 
                    dirs.append(f)
        startCount = fileNumber
        for d in dirs:
            normalizedPath = os.path.normpath(os.path.join(root,d))
            startCount =  self.printTreeWithCount3(normalizedPath,absPath=absPath,printTree=printTree,showOnlyModified=showOnlyModified,numberAll=numberAll,dirLevel=dL+1,count=startCount)
        returnCount = fileNumber if len(dirs)==0 else startCount
        if dirLevel ==1:
            self.saveIndexDict()
        return returnCount

    def returnBooleanAndIndexIfInModifiedFilesList(self,absPath):
        relPath = os.path.relpath(absPath,self.repoPath)
        modifiedFiles = self.indexDict['modifiedFiles']
        for i in range(len(modifiedFiles)):
            if modifiedFiles[i]['filePath']==relPath:
                return (True,i)
        return (False,None)

    def refreshTempDirectory(self):
        shutil.rmtree(self.repoPath+'/.mvc/temp')
        os.mkdir(self.repoPath+'/.mvc/temp',0o777)
        os.mkdir(self.repoPath+'/.mvc/temp/cVUnmodifiedFiles',0o777)
        os.mkdir(self.repoPath+'/.mvc/temp/patchedFiles',0o777)
        os.mkdir(self.repoPath+'/.mvc/temp/patches',0o777)

    def generateStatus(self,dirPath,absPath=False,indexedFiles=None,showOnlyModified=False,numberAll = False,dirLevel=1,count=0):
        dL=dirLevel
        startCount = int(count)
        fileNumber = int(count)
        bufferSpace = ' '#<1 space>
        dString = (dL-1)*'   ' #<3 spaces>
        rwd =None
        relPath = None
        l = None
        if absPath:
            rwd = dirPath
            relPath = '.'
            l = os.listdir(dirPath)
        else:
            rwd = os.path.join(self.repoPath,dirPath)
            relPath = dirPath
            l = os.listdir(rwd)
        root=None
        rootName = None
        if dL==1:
            rootName = os.path.basename(rwd)
            root = rwd
        else:
            root = rwd
            rootName = os.path.basename(rwd)
        # if dL>1:
            # dPString = (dL-2)*'   '#<3 spaces>  
            # print(bufferSpace+'     '+dPString+'|-['+rootName+']')# 6 spaces(including bufferSpace=<1 space>) for modified bit,space and fileNumber 
        # else:
            # print(dString+'     '+'['+rootName+']')#<5 spaces> for m bit,file number and extra space
        dirs = []
        for f in l:
            if not os.path.isdir(os.path.normpath(os.path.join(root,f))):
                mBit = 'n'
                # print(f)
                # print(os.path.join(root,f))
                mBit = self.isNewOrModified(os.path.join(root,f),absPath=absPath)
                if mBit=='n' or mBit=='m' or mBit=='u':
                    # print(bufferSpace+mBit+' '+'<'+str(fileNumber+1)+'>'+dString+'|--'+f)
                    fileNumber = fileNumber+1
                if (not showOnlyModified) and mBit==' ':
                    if numberAll:
                        # print(bufferSpace+mBit+' '+'<'+str(fileNumber+1)+'>'+dString+'|--'+f)
                        fileNumber = fileNumber+1
                    # else:
                        # print(bufferSpace+mBit+'    '+dString+'|--'+f)
            else:
                if not (len(f)>1 and f[0]=='.'): 
                    dirs.append(f)
        startCount = fileNumber
        for d in dirs:
            normalizedPath = os.path.normpath(os.path.join(root,d))
            startCount =  self.generateStatus(normalizedPath,absPath=absPath,showOnlyModified=showOnlyModified,numberAll=numberAll,dirLevel=dL+1,count=startCount)
        returnCount = fileNumber if len(dirs)==0 else startCount
        return returnCount
# **********************************************
# functions used in class
# **********************************************

# clear contents of a file
def deleteFileContents(fileDescriptor):
    fileDescriptor.seek(0)
    fileDescriptor.truncate()

def returnModifiedDict(absPath,repoPath,treeIndex,mTag):
    relPath = os.path.relpath(absPath,repoPath)
    d = {}
    d['filePath'] = relPath
    d['tag'] = mTag
    d['treeIndex'] = treeIndex
    return d

def applyUnixPatch(onFilePath,patchFilePath):
    patchCommand = 'patch -i '+patchFilePath+' -o '+onFilePath
    # print(patchCommand)
    os.system(patchCommand)

def createFile(filePath):
    if not os.path.exists(filePath):
        open(filePath,'w+').close()
        return True
    else:
        return False

def getCleanInputList(inputList):
    l = set()
    for i in inputList:
        l.add(int(i))
    return l

def saveDataToNewFile(filePath,data):
    f = open(filePath,'w+')
    f.write(data)
    f.close()


def saveDataToFile(filePath,data):
    f = open(filePath,'r+')
    deleteFileContents(f)
    f.write(data)
    f.close()


def isFileNew(sIndexData,filePath):
    if filePath not in sIndexData:
        return True
    else:
        return False


def returnBLAKE2Hash(dataString,digestSize=16):
    hObj = hashlib.blake2b(digest_size=digestSize)
    hObj.update(dataString.encode('utf-8'))
    return hObj.hexdigest()

def copyFilesToDir(destDirPath,filePathsList):
    for file in filePathsList:
        shutil.copy(file,destDirPath)


def deleteFiles(filePathsList):
    for file in filePathsList:
        os.remove(file)
    pass
def dupIndexFileForStage(repoPath,latestV):
    previousSIndexPath = repoPath+'/.mvc/master/'+str(latestV)+'/'+str(latestV)+'.json'
    newSIndexPath = repoPath+'/.mvc/stage/sIndex.json'
    shutil.copy(previousSIndexPath,newSIndexPath)


def extractGZipFile(fromPath,toPath):
    with gzip.open(fromPath,'rb') as inputFile:
        with open(toPath,'wb') as outputFile:
            shutil.copyfileobj(inputFile,outputFile)
    # check if gzip file is successfully created and return boolean
    if os.path.exists(toPath):
        return True
    else:
        return False


def createGZipFile(fromPath,toPath):
    with open(fromPath,'rb') as inputFile:
        with gzip.open(toPath,'wb') as outputFile:
            shutil.copyfileobj(inputFile,outputFile)
    # check if gzip file is successfully created and return boolean
    if os.path.exists(toPath):
        return True
    else:
        return False