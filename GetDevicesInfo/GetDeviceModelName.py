import copy
import os
import re
import subprocess
import sys
import threading
from multiprocessing import Process, Queue
from time import sleep
from typing import Any, Callable, List, Mapping, Optional, Tuple

#CONST
#INSTALL STATUS
IDLE = 0
INSTALLING = 1
COMPLITE = 2

#ADB NAME
ADB = "nox_adb"

#Reg
getModelReg = re.compile(r"model]:\s\[([\S]*)\]")
getOSVersionReg = re.compile(r"version.release]:\s\[([\S]*)\]")
getPhoneNumReg = re.compile(r"8?[2|0]0?1[8|7|0|1][\d]*")

class device:
    def __init__(self):
        self.installed = False
        self.installStatus = IDLE
        
        self.modelName = "None"
        self.udid = "None"
        self. OSVersion = "None"

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

def getDeviceInfo():

    resultDict = dict()

    getCmdResult = subprocess.check_output('%s devices' %(ADB), text=True)
    getDevices = getCmdResult.splitlines()

    print("----getDeviceInfo----")
    
    # Devices List Get
    for reSplit in getDevices:
        #print(reSplit)
        sp = reSplit.split('\t')
        
        if len(sp) >= 2:
            if sp[1] == "device":
                
                # udid
                # print("udid: %s" %sp[0])
                udid = sp[0]

                #android getprop
                getModelCmd = subprocess.check_output(r'%s -s %s shell getprop' %(ADB, udid), text=True)
                #print(getModelCmd)

                #get Name
                modelName = getModelReg.search(getModelCmd)
                
                #get OSversion
                OSversion = getOSVersionReg.search(getModelCmd)            

                #get PhoneNumCmd
                phoneNum = None
                iphonesubinfo = 5
                while phoneNum is None:
                    getPhoneNumCmd = subprocess.check_output(
                        "%s -s %s shell \"service call iphonesubinfo %i | cut -c 52-66 | tr -d '. [:space:]+'\""
                        %(ADB, udid, iphonesubinfo)
                        , text=True
                    )
                    #print(getPhoneNumCmd)
                    phoneNum = getPhoneNumReg.search(getPhoneNumCmd)
                    iphonesubinfo += 1
                    if phoneNum:
                        break
                    if iphonesubinfo >= 30:
                        print("PhoneNum not Found")
                        break

                if not OSversion:
                    print("OSversion Notfound")
                
                d = device()
                d.udid = udid
                d.phoneNum = phoneNum.group()
                d.modelName = modelName.group(1)
                d.OSVersion = OSversion.group(1)
                
                resultDict[d.udid] = d

    return resultDict


if __name__ == "__main__":

    devicesDict = dict()

    devicesDict.update(getDeviceInfo())


    for i in devicesDict:
        d = devicesDict.get(i)
        print("[%s] modelName: %s (Android %s) MDN: %s" %(d.udid, d.modelName, d.OSVersion, d.phoneNum))