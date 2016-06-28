import random
from time import sleep
import sys
import pip

try:
    from FirefoxWebDriver import FirefoxWebDriver
    from ChromeWebDriver import ChromeWebDriver
    from Searches import Searches   
except:
    checkDependencies()

Edge = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36 Edge/12.0"
SafariMobile = "Mozilla/5.0 (iPhone; CPU iPhone OS 9_2 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/47.0.2526.70 Mobile/13C71 Safari/601.1.46"

base_url = "http://www.bing.com/search?q="

def checkDependencies():
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

            
            
# def updateDependencies(dependencies):
#     for dependency in dependencies:
#         try:
#             pip.main(['install', '-U', dependency])
#         except:
#             print ("Unable to update %s\n" % dependency)
        
if __name__ == '__main__':

#     dependencies = ["selenium", "feedparser"]
#     updateDependencies(dependencies)
    usefirefox = False
    usechrome = True
    chrome = None
    firefox = None
    
    DesktopSearches = 35
    MobileSearches = 25
    
    searchesList = Searches().getSearchesList()
    if usefirefox == True:
        firefox = FirefoxWebDriver(Edge,SafariMobile)
        firefox.startDesktopDriver()

    if usechrome == True:
        chrome = ChromeWebDriver(Edge,SafariMobile)
        chrome.startDesktopDriver()
        
    print ("Desktop Searches:")
    for index in (random.sample(range(len(searchesList)), min(DesktopSearches,len(searchesList)))):
        print (searchesList[index])
        if usefirefox == True:
            firefox.getDesktopUrl(base_url + searchesList[index])
        if usechrome == True:
            chrome.getDesktopUrl(base_url + searchesList[index])
        sleep(random.uniform(1.0,3.25))
        
    if firefox == True:
        firefox.closeDesktopDriver()
    if chrome == True:    
        chrome.closeDesktopDriver()
     
    if firefox == True:
        firefox.startMobileDriver()
    if chrome == True:
        chrome.startMobileDriver()
    
    print ("Mobile Searches:")
    for index in (random.sample(range(len(searchesList)), min(MobileSearches, len(searchesList)))):
        print (searchesList[index])
        if usefirefox == True:
            firefox.getMobileUrl(base_url + searchesList[index])
        if usechrome == True:
            chrome.getMobileUrl(base_url + searchesList[index])
            print base_url + searchesList[index]
        sleep(random.uniform(1.0,3.25))

    if firefox == True:
        firefox.closeMobileDriver()
    if chrome == True:    
        chrome.closeMobileDriver()
    

