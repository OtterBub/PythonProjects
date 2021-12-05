import os
import re
import sys
import threading
import datetime
from multiprocessing import Process, Queue
from time import sleep

from custom import ADBcommand as adb
from custom import quickEditMode

# Patch History
''' 
210906
번호_단말명(OS버전)_날짜시간.log -> 단말명(OS버전)_번호_날짜시간.log 으로 변경
'''

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
        gPrintResult += "----------- by TEST ENC ParkSungKyoung 210906 ----------\n"
        gPrintResult += "----------- ADBcommand Module Ver: %s ----------\n" %(adb.VERSION)
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
            filepath = './%s.log' %(d.modelName + '(' + d.OSVersion + ')' + '_' + d.phoneNum + '_' + now.strftime("%Y%m%d%H%M%S"))

            commandList = [
                'logcat -v threadtime >> "%s"' %(filepath)
            ]

            # ------ Get Log File Size ------

            # found logFilename
            if not filenameDict.get(d.udid):
                rpath = os.path.realpath(filepath)
                filenameDict[d.udid] = rpath
            
            # Logfile Size Update
            if os.path.isfile(filenameDict.get(d.udid)):
                d.customString = "LogSize: %.2f KB" %(os.path.getsize(filenameDict.get(d.udid)) / (1024.0))
            else:
                d.customString = " "

            if (d.deviceStatus is adb.COMPLITE) or (not d.connect):
                filenameDict[d.udid] = None

            # ------ Update ------
            gPrintResult += adb.update(d, runCommandStatus= 'RECORDING LOG', repeat= True)
            adb.runThread(d= d, func= adb.runCommand, a= (d, commandList))

        os.system("cls")
        print(gPrintResult)
        print("Continue. . .")
        sleep(1)
