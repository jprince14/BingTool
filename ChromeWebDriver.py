from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import platform
import os
import sys
import zipfile
import io
import stat
import bs4 as BeautifulSoup
import re
    
class ChromeWebDriver:
    SUCCESS = 0
    FAILURE = 1
    
    linux32 = "/chromedriver_linux32.zip"
    linux64 = "/chromedriver_linux64.zip"
    mac32 = "/chromedriver_mac32.zip"
    windows32 = "/chromedriver_win32.zip"
    
    win = "windows"
    mac = "mac"
    linux64 = "linux64"
    linux32 = "linux32"
    

    def __init__(self, desktopUA, mobileUA):
        self.desktopUA = desktopUA
        self.mobileUA = mobileUA
        
        self.winDriver = None
        self.macDriver = None
        self.linux64Driver = None
        self.linux32Driver = None
        
        self.DriverURLDict = {ChromeWebDriver.win: None, ChromeWebDriver.mac: None,
                              ChromeWebDriver.linux32 : None, ChromeWebDriver.linux64 : None}
                
        if platform.system() == "Windows":
            self.controlKey = Keys.CONTROL
            self.chromedirect = os.path.join(os.getenv('LOCALAPPDATA'),"Google\\Chrome\\User Data\\")
            self.downloadsDir = os.path.join(os.getenv('HOMEPATH'),"Downloads")
            
            #driverUrl is a pointer
            self.os = ChromeWebDriver.win
            
        elif platform.system() == "Darwin":
        #Mac
            self.controlKey = Keys.COMMAND
            self.chromedirect = os.path.join(os.getenv('HOME'), \
                "Library/Application Support/Google/Chrome/Default/")
            self.downloadsDir = os.path.join(os.getenv('HOME'),"Downloads")
            
            self.os = ChromeWebDriver.mac
        
        self.getChromeDriver()
        
        for file in os.listdir(self.downloadsDir):
            if ((file.startswith("chromedriver")) and (not file.endswith(".zip"))):
                self.webDriver = os.path.join(self.downloadsDir,file)
                break
            
    def __del__(self):
        os.remove(self.webDriver)
        print ("Chrome Cleanup Complete")
        
    def checkForChromeDriver(self):
        for file in os.listdir(self.downloadsDir):
            if ((file.startswith("chromedriver")) and (not file.endswith(".zip"))):
                return ChromeWebDriver.SUCCESS
        return ChromeWebDriver.FAILURE

    def getDriverUrl(self):
        
        url = "https://sites.google.com/a/chromium.org/chromedriver/downloads"

        html_page = None
        if sys.version_info.major <= 2:
            import urllib2
            html_page = urllib2.urlopen(url)

        elif sys.version_info.major >= 3:
            import urllib.request
            html_page = urllib.request.urlopen(url)

        soup = BeautifulSoup.BeautifulSoup(html_page, "html.parser")
        urlfound = False
        downloadURL = None
        for table in soup.findAll('table'):
            links = table.findAll('a')
            for x in range(len(links)):
                if "TOC-Latest-Release" in str(links[x]):
                    downloadURL = links[x+1]['href']
                    urlfound = True
                    break
            if urlfound == True:
                break
        
        pattern = "index.html\?path=([0-9a-fA-F-.]{1,7})\/"
        regexFind = re.search(pattern, downloadURL)
        version = regexFind.group(1)
     
        baseurl = "http://chromedriver.storage.googleapis.com/"
        
        self.DriverURLDict[self.linux32] = baseurl + version + ChromeWebDriver.linux32
        self.DriverURLDict[self.linux64] = baseurl + version + ChromeWebDriver.linux64
        self.DriverURLDict[self.mac] = baseurl + version + ChromeWebDriver.mac32
        self.DriverURLDict[self.win] = baseurl + version + ChromeWebDriver.windows32   
        
    def getChromeDriver(self):
        self.getDriverUrl()
        if sys.version_info.major <= 2:
            import urllib2
            zipDriver = urllib2.urlopen(self.DriverURLDict[self.os]).read()
            zip_ref = zipfile.ZipFile(io.BytesIO(zipDriver))
            zip_ref.extractall(self.downloadsDir)
            zip_ref.close() 
        elif sys.version_info.major >= 3:
            import urllib.request
            zipDriver = urllib.request.urlopen(self.DriverURLDict[self.os]).read()
            zip_ref = zipfile.ZipFile(io.BytesIO(zipDriver))
            zip_ref.extractall(self.downloadsDir)
            zip_ref.close() 
        
        for file in os.listdir(self.downloadsDir):
            if ((file.startswith("chromedriver")) and (not file.endswith(".zip"))):
                filePath = os.path.join(self.downloadsDir, file)
                st = os.stat(filePath)
                os.chmod(filePath, st.st_mode | stat.S_IEXEC)

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

        
