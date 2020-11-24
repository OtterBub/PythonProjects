import unittest
import os
from appium import webdriver
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import NoSuchElementException

class TestCode(unittest.TestCase):
    def setUp(self):
        
        # Kakao Game SDK Test App 경로
        app = os.path.join(os.path.dirname(__file__), 'C:\\Users\\User\\Desktop\\업무\\Appium\\5. TestFiles', 'ApiDemos-debug.apk')
        app = os.path.abspath(app)

        # Set up appium
        # Appium 서버의 포트는 4001로 지정합니다.
        # 그리고 desired_capabilities에 연결하려는 디바이스(V10)의 정보를 넣습니다.
        cap = {
                'app': app,
                'platformName': 'Android',
                'platformVersion': '7.1.2',
                'deviceName': '127.0.0.1:62001 (7.1.2)',
                'automationName': 'Appium',
                'appPackage': 'io.appium.android.apis',
                'appActivity': 'io.appium.android.apis.ApiDemos',
                'newCommandTimeout': 300
                #'udid': 'LGF600Kb1134738'
            }

        self.driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4723/wd/hub',
            desired_capabilities=cap
            )

        

    def test_search_field(self):

        # appiun의 webdriver를 초기화 합니다.
        driver = self.driver

        # selenium의 WebDriverWait을 사용합니다. element가 나올때 까지 최고 20초까지 기다립니다.
        wait = WebDriverWait(driver, 20)
        
        #Button1 = wait.until(EC.element_to_be_clickable((By.ID, 'android:id/text1')))
        #Button1.click()

        Button1 = driver.find_element_by_xpath('//android.widget.TextView[@content-desc="Accessibility"]')
        Button1.click()

        Button2 = driver.find_element_by_xpath('//android.widget.TextView[@content-desc="Accessibility Node Querying"]')
        Button2.click()

        Button3 = driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.ListView/android.widget.LinearLayout[1]/android.widget.CheckBox')
        Button3.click()
        Button3.click()
        Button3.click()

        

        #Button4 = driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.ListView/android.widget.LinearLayout[3]/android.widget.CheckBox')
        #Button4.click()
        
        
        print('Click')



    def tearDown(self):
        print("tearDown")
        #self.driver.quit()


def Test(DeviceUid:str = ''):
    app = os.path.join(os.path.dirname(__file__), 'C:\\Users\\User\\Desktop\\업무\\Appium\\5. TestFiles', 'ApiDemos-debug.apk')
    app = os.path.abspath(app)

    # Set up appium
    # Appium 서버의 포트는 4001로 지정합니다.
    # 그리고 desired_capabilities에 연결하려는 디바이스(V10)의 정보를 넣습니다.
    cap = {
            'app': app,
            'uid': DeviceUid,
            'platformName': 'Android',
            'platformVersion': '7.1.2',
            'deviceName': 'Virtual',
            'automationName': 'Appium',
            'appPackage': 'io.appium.android.apis',
            'appActivity': 'io.appium.android.apis.ApiDemos',
            'newCommandTimeout': 300
            #'udid': 'LGF600Kb1134738'
        }

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

    print(DeviceUid & ' Test End')
    sleep(10)

    driver.quit()


if __name__ == "__main__":
    
    Test('127.0.0.1:62001')
    Test('127.0.0.1:62025')
    
    #test = unittest.TestLoader().loadTestsFromTestCase(code)
    #unittest.TextTestRunner(verbosity=2).run(test)
    print('Test End')
    pass