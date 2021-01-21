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
        gPrintResult += "----------- by TEST ENC ParkSungKyoung 210120 ----------\n"
        gPrintResult += "----------- Packet Capture ----------\n\n"
        devicesDict.update(adb.getDeviceInfo(devicesDict))
        #print("")
        #print("----Installed Devices History Status----")

        # Install APK
        for i in devicesDict:
            d:adb.device = devicesDict.get(i)
            #print("[%s] modelName: %s (Android %s) / MDN: %s / status: %i" %(d.udid, d.modelName, d.OSVersion, d.phoneNum, d.deviceStatus))
            gPrintResult += adb.update(d, "CAPTURRING PACKETS", repeat= True)
            
            # ------ command List ------
            commandList = [
                'root',
                'shell tcpdump -i any -p -s 0 -w "/sdcard/%s.pcap"' %(d.phoneNum + '_' + d.modelName)
            ]

            if (d.deviceStatus is adb.COMPLITE) or (not d.connect):
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
        sleep(0.5)
