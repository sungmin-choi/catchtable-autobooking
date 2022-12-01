from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
from selenium.webdriver.remote.remote_connection import LOGGER
import logging
LOGGER.setLevel(logging.WARNING)
import os

class Spoofer(object):
    def __init__(self, country_id=['US'], rand=True, anonym=True,):
#         self.user_proxy = user_proxy
        self.country_id = country_id
        self.rand = rand
        self.anonym = anonym
        self.userAgent = self.get()
    def get(self):
        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
#         ip = self.user_proxy.split(":")[0]
#         return ua, ip
        return ua

class DriverOptions(object):
     def __init__(self ):
        cookie_dir = str(os.path.abspath(os.getcwd())) + "\\cookies\\" +str(1) + '\Chrome_cookie'
        print("cookie_dir: " + cookie_dir)
        self.options = Options()
        self.options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.options.add_argument(f"--user-data-dir={cookie_dir}") 
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--start-maximized')
        self.options.add_argument('--single-process')
        self.options.add_argument('--disable-dev-shm-usage')
        # self.options.add_argument("--incognito")
     #    self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_argument("disable-infobars")
        self.helperSpoofer = Spoofer()
        self.options.add_argument("user-agent={}".format("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"))

class WebDriver(DriverOptions,object):
    def __init__(self, path="",):
        DriverOptions.__init__(self,)
#         self.user_proxy = user_proxy
        self.driver_instance = self.get_driver()
    def get_driver(self):
        webdriver.DesiredCapabilities.CHROME['acceptSslCerts'] = True
        chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]  #크롬드라이버 버전 확인

        try:     
            driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe',options=self.options)   
        except:
            chromedriver_autoinstaller.install(True)
            driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe',options=self.options)
#         driver = webdriver.Chrome(path, options=self.options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
           "source":
                "const newProto = navigator.__proto__;"
                "delete newProto.webdriver;"
                "navigator.__proto__ = newProto;"
        })
        return driver