import os
import re
import sys
import threading
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
        gPrintResult += "----------- by TEST ENC ParkSungKyoung 210405 ----------\n"
        gPrintResult += "----------- ADBcommand Module Ver: %s ----------\n" %(adb.VERSION)
        gPrintResult += "----------- Packet Capture ----------\n\n"
        devicesDict.update(adb.getDeviceInfo(devicesDict))

        # Install APK
        for i in devicesDict:
            d:adb.device = devicesDict.get(i)
            
            # ------ command List ------
            commandList = [
                'root',
                'shell tcpdump -i any -p -s 0 -w "/sdcard/%s.pcap"' %(d.phoneNum + '_' + d.modelName)
            ]

            # ------ Update ------
            gPrintResult += adb.update(d, "CAPTURRING PACKETS", repeat= True)
            adb.runThread(d, func= adb.runCommand, a= (d, commandList))

        os.system("cls")
        print(gPrintResult)
        print("Continue. . .")
        sleep(0.5)
