import copy
import os
import re
import subprocess
import sys
import threading
import unittest
from multiprocessing import Process, Queue
from time import sleep

from appium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def TestFunc(cap:dict = {}):

    debugStrUdid = '[%s] ' %(cap.get('udid'))
    print(debugStrUdid + 'MDN: %s Test Start' %(cap.get('phonenumber')))    

    # Set up appium

    driver = webdriver.Remote(
        command_executor='http://127.0.0.1:4723/wd/hub',
        desired_capabilities=cap
        )

    if  driver.is_app_installed('io.appium.android.apis'):
        driver.activate_app('io.appium.android.apis')
    elif cap.get('appPath'): 
        driver.install_app(cap.get('appPath'))
    else:
        print(debugStrUdid + "Test Failed Can't install app")
        driver.quit()


    Button1 = driver.find_element_by_xpath('//android.widget.TextView[@content-desc="Accessibility"]')
    Button1.click()

    Button2 = driver.find_element_by_xpath('//android.widget.TextView[@content-desc="Accessibility Node Querying"]')
    Button2.click()

    Button3 = driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.ListView/android.widget.LinearLayout[1]/android.widget.CheckBox')
    Button3.click()
    Button3.click()
    Button3.click()

    #driver.terminate_app("io.appium.android.apis")
    print(debugStrUdid + 'Test End')
    #sleep(10)

    driver.quit()

def getCaplistByDevice(app:str = ''):
    capList = list()
    cap = {
        'udid': '127.0.0.1:62025',
        'platformName': 'Android',
        'platformVersion': '7.1.2',
        'deviceName': 'Virtual',
        'automationName': 'Appium',
        'newCommandTimeout': 300
    }

    if len(app) > 0:
        cap['appPath'] = app

    cap['appPackage'] = 'io.appium.android.apis'
    cap['appActivity'] ='io.appium.android.apis.ApiDemos'
    cap['app'] = app

    getCmdResult = subprocess.check_output('adb devices', text=True)

    getDevices = getCmdResult.splitlines()

    print("---devices----")
    
    # Devices List Get
    for reSplit in getDevices:
        #print(reSplit)
        sp = reSplit.split('\t')
        
        if len(sp) >= 2:
            if sp[1] == "device":
                
                # udid
                print("udid: %s" %sp[0])
                cap['udid'] = sp[0]
                

                #android version
                getCmdResult = subprocess.check_output('adb -s %s shell "getprop | grep ro.build.version.release"' %(sp[0]), text=True)
    
                getprop = getCmdResult.splitlines()

                print("---getprop---")
                
                for reSplit in getprop:
                    print(reSplit)
                    reg = re.compile(r'\[(\S+)\]:\s\[(\S+)\]')
                    comResult = reg.match(reSplit)
                    if comResult: 
                        print(comResult.group(2))
                        cap['platformVersion'] = comResult.group(2) 
                    else: print("comResult is None")

                capList.append(copy.deepcopy(cap))

    return capList


class TestThread:
    def __init__(self):
        self.ThreadList = []

    def AddDevice(self, FuncArgs:tuple = []):
        thr = Process(target=TestFunc, args=FuncArgs)
        self.ThreadList.append(thr)

    def StartDevice(self):
        for thr in self.ThreadList:
            thr.start()

    def Join(self):
        for thr in self.ThreadList:
            thr.join()



if __name__ == "__main__":

    appPath = os.path.join(os.path.dirname(__file__), 'C:\\Users\\User\\Desktop\\업무\\Appium\\5. TestFiles', 'ApiDemos-debug.apk')
    appPath = os.path.abspath(appPath)
    
    capList = getCaplistByDevice(app = appPath)

    T = TestThread()
    
    for device in capList:
        T.AddDevice((device,))

    T.StartDevice()
    T.Join()


    print('\nTest End')
