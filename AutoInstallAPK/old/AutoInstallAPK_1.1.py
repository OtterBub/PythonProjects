import copy
import os
import re
import subprocess
import sys
import threading
import unittest
from multiprocessing import Process, Queue
from time import sleep
from typing import Any, Callable, List, Mapping, Optional, Tuple


class thrList:
    def __init__(self):
        self.ThreadList = []

    def addThread(self, funcTarget:Optional[Callable[..., Any]] = ... ,funcArgs:tuple = []):
        thr = Process(target=funcTarget, args=funcArgs)
        self.ThreadList.append(thr)

    def startThread(self):
        for thr in self.ThreadList:
            thr.start()

    def join(self):
        for thr in self.ThreadList:
            thr.join()

def installApk(app:str = ''):
    
    tList = thrList()
    capList = list()
    cap = {}

    if len(app) > 0:
        cap['appPath'] = app
    else: 
        print("AppPath don't Setting")
        return 0


    getCmdResult = subprocess.check_output('adb devices', text=True)

    getDevices = getCmdResult.splitlines()

    print("---devices----")
    
    # Devices List Get
    for reSplit in getDevices:
        #print(reSplit)
        sp = reSplit.split('\t')
        
        if len(sp) >= 2:
            if sp[1] == "device":
                
                # udid
                print("udid: %s" %sp[0])
                cap['udid'] = sp[0]

                
                #android APK install
                tList.addThread(os.system, ('adb -s %s install -d -r "%s"' %(cap['udid'], cap['appPath']),))
                #os.system('adb -s %s install %s' %(cap['udid'], cap['appPath']))
    
    tList.startThread()
    tList.join()

    return capList

def tempFunc():
    print('tempFunc')



if __name__ == "__main__":

    appPath = os.path.join(
        os.path.dirname(__file__), 
        'C:\\Users\\Administrator\\Desktop\\-TodayTest\\1. MeetUs\\Together install\\Together AOS Version\\beta_debug', 
        'groupcallapp-beta-debug-1.0.8.3.apk'
        )
    appPath = os.path.abspath(appPath)

    if len(sys.argv) >= 2:
        appPath = sys.argv[1]
    else: 
        print("Need argument") 
        input()
        exit()

    print(appPath)

    installApk(app = appPath)

    print("Complete")
    input()

    

    print('\ninstall End')
