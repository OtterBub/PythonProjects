import os
import re
import sys
import time
import tkinter
from tkinter import filedialog

class contact:
    def __init__(self):
        self.name = ""
        self.poc = ""
        self.mdn = ""
        self.time = ""
        self.duplication = list()

if __name__ == "__main__":
    
    appPath = ""

    if len(sys.argv) > 1:
        appPath = sys.argv[1]
    else:
    #    apkPath = r"C:\Users\User\Desktop\Python\AutoInstallAPK\ApiDemos-debug.apk"
        root = tkinter.Tk()
        root.withdraw()
        appPath = filedialog.askopenfilename(
            initialdir=".\\",
            parent=root, title="Select APK file",
            filetypes=(("APK Files","*.txt"),)
            )       

    if appPath == "":
        print("Need Select TXT File")
        input("Press Enter...")
        exit()
        
    f = open(appPath, mode='rt', encoding='utf-8')

    #Number Reg
    regNum = re.compile(r"([A-z]*[\d]?)[\-|\_|\s]{1,2}([\d]{3}[-|_|\s]?[\d]{3,4}[-|_|\s]?([\d]{4}))")

    #Name Reg
    regName = re.compile(r"([\d]{2}:[\d]{2})\s(\S{1,4})")
    contactDict = dict(str())
    name = str()
    time = str()

    while True:
        c:contact = contact()
        line = f.readline()
        #print(line)
        resultNum = regNum.search(line)
        resultName = regName.search(line)
        
        if resultName:
            #print(resultName.groups())
            nameGroup = resultName.group(2)
            time = resultName.group(1)
            name = nameGroup[len(nameGroup)-2:len(nameGroup)]
            #print(name)
        
        if resultNum:
            c.mdn = resultNum.group(2)

            # remove "-, space" in number
            c.mdn = re.sub(pattern=r"[\-|\s]", repl='', string=c.mdn)

            # Duplication Check (add Time Check)
            dup:contact = contactDict.get(c.mdn)
            if dup:
                if (type(dup) is contact):
                    dup.duplication.append(dup.time + ' ' + dup.name)
                    c = dup
                    print("%s 중복" %dup.name)
            
            c.poc = resultNum.group(1)   
            c.name = name
            c.time = time

            if len(c.poc) > 1:
                c.name += c.poc + "_" + resultNum.group(3)
            else:
                c.name += "_" + resultNum.group(3)

            
            contactDict[c.mdn] = c
            

        if not line: 
            f.close()
            break
        #else: input()

    # file write

    # txt to csv
    newFilePath = appPath[:len(appPath)-4] + '_Contact.csv'
    w = open(newFilePath, 'wt', encoding='utf-8')

    # csv file's title
    w.write("Last Name,Mobile Phone,Categories")

    # contact write
    for mdn in contactDict:
        c = contactDict.get(mdn)
        wstr = '\n%s,%s,myContacts' %(c.name + "_Today", c.mdn)
        w.write(wstr)
        print(wstr)
        if len(c.duplication) > 0:
            for dup in c.duplication:
                print("duplication: %s" %(dup))

    w.close()
    input("Complete Press Enter...")