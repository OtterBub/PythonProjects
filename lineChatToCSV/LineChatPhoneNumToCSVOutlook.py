import os
import re
import sys
import time

if __name__ == "__main__":
    
    folderPath = 'C:\\Users\\User\\Desktop\\Python\\reg'
    appPath = os.path.join(os.path.dirname(__file__), folderPath , 'PhoneNumOri.txt')
    appPath = os.path.abspath(appPath)

    if len(sys.argv) > 1:
        appPath = sys.argv[1]
    
    print('reg practice')
    
    f = open(appPath, mode='rt', encoding='utf-8')

    #reg = re.compile(r"[\d]2\:[\d]2\s[\S]{2,5}([\S]*)[\s|\_ |\-]([\S]*\-[\S]*\-[\S]*)")
    #reg = re.compile(r"[\d]+\:[\d]+\s[\S]+\s([\S]*)[\s|\_ |\-]([\S]*\-[\S]*\-[\S]*)")

    regNum = re.compile(r"([\S]*)[\s|\_|\-]*([\S]{3}\-[\S]{3,4}\-([\S]{4}))")
    regNum2 = re.compile(r"([\d]{3}[\d]{3,4}([\d]{4}))")
    regNum3 = re.compile(r"([\d]{3}\-[\d]{3,4}\-([\d]{4}))")
    regName = re.compile(r"[\d]{2}\:[\d]{2}\s([\S]+)")
    contactList = list()
    name = "1"

    while(1):
        line = f.readline()
        #print(line)
        resultNum = regNum.search(line)
        resultName = regName.search(line)
        
        if resultName:
            #print(resultName.groups())
            nameGroup = resultName.group(1)
            name = nameGroup[len(nameGroup)-2:len(nameGroup)]
            #print(name)
        
        if resultNum:
            #print(resultNum.groups())
            backNum = resultNum.group(3)
            PhoneNum = resultNum.group(2)
            contactList.append(
                        name + '_' + backNum + ',' + PhoneNum + ',' + 'myContacts,'
            )
        else:
            resultNum = regNum2.search(line)
            if resultNum:
                print(resultNum.groups())
                backNum = resultNum.group(2)
                PhoneNum = resultNum.group(1)
                contactList.append(
                        name + '_' + backNum + ',' + PhoneNum + ',' + 'myContacts,'
                )
            else:
                resultNum = regNum3.search(line)
                if resultNum:
                    print(resultNum.groups())
                    backNum = resultNum.group(2)
                    PhoneNum = resultNum.group(1)
                    contactList.append(
                        name + '_' + backNum + ',' + PhoneNum + ',' + 'myContacts,'
                    )

        if not line: 
            f.close()
            break
        #else: input()
    
    newFilePath = appPath[:len(appPath)-4] + '_Contact.csv'
    w = open(newFilePath, 'wt', encoding='utf-8')

    w.write("Last Name,Mobile Phone,Categories,\n")
    

    for output in contactList:
        w.write(output+'\n')
        print(output)

    w.close()
    
    