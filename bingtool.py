import random
from time import sleep
import sys
import threading
import os
import argparse
import platform
import subprocess

REQUIRED_PACKAGES = ["selenium", "feedparser", "beautifulsoup4", "setuptools"]


def updateDependencies(dependencies):
    for dependency in dependencies:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', dependency])
        except:
            print("Unable to update %s\n" % dependency)


def checkDependencies(packageList):
    # Make sure that all dependencies are installed
    installed_packages = pip.get_installed_distributions()
    flat_installed_packages = [package.project_name for package in installed_packages]
    for packageName in packageList:
        if packageName not in flat_installed_packages:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', packageName])
            except:
                sys.stderr.write("NEED TO INSTALL \"%s\"" % packageName)
                sys.stderr.write("run the command \"pip install -U %s\"" % packageName)

    updateDependencies(packageList)


try:
    from FirefoxWebDriver import FirefoxWebDriver
    from ChromeWebDriver import ChromeWebDriver
    from Searches import Searches
except:
    checkDependencies(REQUIRED_PACKAGES)
    # Try the imports again
    from FirefoxWebDriver import FirefoxWebDriver
    from ChromeWebDriver import ChromeWebDriver
    from Searches import Searches


class BingRewards(object):

    Edge = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299"
    SafariMobile = "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
    DESKTOP = "desktop"
    MOBILE = "mobile"
    base_url = "https://www.bing.com/search?q="

    def __init__(self, artifacts_dir, desktopSearches, mobileSearches, UseFirefox, UseChrome, searchesList=None,
                 useHeadless=False, loadcookies=False, load_default_profile=True):
        #If load_default_profile == False, loading cookies doesnt work
        self.UseFirefox = UseFirefox
        self.UseChrome = UseChrome
        self.totalSearches = desktopSearches + mobileSearches
        self.numSearches = {BingRewards.DESKTOP: desktopSearches, BingRewards.MOBILE: mobileSearches}
        self.useHeadless = useHeadless
        self.loadcookies = loadcookies
        self.load_default_profile = load_default_profile

        if platform.system() == "Windows":
            downloads_dir = os.path.join(os.getenv('HOMEPATH'), "Downloads")
        elif platform.system() == "Darwin":
            downloads_dir = os.path.join(os.getenv('HOME'), "Downloads")
        elif platform.system() == "Linux":
            downloads_dir = os.path.join(os.getenv('HOME'), "Downloads")

        if artifacts_dir == None:
            self.artifacts_dir = downloads_dir
        else:
            if os.path.exists(artifacts_dir):
                self.artifacts_dir = artifacts_dir
            else:
                raise Exception("The location %s does not exist" % artifacts_dir)

        if searchesList == None:
            searchesThread = threading.Thread(name='searches_init', target=self.init_searches)
            searchesThread.start()
        else:
            self.searchesList = searchesList

        if self.UseFirefox == True:
            startFirefox = threading.Thread(name='startFirefox', target=self.init_firefox, args=())
            startFirefox.start()

        if self.UseChrome == True:
            startChrome = threading.Thread(name='startChrome', target=self.init_chrome, args=())
            startChrome.start()

        if searchesList == None:
            searchesThread.join()
        if self.UseChrome == True:
            startChrome.join()
        if self.UseFirefox == True:
            startFirefox.join()

    def init_searches(self, ):
        self.searchesList = Searches(self.totalSearches).getSearchesList()

    def init_chrome(self, ):
        if self.UseChrome == True:
            self.chromeObj = ChromeWebDriver(self.artifacts_dir, BingRewards.Edge, BingRewards.SafariMobile,
                                             self.useHeadless, loadCookies=self.loadcookies,
                                             load_default_profile=self.load_default_profile)
            if self.chromeObj == None:
                raise ("ERROR: chromeObj = None")

    def init_firefox(self, ):
        if self.UseFirefox == True:
            self.firefoxObj = FirefoxWebDriver(self.artifacts_dir, BingRewards.Edge, BingRewards.SafariMobile,
                                               self.useHeadless, loadCookies=self.loadcookies,
                                               load_default_profile=self.load_default_profile)
            if self.firefoxObj == None:
                raise ("ERROR: firefoxObj = None")

    def firefox_search(self, browser):

        if self.UseFirefox == False:
            return

        if browser == BingRewards.DESKTOP:
            self.firefoxObj.startDesktopDriver()
        elif browser == BingRewards.MOBILE:
            self.firefoxObj.startMobileDriver()

        for index in range(self.numSearches[browser]):
            if browser == BingRewards.DESKTOP:
                print("Firefox %s search %d : \"%s\"" % (browser, index+1, self.searchesList[index]))
                self.firefoxObj.getDesktopUrl(BingRewards.base_url + self.searchesList[index])
            elif browser == BingRewards.MOBILE:
                print("Firefox %s search %d : \"%s\"" % (browser, index+1, 
                                                         self.searchesList[index + self.numSearches[BingRewards.DESKTOP]]))
                self.firefoxObj.getMobileUrl(BingRewards.base_url +
                                             self.searchesList[index + self.numSearches[BingRewards.DESKTOP]])
            sleep(random.uniform(1.25, 3.25))

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

        for index in range(self.numSearches[browser]):
            if browser == BingRewards.DESKTOP:
                print("Chrome %s search %d : \"%s\"" % (browser, index+1, self.searchesList[index]))
                self.chromeObj.getDesktopUrl(BingRewards.base_url + self.searchesList[index])
            elif browser == BingRewards.MOBILE:
                print("Chrome %s search %d : \"%s\"" % (browser, index+1,
                                                        self.searchesList[index + self.numSearches[BingRewards.DESKTOP]]))
                self.chromeObj.getMobileUrl(BingRewards.base_url +
                                            self.searchesList[index + self.numSearches[BingRewards.DESKTOP]])
            sleep(random.uniform(1.25, 3.25))

        if browser == BingRewards.DESKTOP:
            self.chromeObj.closeDesktopDriver()
        elif browser == BingRewards.MOBILE:
            self.chromeObj.closeMobileDriver()

    def runDesktopSearches(self):
        firefoxDesktopSearches = threading.Thread(name='ff_desktop', target=self.firefox_search, kwargs={
                                                  'browser': BingRewards.DESKTOP})
        firefoxDesktopSearches.start()

        chromeDesktopSearches = threading.Thread(name='chrome_desktop', target=self.chrome_search, kwargs={
                                                 'browser': BingRewards.DESKTOP})
        chromeDesktopSearches.start()

        firefoxDesktopSearches.join()
        chromeDesktopSearches.join()

    def runMobileSearches(self):
        firefoxMobileSearches = threading.Thread(name='ff_mobile', target=self.firefox_search, kwargs={
                                                 'browser': BingRewards.MOBILE})
        firefoxMobileSearches.start()

        chromeMobileSearches = threading.Thread(name='chrome_mobile', target=self.chrome_search, kwargs={
                                                'browser': BingRewards.MOBILE})
        chromeMobileSearches.start()

        firefoxMobileSearches.join()
        chromeMobileSearches.join()


