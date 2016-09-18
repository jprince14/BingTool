from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.keys import Keys
import platform
import os

class FirefoxWebDriver:

    def __init__(self, desktopUA, mobileUA):
        self.desktopUA = desktopUA
        self.mobileUA = mobileUA
        
        if platform.system() == "Windows":
            self.controlKey = Keys.CONTROL
            profilesDir = os.path.join(os.getenv('APPDATA') , "Mozilla\\Firefox\\Profiles\\")
            self.ffProfileDir = os.path.join(profilesDir, os.listdir(profilesDir)[0]).replace("\\","/")
            self.binary = "C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe"
            
            #TODO: automatically download driver and set path
            downloadsDir = os.path.join(os.getenv('HOMEPATH'),"Downloads")
            driverLocation = downloadsDir + "\\geckodriver-v0.10.0-win64\\"
            os.environ["PATH"] = os.environ["PATH"] + ";" + driverLocation
            
        elif platform.system() == "Darwin":
        #Mac
            self.controlKey = Keys.COMMAND
            profilesDir = os.path.join(os.environ['HOME'], "Library/Application Support/Firefox/Profiles/")
            self.ffProfileDir = os.path.join(profilesDir + os.listdir(profilesDir)[0])
            self.binary = "/usr/bin/firefox"
            
            self.downloadsDir = os.path.join(os.getenv('HOME'),"Downloads")

            
            #TODO: set path for mac, download gecko driver
    
    def startDesktopDriver(self):
        
        firefoxDeskopProfile = FirefoxProfile(profile_directory=self.ffProfileDir)
        firefoxDeskopProfile.set_preference("general.useragent.override", self.desktopUA)
        
        caps = DesiredCapabilities.FIREFOX
        caps["marionette"] = True
        caps["binary"] = self.binary
        
        self.firefoxDesktopDriver = webdriver.Firefox(capabilities=caps, firefox_profile=firefoxDeskopProfile)
    
    def startMobileDriver(self):    
        
        firefoxMobileProfile = FirefoxProfile(profile_directory=self.ffProfileDir)
        firefoxMobileProfile.set_preference("general.useragent.override", self.mobileUA)
        
        caps = DesiredCapabilities.FIREFOX
        caps["marionette"] = True
        caps["binary"] = self.binary
        
        self.firefoxMobileDriver = webdriver.Firefox(capabilities=caps, firefox_profile=firefoxMobileProfile)
        
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
