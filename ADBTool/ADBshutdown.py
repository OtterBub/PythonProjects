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
    select = True

    print("Devices Searching...")
    # Main
    while select:
        # print init
        gPrintResult = ""
        gPrintResult += "----------- by TEST ENC ParkSungKyoung 211020 ----------\n"
        gPrintResult += "----------- ADBcommand Module Ver: %s ----------\n" %(adb.VERSION)
        gPrintResult += "----------- shell reboot -p ----------\n\n"
        devicesDict.update(adb.getDeviceInfo(devicesDict))

        # Install APK
        for i in devicesDict:
            d:adb.device = devicesDict.get(i)

            # ------ command List ------
            commandList = [
                "shell reboot -p"
            ]

            # ------ update ------
            gPrintResult += adb.update(d, runCommandStatus= 'Shutdown Device', repeat= False)
            adb.runThread(d= d, func= adb.runCommand, a= (d, commandList))

            

        os.system("cls")
        print(gPrintResult)
        print("Continue. . .")
        sleep(1)