def testChromeMobileGPSCrash():
    searchList = ["find my location", "near me", "weather"]
    bingRewards = BingRewards(None, desktopSearches=0, mobileSearches=len(searchList), UseFirefox=False,
                              UseChrome=True, searchesList=searchList)
    bingRewards.runMobileSearches()
    sleep(5)


def parseArgs():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-f', '--firefox', dest='firefox', action='store_true',
                        help='include this option to use firefox')
    parser.add_argument('-c', '--chrome', dest='chrome', action='store_true', help='include this option to use chrome')
    parser.add_argument('-m', '--mobile', dest='mobile_searches', type=int,
                        default=50, help='Number of Mobile Searches')
    parser.add_argument('-d', '--desktop', dest='desktop_searches', type=int,
                        default=70, help='Number of Desktop Searches')

    # Either load the default browser profile or load cookies saved from the microsoftLogin.py script"
    parser.add_argument('--cookies', dest='cookies', action='store_true',
                       help="include this option to load cookies that were set using the microsoftLogin.py script."
                       "the script was not used or no cookies were saved this will work as is this flag was not set. Use "
                            "this option if the pc you are running bingtool on doesnt have a GUI")
    parser.add_argument('--headless', dest='headless', action='store_true',
                        help='include this option to use headless mode')
    parser.add_argument('-a', '--artifact', dest='artifact_dir', type=str, help='Directory to both store bing rewards artifacts and look for '
                        "cookies created with the microsoftLogin.py script. If this option is not set the default value of None indicates to use"
                        " the users downloads directory. The artifacts stored are the downloaded webdriver binaries which get deleted at completion")
    parser.add_argument('-cl', '--chrome_location', dest='chrome_location', action='store_true', 
                        help='Check if the chrome mobile webdriver blocks prompts for allowing location. If this option is selected nothing else runs')
    return parser.parse_args()


def main():
    args = parseArgs()

    # This allows the script to work with a windows scheduler
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    if args.chrome_location is True:
        testChromeMobileGPSCrash()
        print("Chrome mobile location test complete, exiting")
        return
    
    if (args.firefox is False) and (args.chrome is False):
        print("Error : At least one browser must be selected. run \"%s --help\"" % sys.argv[0])
        sys.exit(0)

    bingRewards = BingRewards(args.artifact_dir, desktopSearches=args.desktop_searches, mobileSearches=args.mobile_searches,
                              UseFirefox=args.firefox, UseChrome=args.chrome, useHeadless=args.headless, loadcookies=args.cookies)
    print("Init BingRewards Complete")
    bingRewards.runDesktopSearches()

    print("runDesktopSearches Complete")
    bingRewards.runMobileSearches()
    print("runMobileSearches Complete")

    print("Main COMPLETE")


if __name__ == '__main__':
    main()
