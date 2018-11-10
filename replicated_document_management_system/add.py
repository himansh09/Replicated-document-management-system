# add command for mvc
import os
import sys
import pprint
import json
from classes.MVCMeta import MVCMeta
from classes import MVC
import re
import init
myEncoder = lambda o:o.__dict__
if __name__=='__main__':
    rp = init.mvcInit()
    m = MVC.MVC(repoPath = rp)
    print('[1] Addition using manual path entry')
    print('[2] Addition using Status tree')
    c = input()
    if not c.isdigit():
        print('ERROR enter positive valid number!')
        sys.exit(0)
    c = int(c)
    if c>2 or c<0:
        print('ERROR invalid choice:(enter 1 or 2)')
        sys.exit(0)
    if c==1:
        MVC.printColoredText('add <relative filepath>','green')
        q = input()
        q = q.strip()
        if q.index('add')!=0:
            MVC.printColoredText('Usage:add <relative filepath>','red')
            sys.exit(0)
        
        if m.checkIfFileExists(q,absPath=False):
            indexedFiles = m.getListOfIndexedFiles()
            if q in indexedFiles:
                m.addFile(q,absPath=False)
            else:
                # file is new addition
                m.addFile(q,absPath=False)
                pass 
        else:
            MVC.printColoredText('fatal: relative filepath did not match any files','red')
            sys.exit(0)   
    elif c==2:
        m.status(printTree=True)
        print("Enter file numbers (with spaces in between e.g. 1 2 7) to add and push to stage(0 to exit):")
        l = input()
        e = init.getCleanInputSet(l)
        # print(e)
        if 0 in e:
            print("Goodbye")
            sys.exit(0)
        m.pushToStage(e)