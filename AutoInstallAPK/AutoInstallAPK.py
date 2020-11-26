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

#GLOBAL
gPrintResult = ""


class device:
    def __init__(self):
        self.installed = False
        self.connect = False
        self.installStatus = IDLE
        
        self.modelName = "None"
        self.udid = "None"
        self.OSVersion = "None"
        self.phoneNum = "None"
        self.th = threading.Thread()

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
                    status = tempd.installStatus
                    if status is COMPLITE:
                        #print("[%s] %s (MDN:%s) is COMPLITE" %(tempd.udid, tempd.modelName, tempd.phoneNum))
                        continue
                    elif status is IDLE:
                        #print("[%s] %s (MDN:%s) is IDLE" %(tempd.udid, tempd.modelName, tempd.phoneNum))
                        continue
                    elif status is INSTALLING:
                        #print("[%s] %s (MDN:%s) is INSTALLING" %(tempd.udid, tempd.modelName, tempd.phoneNum))
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

def update(d:device = None):
    
    d.printStatus = ""

    if(d.connect):
        d.printStatus += "CONNECT\n"

    d.printStatus += "[%s] modelName: %s (Android %s) / MDN: %s" %(d.udid, d.modelName, d.OSVersion, d.phoneNum)
    d.printStatus += "\n- status: "
    if d.installStatus is IDLE:
        d.printStatus += "IDLE"
    elif d.installStatus is INSTALLING:
        d.printStatus += "INSTALLING"
    elif d.installStatus is COMPLITE:
        d.printStatus += "COMPLITE"

    d.printStatus += "\n\n"

    return d.printStatus


def apkInstall(d:device = None, path:str = None):
    if (not d) or (not path):
        return False

    if not isinstance(d, device):
        return False

    if (d.installed is True) or (d.installStatus is COMPLITE):
        #print("[%s / %s] already COMPLITE" %(d.udid, d.modelName))
        return False
    elif d.installStatus is INSTALLING:
        #print("[%s / %s] Current Installing" %(d.udid, d.modelName))
        return False

    try:
        d.installStatus = INSTALLING
        subprocess.check_output('%s -s %s install -d -r "%s"' %(ADB, d.udid, path))
        #print("[%s / %s] Install Success" %(d.udid, d.modelName))
    except subprocess.CalledProcessError:
        d.installStatus = IDLE
        return False
    
    d.installed = True
    d.installStatus = COMPLITE
    return True


if __name__ == "__main__":

    apkPath = str()
    if len(sys.argv) > 1:
        apkPath = sys.argv[1]
    else:
    #    apkPath = r"C:\Users\User\Desktop\Python\AutoInstallAPK\ApiDemos-debug.apk"
        print("Need Argument")
        exit()

    appNameReg = re.compile(r".*\\(.*[.]apk)$")

    appName = appNameReg.match(apkPath).group(1)

    devicesDict = dict()
    select = True

    # Main
    while select:
        # print init
        gPrintResult = ""
        gPrintResult += "----------- AUTO INSTALL [%s] ----------\n\n" %appName
        devicesDict.update(getDeviceInfo(devicesDict))
        #print("")
        #print("----Installed Devices History Status----")

        # Install APK
        for i in devicesDict:
            d:device = devicesDict.get(i)
            #print("[%s] modelName: %s (Android %s) / MDN: %s / status: %i" %(d.udid, d.modelName, d.OSVersion, d.phoneNum, d.installStatus))
            gPrintResult += update(d)

            if d.installStatus is COMPLITE:
                #print("[%s / %s] %s APK Install Success" %(d.udid, d.modelName, appName))
                #print("")
                continue

            if d.th:
                if d.installStatus is INSTALLING:
                    #print("[%s / %s] Current APK Installing" %(d.udid, d.modelName))
                    #print("")
                    continue

                if d.th.is_alive():
                    #print("[%s / %s] d.th.is_alive() is True" %(d.udid, d.modelName))
                    #print("")
                    continue
                else:
                    d.th = threading.Thread(target=apkInstall, args=(d, apkPath))
                    d.th.setDaemon(True)
                    d.th.start()
            else:
                d.th = threading.Thread(target=apkInstall, args=(d, apkPath))
                d.th.setDaemon(True)
                d.th.start()

            #print("")
        print(gPrintResult)
        print("Continue. . .")
        sleep(1)
        os.system("cls")