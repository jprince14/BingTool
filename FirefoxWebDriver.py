from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys
import platform
import stat
import bs4 as BeautifulSoup
import os
import sys
import zipfile
import tarfile
import io

class FirefoxWebDriver:

    def __init__(self, desktopUA, mobileUA):
        self.desktopUA = desktopUA
        self.mobileUA = mobileUA
        self.driverURL = "https://github.com/mozilla/geckodriver/releases/latest"
        self.githubUrl = "https://github.com"
        
        self.getWebdriverURL(self.driverURL)
        
        if platform.system() == "Windows":
            self.controlKey = Keys.CONTROL
            profilesDir = os.path.join(os.getenv('APPDATA') , "Mozilla\\Firefox\\Profiles\\")
            self.ffProfileDir = os.path.join(profilesDir, os.listdir(profilesDir)[0])
            widowsFile_32bit = "C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe"
            widowsFile_64bit = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"

            if os.path.isfile(widowsFile_32bit):
                self.binary = widowsFile_32bit
            elif os.path.isfile(widowsFile_64bit):
                self.binary = widowsFile_64bit
            else:
                print ("Unable to finf firefox binary\n")
                raise "U"
                
            
            self.downloadsDir = os.path.join(os.getenv('HOMEPATH'),"Downloads")
            print (self.downloadsDir)
            
            os.environ["PATH"] = os.environ["PATH"] + ";" + self.downloadsDir
            
            self.getGeckoDriver_zip(self.windowsURL)
            
        elif platform.system() == "Darwin":
        #Mac
            self.controlKey = Keys.COMMAND
            profilesDir = os.path.join(os.environ['HOME'], "Library/Application Support/Firefox/Profiles/")
            self.ffProfileDir = os.path.join(profilesDir + os.listdir(profilesDir)[0])
            self.binary = "/usr/bin/firefox"
            
            self.downloadsDir = os.path.join(os.getenv('HOME'),"Downloads")
            self.getGeckoDriver_tar_gz(self.macURL)
                        
        for file in os.listdir(self.downloadsDir):
            if ((file.startswith("geckodriver")) and (not file.endswith(".zip")) and (not file.endswith(".gz"))):
                self.driverBinary = os.path.join(self.downloadsDir, file)
                st = os.stat(self.driverBinary)
                os.chmod(self.driverBinary, st.st_mode | stat.S_IEXEC)

    def getGeckoDriver_zip(self, URL):
        if sys.version_info.major <= 2:
            import urllib2
            zipDriver = urllib2.urlopen(URL).read()
            zip_ref = zipfile.ZipFile(io.BytesIO(zipDriver))
            zip_ref.extractall(self.downloadsDir)
            zip_ref.close() 
        elif sys.version_info.major >= 3:
            import urllib.request
            zipDriver = urllib.request.urlopen(URL).read()
            zip_ref = zipfile.ZipFile(io.BytesIO(zipDriver))
            zip_ref.extractall(self.downloadsDir)
            zip_ref.close()
    
    def getGeckoDriver_tar_gz(self, URL):
        if sys.version_info.major <= 2:
            import urllib2
            tar_gz_file = urllib2.urlopen(URL).read()

        elif sys.version_info.major >= 3:
            import urllib.request
            tar_gz_file = urllib.request.urlopen(URL).read()
    
        file_like_object = io.BytesIO(tar_gz_file)
        tar = tarfile.open(fileobj=file_like_object)
        tar.extractall(path=self.downloadsDir)
        tar.close()
        
    def __del__(self):
#         print ("Firefox __del__")
        os.remove(self.driverBinary)
        
    def getWebdriverURL(self, driverPageURL):
        if sys.version_info.major <= 2:
            import urllib2
            html_page = urllib2.urlopen(driverPageURL)
        
        elif sys.version_info.major >= 3:
            import urllib.request
            html_page = urllib.request.urlopen(driverPageURL)
        
        soup = BeautifulSoup.BeautifulSoup(html_page, "html.parser")
        
        downloadsSection = soup.find('ul', {"class": "release-downloads"})
        
        driverList = downloadsSection.findAll("a")
        
        for driver in driverList:
            driverUrl = driver['href']
            if "linux64.tar.gz" in driverUrl:
                self.linuxURL = self.githubUrl + driverUrl
            elif "macos.tar.gz" in driverUrl:
                self.macURL = self.githubUrl + driverUrl
            elif "win64.zip" in driverUrl:
                self.windowsURL = self.githubUrl + driverUrl
            
    
    def startDesktopDriver(self):
        firefoxDeskopProfile = FirefoxProfile(profile_directory=self.ffProfileDir)
        firefoxDeskopProfile.set_preference("general.useragent.override", self.desktopUA)
        
        caps = DesiredCapabilities.FIREFOX
        caps["marionette"] = True
        
        binary = FirefoxBinary(self.binary)
        
        self.firefoxDesktopDriver = webdriver.Firefox(firefox_binary=binary, capabilities=caps, firefox_profile=firefoxDeskopProfile)
    
    def startMobileDriver(self):    
        
        firefoxMobileProfile = FirefoxProfile(profile_directory=self.ffProfileDir)
        firefoxMobileProfile.set_preference("general.useragent.override", self.mobileUA)
        
        caps = DesiredCapabilities.FIREFOX
        caps["marionette"] = True

        binary = FirefoxBinary(self.binary)
        
        self.firefoxMobileDriver = webdriver.Firefox(firefox_binary=binary, capabilities=caps, firefox_profile=firefoxMobileProfile)
        
    def getDesktopUrl(self, url):
        if not url.startswith("http"):
            url = "http://" + url
        self.firefoxDesktopDriver.get(url)
#         self.firefoxDesktopDriver.find_element_by_tag_name("body").send_keys(self.controlKey + "t")
         
    def getMobileUrl(self, url):
        if not url.startswith("http"):
            url = "http://" + url
        self.firefoxMobileDriver.get(url)
#         self.firefoxMobileDriver.find_element_by_tag_name("body").send_keys(self.controlKey + "t")

    def closeDesktopDriver(self):
        self.firefoxDesktopDriver.quit()
    
    def closeMobileDriver(self):
        self.firefoxMobileDriver.quit()     
