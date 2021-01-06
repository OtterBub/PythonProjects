import os
import re
import sys
import threading
import datetime
import tkinter
from multiprocessing import Process, Queue
from time import sleep

from custom import ADBcommand as adb
from custom import quickEditMode

if __name__ == "__main__":
    quickEditMode.disable_quickedit()
    apkPath = ""
    
    if len(sys.argv) > 1:
        apkPath = sys.argv[1]
    else:
        # apkPath = r"C:\Users\User\Desktop\Python\AutoInstallAPK\ApiDemos-debug.apk"
        root = tkinter.Tk()
        root.withdraw()
        apkPath = tkinter.filedialog.askopenfilename(
            initialdir=".\\",
            parent=root, title="Select APK file",
            filetypes=(("APK Files","*.apk"),)
            )       

    if apkPath == "":
        print("Need Select APK File")
        input("Press Enter...")
        exit()

    appname = os.path.split(apkPath)[1]
    devicesDict = dict()
    select = True

    print("Devices Searching...")
    # Main
    while select:
        # print init
        gPrintResult = ""
        gPrintResult += "----------- by TEST ENC ParkSungKyoung 210107 ----------\n"
        gPrintResult += "----------- Install %s ----------\n\n" %(appname)
        devicesDict.update(adb.getDeviceInfo(devicesDict))
        #print("")
        #print("----Installed Devices History Status----")

        # Install APK
        for i in devicesDict:
            d:adb.device = devicesDict.get(i)
            #print("[%s] modelName: %s (Android %s) / MDN: %s / status: %i" %(d.udid, d.modelName, d.OSVersion, d.phoneNum, d.deviceStatus))
            gPrintResult += adb.update(d, runCommandStatus= 'INSTALLING', repeat= False)
            
            now = datetime.datetime.now()


            # ------ command List ------
            commandList = [
                'install -r -d %s' %(apkPath)
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
