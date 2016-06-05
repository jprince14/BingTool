from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import platform
import os
import sys
import zipfile
import io
    
class ChromeWebDriver:
    SUCCESS = 0
    FAILURE = 1
    winDriver = "http://chromedriver.storage.googleapis.com/2.21/chromedriver_win32.zip"
    macDriver = "http://chromedriver.storage.googleapis.com/2.21/chromedriver_mac32.zip"
    linux64Driver = "http://chromedriver.storage.googleapis.com/2.21/chromedriver_linux64.zip"
    linux32Driver = "http://chromedriver.storage.googleapis.com/2.21/chromedriver_linux32.zip"
    
    def __init__(self, desktopUA, mobileUA):
        self.desktopUA = desktopUA
        self.mobileUA = mobileUA
        
        if platform.system() == "Windows":
            self.controlKey = Keys.CONTROL
            self.chromedirect = os.path.join(os.getenv('LOCALAPPDATA'),"Google\\Chrome\\User Data\\")
            self.downloadsDir = os.path.join(os.getenv('HOMEPATH'),"Downloads")
            self.driverUrl = ChromeWebDriver.winDriver
            
        elif platform.system() == "Darwin":
        #Mac
            self.controlKey = Keys.COMMAND
            self.chromedirect = os.path.join(os.getenv('HOME'), \
                "Library/Application Support/Google/Chrome/Default/")
            self.downloadsDir = os.path.join(os.getenv('HOME'),"Downloads")
            self.driverUrl = ChromeWebDriver.winDriver
        
        if self.checkForChromeDriver() == ChromeWebDriver.FAILURE:
            self.getChromeDriver()
        
        for file in os.listdir(self.downloadsDir):
            if ((file.startswith("chromedriver")) and (not file.endswith(".zip"))):
                self.webDriver = os.path.join(self.downloadsDir,file)
                break

    def checkForChromeDriver(self):
        for file in os.listdir(self.downloadsDir):
            if ((file.startswith("chromedriver")) and (not file.endswith(".zip"))):
                return ChromeWebDriver.SUCCESS
        return ChromeWebDriver.FAILURE

    def getChromeDriver(self):
        if sys.version_info.major <= 2:
            import urllib2
            zipDriver = urllib2.urlopen(self.driverUrl).read()
            zip_ref = zipfile.ZipFile(io.BytesIO(zipDriver))
            zip_ref.extractall(self.downloadsDir)
            zip_ref.close() 
        elif sys.version_info.major >= 3:
            import urllib.request
            zipDriver = urllib.request.urlopen(self.driverUrl).read()
            zip_ref = zipfile.ZipFile(io.BytesIO(zipDriver))
            zip_ref.extractall(self.downloadsDir)
            zip_ref.close() 

    def startDesktopDriver(self):
        chrome_desktop_opts = Options()
        chrome_desktop_opts.add_argument("user-agent=" + self.desktopUA)
        chrome_desktop_opts.add_argument("user-data-dir=" + self.chromedirect)
        self.chromeDesktopDriver = webdriver.Chrome(executable_path=self.webDriver,chrome_options=chrome_desktop_opts)
    
    def startMobileDriver(self):    
        chrome_mobile_opts = Options()
        chrome_mobile_opts.add_argument("user-agent=" + self.mobileUA)
        chrome_mobile_opts.add_argument("user-data-dir=" + self.chromedirect)
        self.chromeMobileDriver = webdriver.Chrome(executable_path=self.webDriver,chrome_options=chrome_mobile_opts)
        
    def getDesktopUrl(self, url):
        if not url.startswith("http"):
            url = "http://" + url
        self.chromeDesktopDriver.get(url)
        self.chromeDesktopDriver.find_element_by_tag_name("body").send_keys(self.controlKey + "t")
        self.chromeDesktopDriver.find_element_by_tag_name("body").send_keys(self.controlKey + Keys.TAB)
         
    def getMobileUrl(self, url):
        if not url.startswith("http"):
            url = "http://" + url
        self.chromeMobileDriver.get(url)
        self.chromeMobileDriver.find_element_by_tag_name("body").send_keys(self.controlKey + "t")
        self.chromeMobileDriver.find_element_by_tag_name("body").send_keys(self.controlKey + Keys.TAB)

    def closeDesktopDriver(self):
        self.chromeDesktopDriver.quit()
    
    def closeMobileDriver(self):
        self.chromeMobileDriver.quit()     

        
