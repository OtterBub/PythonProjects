import copy
import os
import re
import subprocess
import sys
import threading
import tkinter
from multiprocessing import Process, Queue
from time import sleep
from tkinter import filedialog
from typing import Any, Callable, List, Mapping, Optional, Tuple

import traceback

#CONST
#INSTALL STATUS
IDLE = 0
RUNCOMMAND = 1
COMPLITE = 2

#ADB NAME
ADB = "adb"

if os.path.isfile(os.path.dirname(sys.argv[0]) + "/nox.txt"):
    print("Active nox_adb")
    sleep(1)
    ADB = "nox_adb"


#Reg
getModelReg = re.compile(r"model]:\s\[([\S]*)\]")
getOSVersionReg = re.compile(r"version.release]:\s\[([\S]*)\]")
getPhoneNumReg = re.compile(r"8?[2|0]0?1[8|7|0|1][\d]*")

#GLOBAL
gPrintResult = ""


class device:
    def __init__(self):
        self.installed = False
        self.connect = False
        self.deviceStatus = IDLE
        
        self.modelName = "None"
        self.udid = "None"
        self.OSVersion = "None"
        self.phoneNum = "None"
        self.th = threading.Thread()
        self.count = 1

        self.printStatus = "None"

    def getInfoStr(self) -> str:
        return self.printStatus


class thrList:
    def __init__(self):
        self.ThreadList = []

    def addThread(self, funcTarget:Optional[Callable[..., Any]] = ... ,funcArgs:tuple = []):        
        thr = threading.Thread(target=funcTarget, args=funcArgs)
        self.ThreadList.append(thr)

    def startThread(self):
        for thr in self.ThreadList:
            thr.start()

    def join(self):
        for thr in self.ThreadList:
            thr.join()

    def clear(self):
        self.ThreadList.clear()
            

def getDeviceInfo(origDict:dict() = None):
    resultDict = dict()

    if origDict:
        resultDict = origDict

    for i in resultDict:
        d:device = resultDict.get(i)
        d.connect = False
    
    getCmdResult = subprocess.check_output('%s devices' %(ADB), text=True)
    getDevices = getCmdResult.splitlines()

    #print("----Current Connected Device List Status----")
    
    # Devices List Get
    for reSplit in getDevices:
        sp = reSplit.split('\t')
        #print(sp)
        if len(sp) >= 2:
            if sp[1] == "device":
                
                # udid
                # print("udid: %s" %sp[0])
                udid = sp[0]

                if resultDict.get(udid):
                    tempd:device = resultDict.get(udid)
                    tempd.connect = True
                    status = tempd.deviceStatus
                    if status is COMPLITE:
                        #print("[%s] %s (MDN:%s) is COMPLITE" %(tempd.udid, tempd.modelName, tempd.phoneNum))
                        continue
                    elif status is IDLE:
                        #print("[%s] %s (MDN:%s) is IDLE" %(tempd.udid, tempd.modelName, tempd.phoneNum))
                        continue
                    elif status is RUNCOMMAND:
                        #print("[%s] %s (MDN:%s) is RUNCOMMAND" %(tempd.udid, tempd.modelName, tempd.phoneNum))
                        continue

                #android getprop
                try:
                    getModelCmd = subprocess.check_output(r'%s -s %s shell getprop' %(ADB, udid), text=True)
                except subprocess.CalledProcessError:
                    print("[%s] shell getprop Command Failed" %(udid))
                #print(getModelCmd)

                #get Name
                modelName = getModelReg.search(getModelCmd)
                
                #get OSversion
                OSversion = getOSVersionReg.search(getModelCmd)            

                #get PhoneNumCmd
                phoneNum = None
                iphonesubinfo = 5

                try:
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
                            #print("PhoneNum not Found")
                            break
                except subprocess.CalledProcessError:
                    print("[%s] shell call iphonesubinfo Command Failed" %(udid))

                if not OSversion:
                    print("OSversion Notfound")
                
                d = device()
                d.udid = udid
                d.connect = True
                if phoneNum:
                    d.phoneNum = phoneNum.group()
                if modelName:
                    d.modelName = modelName.group(1)
                if OSversion:
                    d.OSVersion = OSversion.group(1)
                
                resultDict[d.udid] = d

    return resultDict

def update(d:device = None, runCommandStatus:str = "RUNNING COMMAND", repeat:bool = False):
    
    d.printStatus = ""

    if(d.connect):
        d.printStatus += "CONNECT\n"
    else:
        d.printStatus += "\n"

    d.printStatus += "[%s] modelName: %s (Android %s) / MDN: %s" %(d.udid, d.modelName, d.OSVersion, d.phoneNum)
    d.printStatus += "\n- status: "
    if d.deviceStatus is IDLE:
        d.printStatus += "IDLE"
    elif d.deviceStatus is RUNCOMMAND:
        d.printStatus += runCommandStatus + "." * d.count
        d.count = (d.count + 1) % 4
    elif d.deviceStatus is COMPLITE:
        d.printStatus += "COMPLITE"

    

    d.printStatus += "\n\n"

    return d.printStatus


def commandRun(d:device = None, cmd:list = None):
    if (not d) or (not cmd):
        return False

    if not isinstance(d, device):
        return False

    if (d.installed is True) or (d.deviceStatus is COMPLITE):
        #print("[%s / %s] already COMPLITE" %(d.udid, d.modelName))
        return False
    elif d.deviceStatus is RUNCOMMAND:
        #print("[%s / %s] Current RUN COMMAND" %(d.udid, d.modelName))
        return False

    # command run
    try:
        d.deviceStatus = RUNCOMMAND

        for c in cmd:
            os.system('%s -s %s %s' %(ADB, d.udid, c))

        #print("[%s / %s] Install Success" %(d.udid, d.modelName))
    except subprocess.CalledProcessError:
        d.deviceStatus = IDLE
        traceback.print_exc()
        print("subprocess.CalledProcessError")
        return False
    except:
        d.deviceStatus = IDLE
        traceback.print_exc()
        print("except")
        return False
    
    d.installed = True
    d.deviceStatus = COMPLITE
    return True