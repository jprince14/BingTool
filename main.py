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

def updateDependencies(dependencies):
    for dependency in dependencies:
        try:
            pip.main(['install', '-U', dependency])
        except:
            print ("Unable to update %s\n" % dependency)

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
    
    updateDependencies(["selenium", "feedparser", "beautifulsoup4"])
            
        
searchesList = None
# chromeObj = None
# firefoxObj = None
    
def init_searches():
    global searchesList 
    searchesList = Searches().getSearchesList()
    
def init_chrome(useChrome):
    global chromeObj
    if usechrome == True:
        chromeObj = ChromeWebDriver(Edge,SafariMobile)
        chromeObj.startDesktopDriver()

def init_firefox(useFirefox):
    global firefoxObj        
    if usefirefox == True:
        firefoxObj = FirefoxWebDriver(Edge,SafariMobile)
        firefoxObj.startDesktopDriver() 

def firefox_search(usefirefox, numSearches, browser):
    global searchesList 
    global firefoxObj        

    if usefirefox == False:
        return 
    for index in (random.sample(range(len(searchesList)), min(numSearches,len(searchesList)))):
        if browser == "desktop":
            firefoxObj.getDesktopUrl(base_url + searchesList[index])
        elif browser == "mobile":
            firefoxObj.getMobileUrl(base_url + searchesList[index])
        sleep(random.uniform(1.0,2.75))
    if browser == "desktop":
        firefoxObj.closeDesktopDriver()
        firefoxObj.startMobileDriver()
    elif browser == "mobile":
        firefoxObj.closeMobileDriver()
        
def chrome_search(usechrome, numSearches, browser):
    global searchesList 
    global chromeObj

    if usechrome == False:
        return 
    for index in (random.sample(range(len(searchesList)), min(numSearches,len(searchesList)))):
        if browser == "desktop":
            chromeObj.getDesktopUrl(base_url + searchesList[index])
        elif browser == "mobile":
            chromeObj.getMobileUrl(base_url + searchesList[index])
        sleep(random.uniform(1.0,2.75))
    if browser == "desktop":
        chromeObj.closeDesktopDriver()
        chromeObj.startMobileDriver()
    elif browser == "mobile":
        chromeObj.closeMobileDriver()

if __name__ == '__main__':

    usefirefox = True
    usechrome = True
    DesktopSearches = 70
    MobileSearches = 42
    
    searchesThread = threading.Thread(name='searches_init', target=init_searches)
    searchesThread.start()

    startFirefox = threading.Thread(name='startFirefox', target=init_firefox, args=(usefirefox,))
    startFirefox.start()
        
    startChrome = threading.Thread(name='startChrome', target=init_chrome, args=(usechrome,))
    startChrome.start()

    searchesThread.join()
    startChrome.join()
    startFirefox.join()

    firefoxDesktopSearches = threading.Thread(name='ff_desktop', target=firefox_search, args=(usefirefox, DesktopSearches, "desktop"))
    firefoxDesktopSearches.start()
    chromeDesktopSearches = threading.Thread(name='chrome_desktop', target=chrome_search, args=(usechrome, DesktopSearches, "desktop"))
    chromeDesktopSearches.start()
    
    firefoxDesktopSearches.join()
    chromeDesktopSearches.join()

    firefoxMobileSearches = threading.Thread(name='ff_mobile', target=firefox_search, args=(usefirefox, MobileSearches, "mobile"))
    firefoxMobileSearches.start()
    chromeMobileSearches = threading.Thread(name='chrome_mobile', target=chrome_search, args=(usechrome, MobileSearches, "mobile"))
    chromeMobileSearches.start()

    chromeMobileSearches.join()
    firefoxMobileSearches.join()
    
    

