import os
import sys
import pprint
import json
import time
from classes.MVCMeta import MVCMeta
from classes import MVC
myEncoder = lambda o:o.__dict__
def mvcInit():
    reposData = None
    repoPath = None
    if os.path.exists('repos.json'):
        reposFile = open('./repos.json','r+')
        if os.path.getsize('./repos.json')>0:
            reposData = json.loads(reposFile.read())
        else:
            reposData = None
        if reposData == None:
            # repos.json empty!
            reposData = {}
            reposData['length'] = 0
            reposData['lastUsedRepo'] = None
            reposData['repos'] = [] 
            reposData['localtime'] = time.asctime(time.localtime(time.time()))   
        reposFile.seek(0)
        reposFile.truncate()
    else:
        # repos.json not found!
        reposFile = open('./repos.json','w+')
        reposData = {}
        reposData['length'] = 0
        reposData['lastUsedRepo'] = None
        reposData['repos'] = []
        reposData['localtime'] = time.asctime(time.localtime(time.time()))
    os.system('clear')
    if reposData['length']==0:
        print('[{0}] Set Database Path'.format(0))
    else:
        print('[{0}] Set Database Path'.format(0))
        for i in range(reposData['length']):
            print('[{0}] {1}'.format(i+1,reposData['repos'][i]))
    print('Choose an option:')
    q = input()
    if len(q)>=1 and q.isdigit():
        q = int(q)
        if q>reposData['length']:
            print('ERROR enter valid number from the above list! ')
            json.dump(reposData,reposFile,indent=4)
            reposFile.close()
            sys.exit(0)    
    else:
        print('ERROR positive integer option expected')
        json.dump(reposData,reposFile,indent=4)
        reposFile.close()
        sys.exit(0)
    if q==0:
        os.system('clear')
        print('Path:')
        repoPath = input()
        rp = repoPath
        if repoPath=='.':
            rp = os.getcwd()
        if not rp in reposData['repos']:
            reposData['repos'].append(rp)
            reposData['length'] = reposData['length']+1
        reposData['lastUsedRepo'] = rp
    elif reposData['length']==0 and q != 0:
        print("ERROR Invalid option input !! Enter valid option")
        json.dump(reposData,reposFile,indent=4)
        reposFile.close()
        sys.exit(0)
    else:
        repoPath = reposData['repos'][q-1]
        reposData['lastUsedRepo'] = repoPath
    json.dump(reposData,reposFile,indent=4)
    reposFile.close()
    return repoPath
def toJSON(self):
    return json.dumps(self,default=myEncoder,sort_keys=True,indent=4)
def fetchUser(id):
    #TODO function for fetch user data and copy to .mvc file
    pass
def getCleanInputSet(inputString):
    l = set()
    inputList = inputString.split(sep=' ')
    for i in inputList:
        l.add(int(i))
    return l
rp = None
if __name__=='__main__':
    rp = mvcInit()
    m = MVC.MVC(repoPath = rp)
# if len(sys.argv)==3:
#     if sys.argv[1]=='-rp':
#         rp = sys.argv[2]
# else:
#     print('Usage: python3 <scriptname>.py -rp "path"')
#     sys.exit(0)
# rp = mvcInit()
# m = MVC.MVC(repoPath=rp)


# m.addFile('b/b1.txt',absPath=False)
# m.addFile('b/c/b1.txt',absPath=False)
# m.addFile('a1.txt',absPath=False)
# m.commit()


# m.addFile('p1.txt',absPath=False)
# m.commit()


# m.addFile('p2.txt',absPath=False)
# m.deleteFile('p1.txt',absPath=False)
# m.commit()


# m.addFile('p1.txt',absPath=False)
# m.addFile('b/c/b1.txt',absPath=False)
# m.commit()


# m.addFile('a2.txt',absPath=False)
# m.deleteFile('a1.txt',absPath=False)
# m.commit()
# m.addFile('a1.txt',absPath=False)
# print('*******************')
# x= m.printTreeWithCount3(rp,numberAll=False,showOnlyModified=False,absPath=True)
# # m.status()
# # m.addFile('das.txt',absPath=False)
# l = input('Enter files numbers(with spaces in between e.g. 1 2 4) you would like to push to stage:')
# print(l.split(sep=' '))
# e = getCleanInputList(l.split(sep = ' '))
# print(e)
# print(0 in e)
# m.pushToStage(e)
# m.commit()
# # m.isModified('/home/charlie/Desktop/db1/b/c/b1.txt')

# m.revert(3)