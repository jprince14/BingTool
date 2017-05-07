from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import platform
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
        self.mobileRunning = False
        self.desktopRunning = False
        self.getWebdriverURL(self.driverURL)
        
        if platform.system() == "Windows":
            profilesDir = os.path.join(os.getenv('APPDATA') , "Mozilla", "Firefox", "Profiles")
            self.getDefaultProfile(profilesDir)
                        
            self.downloadsDir = os.path.join(os.getenv('HOMEPATH'),"Downloads")
            
            os.environ["PATH"] = os.environ["PATH"] + ";" + self.downloadsDir
            
            self.checkIfGeckoDriverAlreadyExists()
            self.getGeckoDriver_zip(self.windowsURL)
            
        elif platform.system() == "Darwin":
        #Mac
            profilesDir = os.path.join(os.environ['HOME'], "Library", "Application Support", "Firefox", "Profiles")
            self.getDefaultProfile(profilesDir)
            
            self.downloadsDir = os.path.join(os.getenv('HOME'),"Downloads")
            
            self.checkIfGeckoDriverAlreadyExists()
            self.getGeckoDriver_tar_gz(self.macURL)
                        
        for file in os.listdir(self.downloadsDir):
            if ((file.startswith("geckodriver")) and (not file.endswith(".zip")) and (not file.endswith(".gz"))):
                self.driverBinary = os.path.join(self.downloadsDir, file)
                os.chmod(self.driverBinary, 0o777)
    
    def getDefaultProfile(self, profileDir):
        for file in os.listdir(profileDir):
            if file.endswith(".default"):
                self.ffProfileDir = os.path.join(profileDir, file)
                return
            
        raise ("Unable to find default firefox profile directory")

    def checkIfGeckoDriverAlreadyExists(self):
        for file in os.listdir(self.downloadsDir):
            if (file.startswith("geckodriver")):
                os.remove(os.path.join(self.downloadsDir, file))
                
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
        if self.desktopRunning == True:
            self.closeDesktopDriver()
        if self.mobileRunning == True:
            self.closeMobileDriver()
        try:
            os.remove(self.driverBinary)
        except:
            print ("Failed to delete firefox web driver binary \"%s\"" % (self.driverBinary))
        
        print ("Firefox Cleanup Complete")

        
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
        
        firefoxDeskopProfile = webdriver.FirefoxProfile(profile_directory=self.ffProfileDir)
        firefoxDeskopProfile.set_preference("general.useragent.override", self.desktopUA)
                       
        self.firefoxDesktopDriver = webdriver.Firefox(firefox_profile=firefoxDeskopProfile)
        self.desktopRunning = True
    
    def startMobileDriver(self):    
        
        firefoxMobileProfile = webdriver.FirefoxProfile(profile_directory=self.ffProfileDir)
        firefoxMobileProfile.set_preference("general.useragent.override", self.mobileUA)
                
        self.firefoxMobileDriver = webdriver.Firefox(firefox_profile=firefoxMobileProfile)
        self.mobileRunning = True
        
    def getDesktopUrl(self, url):
        if self.desktopRunning == True:
            if not url.startswith("http"):
                url = "http://" + url
            self.firefoxDesktopDriver.get(url)
        else:
            print ("Firefox desktop webdriver is not open")
         
    def getMobileUrl(self, url):
        if self.mobileRunning == True:
            if not url.startswith("http"):
                url = "http://" + url
            self.firefoxMobileDriver.get(url)
        else:
            print ("Firefox desktop webdriver is not open")
    def closeDesktopDriver(self):
        if self.desktopRunning == True:
            try:
                self.firefoxDesktopDriver.quit()
                self.desktopRunning = False
            except Exception as e:
                print ("Hit exception following exception when trying to close the Firefox Desktop driver\n\t%s" % e)
            
    def closeMobileDriver(self):
        if self.mobileRunning == True:
            try:
                self.firefoxMobileDriver.quit()
                self.mobileRunning = False
            except Exception as e:
                print ("Hit exception following exception when trying to close the Firefox Mobile driver\n\t%s" % e)
