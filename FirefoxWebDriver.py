from selenium import webdriver
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
        elif platform.system() == "Darwin":
        #Mac
            self.controlKey = Keys.COMMAND
            profilesDir = os.path.join(os.environ['HOME'], "Library/Application Support/Firefox/Profiles/")
            self.ffProfileDir = os.path.join(profilesDir + os.listdir(profilesDir)[0])
    
    def startDesktopDriver(self):
        firefoxDeskopProfile = webdriver.FirefoxProfile( self.ffProfileDir)
        firefoxDeskopProfile.set_preference("general.useragent.override", self.desktopUA)
        self.firefoxDesktopDriver = webdriver.Firefox(firefoxDeskopProfile)
    
    def startMobileDriver(self):    
        firefoxMobileProfile = webdriver.FirefoxProfile( self.ffProfileDir)
        firefoxMobileProfile.set_preference("general.useragent.override", self.mobileUA)
        self.firefoxMobileDriver = webdriver.Firefox(firefoxMobileProfile)
        
    def getDesktopUrl(self, url):
        if not url.startswith("http"):
            url = "http://" + url
        self.firefoxDesktopDriver.get(url)
        self.firefoxDesktopDriver.find_element_by_tag_name("body").send_keys(self.controlKey + "t")
         
    def getMobileUrl(self, url):
        if not url.startswith("http"):
            url = "http://" + url
        self.firefoxMobileDriver.get(url)
        self.firefoxMobileDriver.find_element_by_tag_name("body").send_keys(self.controlKey + "t")

    def closeDesktopDriver(self):
        self.firefoxDesktopDriver.quit()
    
    def closeMobileDriver(self):
        self.firefoxMobileDriver.quit()     
