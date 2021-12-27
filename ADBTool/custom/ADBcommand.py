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
from typing import Any, Callable, List, Mapping, Optional, Tuple, Iterable

import traceback

# CONST VAL
# ADB MODULE VERSION
# (Major).(BuildDate).(Minor)
VERSION = '0.211227.1'

# Patch History
# 211227
# shell get prop command 중 한글 포함 시 디바이스 정보 못 불러오는 문제 해결
#
# 211013
# Patch History 파이썬 파일에 기록 시작
# Add Display Font Color
#

# INSTALL STATUS
IDLE = 0
RUNCOMMAND = 1
COMPLITE = 2
KEYINTERRUPT = 3
ERROR = 4

# ADB NAME
ADB = "adb"

# Debug for Nox(VM) ADB
if os.path.isfile(os.path.dirname(sys.argv[0]) + "/nox.txt"):
    print("Active nox_adb")
    sleep(1)
    ADB = "nox_adb"


# Reg
getModelReg = re.compile(r"model]:\s\[([\S]*)\]")
getOSVersionReg = re.compile(r"version.release]:\s\[([\S]*)\]")
getBuildTypeReg = re.compile(r"build.type]:\s\[([\S]*)\]")
getBuildTagsReg = re.compile(r"build.tags]:\s\[([\S]*)\]")
getPhoneNumReg = re.compile(r"8?[2|0]0?1[8|7|0|1][\d]*")

# GLOBAL
# Display Result for Print
gPrintResult = ""


class device:
    def __init__(self):
        self.connect = False
        self.deviceStatus = IDLE
        self.errorcode = "None"
        
        self.modelName = "None"
        self.udid = "None"
        self.OSVersion = "None"
        self.phoneNum = "None"
        self.buildtype = "None"
        self.buildtags = "None"
        self.th = threading.Thread()
        self.count = 1

        self.printStatus = "None"

        self.customData = None
        self.customString = None
        self.customErrorString = None

    def getInfoStr(self) -> str:
        return self.printStatus


class thrList:
    def __init__(self):
        self.ThreadList = []

    def addThread(self, funcTarget= None,
                        funcArgs= None,
                        funcKwargs= None):
        thr = threading.Thread(target=funcTarget, args=funcArgs, kwargs=funcKwargs)
        self.ThreadList.append(thr)
    
    def addThread_t(self, thr:threading.Thread = None):
        if thr:
            self.ThreadList.append(thr)

    def startThread(self):
        for thr in self.ThreadList:
            thr.start()

    def join(self):
        for thr in self.ThreadList:
            thr.join()

    def clear(self):
        self.ThreadList.clear()

def findPhoneNum(d:device = None, iphonesubinfo:int= 1 ):
    phoneNum = None

    try:
        getPhoneNumCmd = subprocess.check_output(
            "%s -s %s shell \"service call iphonesubinfo %i | cut -c 52-66 | tr -d '. [:space:]+'\""
            %(ADB, d.udid, iphonesubinfo)
            , text=True
        )
        #print(getPhoneNumCmd)
        phoneNum = getPhoneNumReg.search(getPhoneNumCmd)
        
    except subprocess.CalledProcessError:
        print("[%s] shell call iphonesubinfo Command Failed" %(d.udid))

    if phoneNum:
        d.phoneNum = phoneNum.group()

            

def getDeviceInfo(origDict:dict() = None):
    resultDict = dict()

    if origDict:
        resultDict = origDict

    for i in resultDict:
        d:device = resultDict.get(i)
        d.connect = False
    try:
        getCmdResult = subprocess.check_output('%s devices' %(ADB), text=True)
        getDevices = getCmdResult.splitlines()
    except:
        return resultDict

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
                    continue

                #android getprop
                try:
                    setcmd = (r'%s -s %s shell getprop' %(ADB, udid))
                    getModelCmd = subprocess.check_output(setcmd, text=True, encoding='UTF8')
                except subprocess.CalledProcessError:
                    print("[%s] subprocess.CalledProcessError" %(udid))
                except :
                    traceback.print_exc()
                    print("[%s] shell getprop Command Failed" %(udid))
                    
                    d = device()
                    d.errorcode = "getprop Error"
                    d.customErrorString = "\033[91m" + "shell getprop Command Failed" + "\033[0m"
                    
                    d.udid = udid
                    d.connect = True
                    resultDict[d.udid] = d
                    continue

                #print(getModelCmd)

                # get Name
                modelName = getModelReg.search(getModelCmd)
                
                # get OSversion
                OSversion = getOSVersionReg.search(getModelCmd)    

                # get build type,tags
                buildtype = getBuildTypeReg.search(getModelCmd)
                buildtags = getBuildTagsReg.search(getModelCmd)

                d = device()

                d.udid = udid
                d.connect = True
                # if phoneNum:
                #     d.phoneNum = phoneNum.group()
                if modelName:
                    d.modelName = modelName.group(1)
                if OSversion:
                    d.OSVersion = OSversion.group(1)
                if buildtype:
                    d.buildtype = buildtype.group(1)
                if buildtags:
                    d.buildtags = buildtags.group(1)

                # FindPhoneNum multi thread
                tlist = thrList()
                for i in range(1, 31):
                    tlist.addThread(funcTarget= findPhoneNum, funcArgs= (d,i,))
                
                tlist.startThread()
                tlist.join()
                
                resultDict[d.udid] = d

    return resultDict

