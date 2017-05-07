import random
from time import sleep
import sys
import pip
import threading

try:
    from FirefoxWebDriver import FirefoxWebDriver
    from ChromeWebDriver import ChromeWebDriver
    from Searches import Searches   
except:
    checkDependencies()



class BingRewards(object):
    Edge = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36 Edge/12.0"
    SafariMobile = "Mozilla/5.0 (iPhone; CPU iPhone OS 9_2 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/47.0.2526.70 Mobile/13C71 Safari/601.1.46"
    DESKTOP = "desktop"
    MOBILE = "mobile"
    base_url = "http://www.bing.com/search?q="
    
    def __init__(self, desktopSearches, MobileSearches, UseFirefox, UseChrome):
        self.desktopSearches = desktopSearches
        self.MobileSearches = MobileSearches
        self.UseFirefox = UseFirefox
        self.UseChrome = UseChrome
        
        self.numSearches = {BingRewards.DESKTOP : self.desktopSearches, BingRewards.MOBILE : self.MobileSearches}

        searchesThread = threading.Thread(name='searches_init', target=self.init_searches)
        searchesThread.start()
        
        startFirefox = threading.Thread(name='startFirefox', target=self.init_firefox, args=())
        startFirefox.start()
             
        startChrome = threading.Thread(name='startChrome', target=self.init_chrome, args=())
        startChrome.start()
        
        searchesThread.join()
        startChrome.join()
        startFirefox.join()
        
        
    def updateDependencies(self, dependencies):
        for dependency in dependencies:
            try:
                pip.main(['install', '-U', dependency])
            except:
                print ("Unable to update %s\n" % dependency)
    
    def checkDependencies(self, ):
        #Make sure that Selenium is installed
        installed_packages = pip.get_installed_distributions()
        flat_installed_packages = [package.project_name for package in installed_packages]
        if "selenium" not in flat_installed_packages:
            try:
                pip.main(['install', '-U', 'selenium'])
            except:
                print ("NEED TO INSTALL SELENIUM")
                sys.stderr.write("ERROR: Need to install selenium")
                
        if "feedparser" not in flat_installed_packages:
            try:
                pip.main(['install', '-U', 'feedparser'])
            except:
                sys.stderr.write("ERROR: Need to install feedparser")
                
        if "beautifulsoup4" not in flat_installed_packages:
            try:
                pip.main(['install', '-U', 'beautifulsoup4'])
            except:
                sys.stderr.write("ERROR: Need to install beautifulsoup4")
        
        self.updateDependencies(["selenium", "feedparser", "beautifulsoup4"])
                        
    def init_searches(self, ):
        self.searchesList = Searches().getSearchesList()
        
    def init_chrome(self, ):
        if self.UseChrome == True:
            self.chromeObj = ChromeWebDriver(BingRewards.Edge,BingRewards.SafariMobile)
    
    def init_firefox(self, ):
        if self.UseFirefox == True:
            self.firefoxObj = FirefoxWebDriver(BingRewards.Edge,BingRewards.SafariMobile)
    
    def firefox_search(self, browser):
        
        if self.UseFirefox == False:
            return 
        
        if browser == BingRewards.DESKTOP:
            self.firefoxObj.startDesktopDriver() 
        elif browser == BingRewards.MOBILE:
            self.firefoxObj.startMobileDriver()
        
        for index in (random.sample(range(len(self.searchesList)), min(self.numSearches[browser],len(self.searchesList)))):
            if browser == BingRewards.DESKTOP:
                self.firefoxObj.getDesktopUrl(BingRewards.base_url + self.searchesList[index])
            elif browser == BingRewards.MOBILE:
                self.firefoxObj.getMobileUrl(BingRewards.base_url + self.searchesList[index])
            sleep(random.uniform(1.0,2.75))
            
        if browser == BingRewards.DESKTOP:
            self.firefoxObj.closeDesktopDriver()
        elif browser == BingRewards.MOBILE:
            self.firefoxObj.closeMobileDriver()
            
    def chrome_search(self, browser):       
       
        if self.UseChrome == False:
            return 
        
        if browser == BingRewards.DESKTOP:
            self.chromeObj.startDesktopDriver() 
        elif browser == BingRewards.MOBILE:
            self.chromeObj.startMobileDriver()
            
        for index in (random.sample(range(len(self.searchesList)), min(self.numSearches[browser],len(self.searchesList)))):
            if browser == BingRewards.DESKTOP:
                self.chromeObj.getDesktopUrl(BingRewards.base_url + self.searchesList[index])
            elif browser == BingRewards.MOBILE:
                self.chromeObj.getMobileUrl(BingRewards.base_url + self.searchesList[index])
            sleep(random.uniform(1.0,2.75))
            
        if browser == BingRewards.DESKTOP:
            self.chromeObj.closeDesktopDriver()
        elif browser == BingRewards.MOBILE:
            self.chromeObj.closeMobileDriver()

    def runDesktopSearches(self):
        firefoxDesktopSearches = threading.Thread(name='ff_desktop', target=self.firefox_search, kwargs={'browser':BingRewards.DESKTOP})
        firefoxDesktopSearches.start()
        
        chromeDesktopSearches = threading.Thread(name='chrome_desktop', target=self.chrome_search, kwargs={'browser':BingRewards.DESKTOP})
        chromeDesktopSearches.start()

        firefoxDesktopSearches.join()
        chromeDesktopSearches.join()
    
    def runMobileSearches(self):
        firefoxMobileSearches = threading.Thread(name='ff_mobile', target=self.firefox_search, kwargs={'browser':BingRewards.MOBILE})
        firefoxMobileSearches.start()
        
        chromeMobileSearches = threading.Thread(name='chrome_mobile', target=self.chrome_search, kwargs={'browser':BingRewards.MOBILE})
        chromeMobileSearches.start()

        firefoxMobileSearches.join()
        chromeMobileSearches.join()

if __name__ == '__main__':

    usefirefox = True
    usechrome = True
    DesktopSearches = 70
    MobileSearches = 40
    bingRewards = BingRewards(desktopSearches=DesktopSearches, MobileSearches=MobileSearches, UseFirefox=usefirefox, UseChrome=usechrome)
    bingRewards.runDesktopSearches()
    bingRewards.runMobileSearches()
    print ("COMPLETE")
# 

    
    

