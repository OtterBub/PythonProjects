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
        gPrintResult += "----------- by TEST ENC ParkSungKyoung 210405 ----------\n"
        gPrintResult += "----------- ADBcommand Module Ver: %s ----------\n" %(adb.VERSION)
        gPrintResult += "----------- Install %s ----------\n\n" %(appname)
        devicesDict.update(adb.getDeviceInfo(devicesDict))

        # Install APK
        for i in devicesDict:
            d:adb.device = devicesDict.get(i)

            # ------ command List ------
            commandList = [
                'install -r -d "%s"' %(apkPath)
            ]

            # ------ Update ------
            gPrintResult += adb.update(d, runCommandStatus= 'INSTALLING', repeat= False)
            adb.runThread(d= d, func= adb.runCommand, a= (d, commandList))

            


            #print("")
        os.system("cls")
        print(gPrintResult)
        print("Continue. . .")
        sleep(0.5)
