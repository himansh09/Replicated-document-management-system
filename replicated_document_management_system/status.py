# status command for mvc
import os
import sys
import pprint
import json
from classes.MVCMeta import MVCMeta
from classes import MVC
import init
myEncoder = lambda o:o.__dict__

if __name__=='__main__':
    rp = init.mvcInit()
    m = MVC.MVC(repoPath = rp)
    m.status(printTree=True)
