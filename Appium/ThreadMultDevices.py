import unittest
import os
from appium import webdriver
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import NoSuchElementException
from multiprocessing import Process, Queue
import threading


def TestFunc(cap:dict = {}):

    debugStrUdid = '[%s] ' %(cap['udid'])
    print(debugStrUdid + 'MDN: %s Test Start' %(cap['phonenumber']))    

    # Set up appium
    # 그리고 desired_capabilities에 연결하려는 디바이스의 정보를 넣습니다.

    driver = webdriver.Remote(
        command_executor='http://127.0.0.1:4723/wd/hub',
        desired_capabilities=cap
        )

    Button1 = driver.find_element_by_xpath('//android.widget.TextView[@content-desc="Accessibility"]')
    Button1.click()

    Button2 = driver.find_element_by_xpath('//android.widget.TextView[@content-desc="Accessibility Node Querying"]')
    Button2.click()

    Button3 = driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.ListView/android.widget.LinearLayout[1]/android.widget.CheckBox')
    Button3.click()
    Button3.click()
    Button3.click()

    print(debugStrUdid + 'Test End')
    #sleep(10)

    driver.quit()

class TestThread:
    def __init__(self):
        self.ThreadList = []

    def AddDevice(self, FuncArgs:tuple = []):
        thread = Process(target=TestFunc, args=FuncArgs)
        self.ThreadList.append(thread)

    def StartDevice(self):
        for index, thread in enumerate(self.ThreadList):
            thread.start()

    def Join(self):
        for index, thread in enumerate(self.ThreadList):
            thread.join()



if __name__ == "__main__":

    T = TestThread()

    app = os.path.join(os.path.dirname(__file__), 'C:\\Users\\User\\Desktop\\업무\\Appium\\5. TestFiles', 'ApiDemos-debug.apk')
    app = os.path.abspath(app)

    cap1 = {
        'udid': '127.0.0.1:62001',
        'platformName': 'Android',
        'platformVersion': '7.1.2',
        'deviceName': 'Virtual',
        'automationName': 'Appium',
        'appPackage': 'io.appium.android.apis',
        'appActivity': 'io.appium.android.apis.ApiDemos',
        'newCommandTimeout': 300
    }
    cap1['phonenumber'] = '01011112222'

    T.AddDevice((cap1,))

    cap2 = {
        'udid': '127.0.0.1:62025',
        'platformName': 'Android',
        'platformVersion': '7.1.2',
        'deviceName': 'Virtual',
        'automationName': 'Appium',
        'appPackage': 'io.appium.android.apis',
        'appActivity': 'io.appium.android.apis.ApiDemos',
        'newCommandTimeout': 300
    }
    cap2['phonenumber'] = '01011112222'

    T.AddDevice((cap2,))

    T.StartDevice()
    T.Join()
    
    #test = unittest.TestLoader().loadTestsFromTestCase(code)
    #unittest.TextTestRunner(verbosity=2).run(test)
    print('Test End')
    pass