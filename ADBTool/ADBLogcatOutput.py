import os
import re
import sys
import threading
import datetime
from multiprocessing import Process, Queue
from time import sleep

from custom import ADBcommand as adb
from custom import quickEditMode

if __name__ == "__main__":
    quickEditMode.disable_quickedit()
    devicesDict = dict()
    filenameDict = dict()
    select = True

    print("Devices Searching...")
    # Main
    while select:
        # print init
        gPrintResult = ""
        gPrintResult += "----------- by TEST ENC ParkSungKyoung 210120 ----------\n"
        gPrintResult += "----------- Recording Logcat ----------\n\n"
        devicesDict.update(adb.getDeviceInfo(devicesDict))
        #print("")
        #print("----Installed Devices History Status----")

        # Install APK
        for i in devicesDict:
            d:adb.device = devicesDict.get(i)
            #print("[%s] modelName: %s (Android %s) / MDN: %s / status: %i" %(d.udid, d.modelName, d.OSVersion, d.phoneNum, d.deviceStatus))

            # ------ command List ------
            now = datetime.datetime.now()
            filepath = './%s.log' %(d.phoneNum + '_' + d.modelName + '(' + d.OSVersion + ')' + '_' + now.strftime("%Y%m%d%H%M%S"))

            commandList = [
                'logcat -v threadtime >> "%s"' %(filepath)
            ]

            # ------ update ------
            
            if not filenameDict.get(d.udid):
                rpath = os.path.realpath(filepath)
                filenameDict[d.udid] = rpath
            
            if os.path.isfile(filenameDict.get(d.udid)):
                result = "\n%.2f KB\n" %(os.path.getsize(filenameDict.get(d.udid)) / (1024.0))
            else:
                result = "\nNone\n"

            statestrList = [
                result
            ]

            gPrintResult += adb.update(d, runCommandStatus= 'RECORDING LOG', repeat= True, addstatestr= statestrList)


            if (d.deviceStatus is adb.COMPLITE) or (not d.connect):
                filenameDict[d.udid] = None
                #print("[%s / %s] %s APK Install Success" %(d.udid, d.modelName, appName))
                #print("")
                continue

            if d.th:
                if d.deviceStatus is adb.RUNCOMMAND:
                    #print("[%s / %s] Current APK Installing" %(d.udid, d.modelName))
                    #print("")
                    continue

                if d.th.is_alive():
                    #print("[%s / %s] d.th.is_alive() is True" %(d.udid, d.modelName))
                    #print("")
                    continue
                else:
                    d.th = threading.Thread(target=adb.runCommand, args=(d, commandList))
                    d.th.setDaemon(True)
                    d.th.start()
            else:
                d.th = threading.Thread(target=adb.runCommand, args=(d, commandList))
                d.th.setDaemon(True)
                d.th.start()

            #print("")
        os.system("cls")
        print(gPrintResult)
        print("Continue. . .")
        sleep(1)
