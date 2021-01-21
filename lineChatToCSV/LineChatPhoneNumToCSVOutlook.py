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

    intro = """
    -------------- TEST ENC Park SungKyoung 20210121 --------------
    -------------- LineChat.txt (utf-8) To CSV File --------------
    """
    print(intro)
    
    appPath = ""
    contactsuffix = ""
    if len(sys.argv) > 1:
        appPath = sys.argv[1]
    else:
        root = tkinter.Tk()
        root.withdraw()
        appPath = filedialog.askopenfilename(
            initialdir=".\\",
            parent=root, title="Select txt file",
            filetypes=(("txt Files","*.txt"),)
            )       

    if appPath == "":
        print("Need Select TXT File")
        input("Press Enter...")
        exit(1)
    
    
    contactsuffix = input("Please enter the suffix you want suffix\n")
    if len(contactsuffix) > 0:
        contactsuffix = '_' + contactsuffix
        
    f = open(appPath, mode='rt', encoding='utf-8')

    # date Reg
    regDate = re.compile(r"^([\d]{4}).\s?([\d]{2}).\s?([\d]{2}).?")

    # Number Reg
    regNum = re.compile(r"([A-z]*[\d]?)[\-|\_|\s]{1,2}([\d]{3}[-|_|\s]?[\d]{3,4}[-|_|\s]?([\d]{4}))")

    regPhonenum = re.compile(r"([\d]{3}[-|_|\s]?[\d]{3,4}[-|_|\s]?([\d]{4}))")

    # Name Reg
    regName = re.compile(r"([\d]{2}:[\d]{2})\s(\S{1,4})")
    contactDict = dict(str())
    name = str()
    time = str()
    date = str()

    while True:
        c:contact = contact()
        line = f.readline()
        #print(line)
        resultName = regName.search(line)
        resultNum = regNum.search(line)
        resultPhoneNum = regPhonenum.search(line)
        resultDate = regDate.search(line)
        
        # 새로운 이름 찾았을 시 이름 갱신
        if resultName:
            #print(resultName.groups())
            nameGroup = resultName.group(2)
            time = resultName.group(1)
            name = nameGroup[len(nameGroup)-2:len(nameGroup)]
            #print(name)
        
        # 날짜 데이터 찾았을 시 날짜 갱신
        if resultDate:
            date = resultDate.group(1) + resultDate.group(2) + resultDate.group(3) + '_'
            # print(date)
        
        # 기존 양식일 경우 (이름POC_000-0000-0000)
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
                    # print("%s 중복" %dup.name)
            
            c.poc = resultNum.group(1)   
            c.name = name
            c.time = date + time

            if len(c.poc) > 1:
                c.name += c.poc + "_" + resultNum.group(3)
            else:
                c.name += "_" + resultNum.group(3)

            contactDict[c.mdn] = c
        
        # 기존 양식과 다를 경우 폰 번호 형식만 서칭 (000-0000-0000, 000-000-0000)
        elif resultPhoneNum:
            c.mdn = resultPhoneNum.group(1)

            # remove "-, space" in number
            c.mdn = re.sub(pattern=r"[\-|\s]", repl='', string=c.mdn)
            
            # Duplication Check (add Time Check)
            dup:contact = contactDict.get(c.mdn)
            if dup:
                if (type(dup) is contact):
                    dup.duplication.append(dup.time + ' ' + dup.name)
                    c = dup
                    # print("%s 중복" %dup.name)
            
            c.name = name + "_" + resultPhoneNum.group(2)
            c.time = date + time

            contactDict[c.mdn] = c
            
        # 파일 끝일경우 루프 종료
        if not line: 
            f.close()
            break
        #else: input()

    # 매칭 데이터가 0개일때 에러 메세지 출력 returncode 2
    if len(contactDict) <= 0 :
        print("Dont Search Contact Please input 'Naver Line Messenger' txt")
        input("Press Enter Key...")
        exit(2)


    # file write

    # txt to csv
    newFilePath = appPath[:len(appPath)-4] + '_Contact.csv'
    convertResult = appPath[:len(appPath)-4] + '_ConvertResult.txt'
    w = open(newFilePath, 'wt', encoding='utf-8')
    resultw = open(convertResult, 'wt', encoding='utf-8')

    # csv file's title
    w.write("Last Name,Mobile Phone,Categories")

    # contact write
    for mdn in contactDict:
        c = contactDict.get(mdn)
        wstr = '\n%s,%s,myContacts' %(c.name + contactsuffix, c.mdn)
        w.write(wstr)

        r = wstr.strip(",myContacts") + '/ Last Date: ' + c.time
        resultw.write(r)
        print(r, end='')
        if len(c.duplication) > 0:
            print()
            resultw.write('\n')
            c.duplication.reverse()
            for dup in c.duplication:
                r = "duplication: %s\n" %(dup)
                resultw.write(r)
                print(r, end='')
    w.close()
    
    r = "\n\n--- Found Contact: %s" %(len(contactDict)) + "---\n"
    print(r, end='')
    resultw.write(r)
    resultw.close()
    input("Complete Press Enter...")
    exit(0)