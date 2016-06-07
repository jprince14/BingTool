from FirefoxWebDriver import FirefoxWebDriver
from ChromeWebDriver import ChromeWebDriver
from Searches import Searches
import random
from time import sleep
import sys

Edge = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36 Edge/12.0"
SafariMobile = "Mozilla/5.0 (iPhone; CPU iPhone OS 9_2 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/47.0.2526.70 Mobile/13C71 Safari/601.1.46"

base_url = "http://www.bing.com/search?q="

def checkDependencies():
    import pip
    #Make sure that Selenium is installed
    installed_packages = pip.get_installed_distributions()
    flat_installed_packages = [package.project_name for package in installed_packages]
    if "selenium" not in flat_installed_packages:
        try:
            pip.main(['install', '-U', 'selenium'])
        except:
            sys.stderr.write("ERROR: Need to install selenium")
            
    if "feedparser" not in flat_installed_packages:
        try:
            pip.main(['install', '-U', 'feedparser'])
        except:
            sys.stderr.write("ERROR: Need to install feedparser")
            
if __name__ == '__main__':
    
    checkDependencies()
    
    DesktopSearches = 35
    MobileSearches = 25
    
    searchesList = Searches().getSearchesList()

    firefox = FirefoxWebDriver(Edge,SafariMobile)
    firefox.startDesktopDriver()

    chrome = ChromeWebDriver(Edge,SafariMobile)
    chrome.startDesktopDriver()
    
    for index in (random.sample(range(len(searchesList)), DesktopSearches)):
        
        firefox.getDesktopUrl(base_url + searchesList[index])
        chrome.getDesktopUrl(base_url + searchesList[index])
        sleep(random.uniform(1.0,3.25))
        
    firefox.closeDesktopDriver()    
    chrome.closeDesktopDriver()
     
    firefox.startMobileDriver()
    chrome.startMobileDriver()
    
    for index in (random.sample(range(len(searchesList)), MobileSearches)):
    
        firefox.getMobileUrl(base_url + searchesList[index])
        chrome.getMobileUrl(base_url + searchesList[index])
        sleep(random.uniform(1.0,3.25))

    firefox.closeMobileDriver()    
    chrome.closeMobileDriver()
    
