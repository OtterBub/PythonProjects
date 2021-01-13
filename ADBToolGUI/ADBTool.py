import os
import re
import sys
import threading
import datetime
from multiprocessing import Process, Queue
from time import sleep

from custom import ADBcommand as adb

if __name__ == "__main__":
    devicesDict = dict()
    filenameDict = dict()
    select = True

    print("Devices Searching...")

    devicesDict.update(adb.getDeviceInfo(devicesDict))

    # main
    while True:
        adb.gPrintResult = ''
        devicesDict.update(adb.getDeviceInfo(devicesDict))
        
        for i in devicesDict:
            d:adb.device = devicesDict.get(i)
            
            if d.deviceStatus is adb.IDLE and d.connect:
                commandList = [
                    'logcat -v threadtime >> "./%s.log"' %(d.modelName + '-' + d.phoneNum)
                ]
                d.th = threading.Thread(target=adb.runCommand, args=(d, commandList,))
                d.th.setDaemon(True)
                d.th.start()

            if d.deviceStatus is adb.COMPLITE and not d.connect:
                d.deviceStatus = adb.IDLE

            addstr = [
                "[modelname] %s\n" %d.modelName
            ]
            adb.gPrintResult += adb.update(d, runCommandStatus= 'RECORDING LOG', addstatestr= addstr)
    
            #print("")
        os.system("cls")
        print(adb.gPrintResult)
        print("Continue. . .")
        sleep(0.5)
