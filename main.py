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
        
searchesList = None
chromeObj = None
firefoxObj = None
    
def init_searches():
    global searchesList 
    searchesList = Searches().getSearchesList()
    
def init_chrome(useChrome):
    global chromeObj
    if usechrome == True:
        chromeObj = ChromeWebDriver(Edge,SafariMobile)

def init_firefox(useFirefox):
    global firefoxObj        
    if usefirefox == True:
        firefoxObj = FirefoxWebDriver(Edge,SafariMobile)
        firefoxObj.startDesktopDriver() 
        
if __name__ == '__main__':

#     dependencies = ["selenium", "feedparser"]
#     updateDependencies(dependencies)
    usefirefox = True
    usechrome = True
    

    
    DesktopSearches = 65
    MobileSearches = 42
    searchesThread = threading.Thread(name='searches_init', target=init_searches)
    searchesThread.start()
    
    startChrome = threading.Thread(name='startChrome', target=init_chrome, args=(usechrome,))
    startChrome.start()
    startFirefox = threading.Thread(name='startFirefox', target=init_firefox, args=(usefirefox,))
    startFirefox.start()

    
    searchesThread.join()
    startFirefox.join()
    startChrome.join()
    
    print ("Desktop Searches:")
    for index in (random.sample(range(len(searchesList)), min(DesktopSearches,len(searchesList)))):
        print (searchesList[index])
        if usefirefox == True:
            firefoxObj.getDesktopUrl(base_url + searchesList[index])
        if usechrome == True:
            chromeObj.getDesktopUrl(base_url + searchesList[index])
        sleep(random.uniform(1.0,2.75))
        
    if usefirefox == True:
        firefoxObj.closeDesktopDriver()
    if usechrome == True:    
        chromeObj.closeDesktopDriver()
     
    if usefirefox == True:
        firefoxObj.startMobileDriver()
    if usechrome == True:
        chromeObj.startMobileDriver()
    
    print ("Mobile Searches:")
    for index in (random.sample(range(len(searchesList)), min(MobileSearches, len(searchesList)))):
        print (searchesList[index])
        if usefirefox == True:
            firefoxObj.getMobileUrl(base_url + searchesList[index])
        if usechrome == True:
            chromeObj.getMobileUrl(base_url + searchesList[index])
        sleep(random.uniform(1.0,2.75))

    if usefirefox == True:
        firefoxObj.closeMobileDriver()
    if usechrome == True:    
        chromeObj.closeMobileDriver()
    