def update(d:device = None, runCommandStatus:str = "RUNNING COMMAND", repeat:bool = False, addstatestr:list = None):
    
    d.printStatus = ""

    if(d.connect):
        d.printStatus += "\033[92m" + "CONNECT" + "\033[0m"
    elif (d.deviceStatus not in [IDLE, COMPLITE]):
        d.deviceStatus = ERROR
    else:
        d.printStatus += "\033[91m" + "DISCONNECT" + "\033[0m"
    
    # add customErrorString
    if d.customErrorString and (len(d.customErrorString) > 0):
        d.printStatus += " - "
        d.printStatus += d.customErrorString
        d.printStatus += "\n"
    else:
        d.printStatus += "\n"


    d.printStatus += "[%s] modelName: %s (Android %s) / PhoneNumber: %s" %(d.udid, d.modelName, d.OSVersion, d.phoneNum)
    d.printStatus += "\nBuildInfo: [Tags: (%s)] [Type: (%s)]" %(d.buildtags, d.buildtype)
    d.printStatus += "\n- status: "
    if d.deviceStatus is IDLE:
        d.printStatus += "IDLE"
    elif d.deviceStatus is RUNCOMMAND:
        d.printStatus += runCommandStatus + "." * d.count
        d.count = (d.count + 1) % 4
    elif d.deviceStatus is COMPLITE:
        d.printStatus += "COMPLETE"
    elif d.deviceStatus is ERROR:
        d.printStatus += "\033[91m" + "ERROR: " + "\033[0m"
        d.printStatus += d.errorcode
    elif d.deviceStatus is KEYINTERRUPT:
        d.printStatus += "KEYINTERRUPT"

    # changed state to IDLE for repeat command
    if (repeat and (d.deviceStatus is COMPLITE) and (d.connect is False)) or ((d.connect is False) and (d.deviceStatus is ERROR)):
        d.deviceStatus = IDLE
    
    

    # Add StateString
    if addstatestr:
        for a in addstatestr:
            d.printStatus += a
    else:
        d.printStatus += "\n"

    if d.customString and (len(d.customString) > 0):
        d.printStatus += d.customString
        d.printStatus += "\n"

    d.printStatus += "\n"

    return d.printStatus

def runThread(d:device = None, func: Optional[Callable[..., Any]] = ..., a: Iterable[Any] = ...):
    if(d.deviceStatus is COMPLITE) or (not d.connect):
        return False

    if d.th:
        if (d.deviceStatus is RUNCOMMAND) or d.th.is_alive():
            # Thread가 실행중이고 device 상태가 RUNCOMMAND면 패스
            return False

        else:
            d.th = threading.Thread(target=func, args=a)
            d.th.setDaemon(True)
            d.th.start()
    else:
        d.th = threading.Thread(target=func, args=a)
        d.th.setDaemon(True)
        d.th.start()
    
    return True


def runCommand(d:device = None, cmd:list = None):
    if (not d) or (not cmd):
        return False

    if d.deviceStatus in [COMPLITE, RUNCOMMAND, KEYINTERRUPT, ERROR]:
        #print("[%s / %s] already COMPLITE" %(d.udid, d.modelName))
        return False

    # command run
    try:
        d.deviceStatus = RUNCOMMAND
        # os.system('echo off')
        # for c in cmd:
        #    os.system('%s -s %s %s' %(ADB, d.udid, c))
        
        for c in cmd:
            r = subprocess.run('%s -s %s %s' %(ADB, d.udid, c), shell=True, text=True)
            if r.returncode != 0:
                d.errorcode = "%d" %r.returncode
                d.deviceStatus = ERROR
                return False

        #print("[%s / %s] Install Success" %(d.udid, d.modelName))
    except subprocess.CalledProcessError:
        d.deviceStatus = ERROR
        # traceback.print_exc()
        print("subprocess.CalledProcessError")
        return False
    except KeyboardInterrupt:
        d.deviceStatus = KEYINTERRUPT
        return True
    except:
        d.deviceStatus = ERROR
        # traceback.print_exc()
        print("except")
        return False
    
    d.deviceStatus = COMPLITE
    return True