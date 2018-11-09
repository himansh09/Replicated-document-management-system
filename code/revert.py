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
    # print('Following versions available')
    MVC.printColoredText('******REVERSION******','red')
    MVC.printColoredText('Following versions available','red')
    availableVersions = m.getAvailableVersionList()
    MVC.printColoredText('Choose the version you want to revert to','red')
    for i in range(1,len(availableVersions)+1):
        if i==len(availableVersions):
            MVC.printColoredText('[{}]< Current Version'.format(i),'green')
        else:
            MVC.printColoredText('[{}]'.format(i),'yellow')
    rVersion = input()
    rVersion = rVersion.strip()
    if not rVersion.isdigit():
        MVC.printColoredText('ERROR invalid input','red')
        sys.exit(0)
    rVersion = int(rVersion)
    if rVersion >= len(availableVersions):
        MVC.printColoredText('ERROR invalid version','red')
        sys.exit(0)
    MVC.printColoredText('Following version(s) will be LOST','red')
    versionsToBeDeleted = list(range(rVersion+1,len(availableVersions)+1))
    MVC.printColoredText(str(versionsToBeDeleted),'red')
    MVC.printColoredText('Are you sure? (Y/N):','red')
    ans = input()
    doRevert = False
    if ans=='y'or ans=='Y'or ans=='yes'or ans=='YES'or ans=='Yes':
        doRevert = True
    # MVC.printColoredText('')
    if doRevert:
        m.revert(rVersion)
    else:
        MVC.printColoredText('Goodbye','green')
    pass