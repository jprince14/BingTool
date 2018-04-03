from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import platform
import os
import sys
import zipfile
import io
import stat
import bs4 as BeautifulSoup
import re
import pickle


class ChromeWebDriver(object):
    SUCCESS = 0
    FAILURE = 1

    linux32_file = "/chromedriver_linux32.zip"
    linux64_file = "/chromedriver_linux64.zip"
    mac32 = "/chromedriver_mac32.zip"
    windows32 = "/chromedriver_win32.zip"

    win = "windows"
    mac = "mac"
    linux64 = "linux64"
    linux32 = "linux32"

    def __init__(self, artifact_storage_dir, desktopUA=None, mobileUA=None, useHeadless=False, loadCookies=False, load_default_profile=True):
        self.desktopUA = desktopUA
        self.mobileUA = mobileUA

        self.winDriver = None
        self.macDriver = None
        self.linux64Driver = None
        self.linux32Driver = None

        self.desktopRunning = False
        self.mobileRunning = False
        self.useHeadless = useHeadless
        self.loadCookies = loadCookies
        self.cookies = None
        self.loadDefaultProfile = load_default_profile

        self.artifact_storage_dir = artifact_storage_dir

        self.DriverURLDict = {ChromeWebDriver.win: None, ChromeWebDriver.mac: None,
                              ChromeWebDriver.linux32: None, ChromeWebDriver.linux64: None}

        if platform.system() == "Windows":
            self.controlKey = Keys.CONTROL
            self.chromedirect = os.path.join(os.getenv('LOCALAPPDATA'), "Google", "Chrome", "User Data")

            self.os = ChromeWebDriver.win

        elif platform.system() == "Darwin":
            # Mac
            self.controlKey = Keys.COMMAND
            self.chromedirect = os.path.join(os.getenv('HOME'),
                                             "Library", "Application Support", "Google", "Chrome", "Default")
            self.os = ChromeWebDriver.mac

        elif platform.system() == "Linux":
            self.controlKey = Keys.COMMAND
            self.chromedirect = os.path.join(os.getenv('HOME'),
                                             ".config", "Google", "Chrome", "Default")
            self.os = ChromeWebDriver.linux64

        self.getChromeDriver()

        for file in os.listdir(self.artifact_storage_dir):
            if ((file.startswith("chromedriver")) and (not file.endswith(".zip"))):
                self.webDriver = os.path.join(self.artifact_storage_dir, file)
                os.chmod(self.webDriver, 0o777)

                break

        self.cookie_file = os.path.join(self.artifact_storage_dir, "bing_cookies", "chrome_cookies.pkl")
        if self.loadCookies == True:
            if os.path.exists(self.cookie_file):
                self.cookies = pickle.load(open(self.cookie_file, "rb"))
                print("Loading Cookies from %s in chrome" % self.cookie_file)

    def __del__(self):
        if self.desktopRunning == True:
            self.closeDesktopDriver()
        if self.mobileRunning == True:
            self.closeMobileDriver()
        try:
            os.remove(self.webDriver)
        except:
            print("Failed to delete chrome web driver binary \"%s\"" % (self.webDriver))

        print("Chrome Cleanup Complete")

    def checkForChromeDriver(self):
        for file in os.listdir(self.artifact_storage_dir):
            if ((file.startswith("chromedriver")) and (not file.endswith(".zip"))):
                return ChromeWebDriver.SUCCESS
        return ChromeWebDriver.FAILURE

    def getDriverUrl(self):

        url = "https://sites.google.com/a/chromium.org/chromedriver/downloads"

        html_page = None
        if sys.version_info.major <= 2:
            import urllib2
            html_page = urllib2.urlopen(url)

        elif sys.version_info.major >= 3:
            import urllib.request
            html_page = urllib.request.urlopen(url)

        soup = BeautifulSoup.BeautifulSoup(html_page, "html.parser")
        urlfound = False
        downloadURL = None
        for table in soup.findAll('table'):
            links = table.findAll('a')
            for x in range(len(links)):
                if "TOC-Latest-Release" in str(links[x]):
                    downloadURL = links[x+1]['href']
                    urlfound = True
                    break
            if urlfound == True:
                break

        pattern = "index.html\?path=([0-9a-fA-F-.]{1,7})\/"
        regexFind = re.search(pattern, downloadURL)
        version = regexFind.group(1)

        baseurl = "http://chromedriver.storage.googleapis.com/"

        self.DriverURLDict[self.linux32] = baseurl + version + ChromeWebDriver.linux32_file
        self.DriverURLDict[self.linux64] = baseurl + version + ChromeWebDriver.linux64_file
        self.DriverURLDict[self.mac] = baseurl + version + ChromeWebDriver.mac32
        self.DriverURLDict[self.win] = baseurl + version + ChromeWebDriver.windows32

    def getChromeDriver(self):
        self.getDriverUrl()
        if sys.version_info.major <= 2:
            import urllib2
            zipDriver = urllib2.urlopen(self.DriverURLDict[self.os]).read()
            zip_ref = zipfile.ZipFile(io.BytesIO(zipDriver))
            zip_ref.extractall(self.artifact_storage_dir)
            zip_ref.close()
        elif sys.version_info.major >= 3:
            import urllib.request
            zipDriver = urllib.request.urlopen(self.DriverURLDict[self.os]).read()
            zip_ref = zipfile.ZipFile(io.BytesIO(zipDriver))
            zip_ref.extractall(self.artifact_storage_dir)
            zip_ref.close()

        for file in os.listdir(self.artifact_storage_dir):
            if ((file.startswith("chromedriver")) and (not file.endswith(".zip"))):
                filePath = os.path.join(self.artifact_storage_dir, file)
                st = os.stat(filePath)
                os.chmod(filePath, st.st_mode | stat.S_IEXEC)

    def startDesktopDriver(self):
        chrome_desktop_opts = Options()
        chrome_desktop_opts.add_argument('disable-infobars')
        chrome_desktop_opts.set_headless(self.useHeadless)
        # prefs prevents gps popups
        prefs = {"profile.default_content_setting_values.geolocation": 2}
        if self.desktopUA != None:
            chrome_desktop_opts.add_argument("user-agent=" + self.desktopUA)
        if self.loadDefaultProfile == True:
            chrome_desktop_opts.add_argument("user-data-dir=" + self.chromedirect)
        self.chromeDesktopDriver = webdriver.Chrome(executable_path=self.webDriver, chrome_options=chrome_desktop_opts)
        self.desktopRunning = True
        if self.loadCookies == True and self.cookies != None:
            self.getDesktopUrl("https://login.live.com")
            self.chromeDesktopDriver.delete_all_cookies()
            for cookie in self.cookies:
                # print("Adding cookie to Chrome Desktop Driver: %s" % str(cookie))
                new_cookie = {}
                new_cookie['name'] = cookie['name']
                new_cookie['value'] = cookie['value']
                self.chromeDesktopDriver.add_cookie(new_cookie)

        self.find_username()

    def find_username(self):
        # This only needs to be run from the desktop browser

        self.chromeDesktopDriver.get(
            "https://account.live.com/names/Manage?mkt=en-US&refd=account.microsoft.com&refp=profile")
        DISPLAY_NAME = (By.ID, "displayName")
        try:
            title_elem = WebDriverWait(self.chromeDesktopDriver, 3).until(
                EC.visibility_of_element_located(DISPLAY_NAME))
            print("\n\nLogged into chrome as %s\n\n" % (title_elem.text))
        except:
            print("\n\nNot logged in on chrome\n\n")

    def startMobileDriver(self):
        chrome_mobile_opts = Options()
        chrome_mobile_opts.add_argument('disable-infobars')
        chrome_mobile_opts.set_headless(self.useHeadless)
        if self.mobileUA != None:
            chrome_mobile_opts.add_argument("user-agent=" + self.mobileUA)
        if self.loadDefaultProfile == True:
            chrome_mobile_opts.add_argument("user-data-dir=" + self.chromedirect)

        # prefs prevents gps popups
        prefs = {"profile.default_content_setting_values.geolocation": 2}
        chrome_mobile_opts.add_experimental_option("prefs", prefs)
        self.chromeMobileDriver = webdriver.Chrome(executable_path=self.webDriver, chrome_options=chrome_mobile_opts)
        self.mobileRunning = True

        if self.loadCookies == True and self.cookies != None:
            self.getMobileUrl("https://login.live.com")
            self.chromeMobileDriver.delete_all_cookies()
            for cookie in self.cookies:
                # print("Adding cookie to Chrome Mobile Driver: %s" % str(cookie))
                new_cookie = {}
                new_cookie['name'] = cookie['name']
                new_cookie['value'] = cookie['value']
                self.chromeMobileDriver.add_cookie(new_cookie)

    def getDesktopUrl(self, url):
        if self.desktopRunning == True:
            if not url.startswith("http"):
                url = "http://" + url
            self.chromeDesktopDriver.get(url)
        else:
            print("Chrome desktop webdriver is not open")

    def getMobileUrl(self, url):
        if self.mobileRunning == True:
            if not url.startswith("http"):
                url = "http://" + url
            self.chromeMobileDriver.get(url)
        else:
            print("Chrome mobile webdriver is not open")

    def closeDesktopDriver(self):
        if self.desktopRunning == True:
            try:
                self.chromeDesktopDriver.stop_client()
                self.chromeDesktopDriver.close()
                self.chromeDesktopDriver.quit()
                self.desktopRunning = False
            except Exception as e:
                print("Hit exception following exception when trying to close the Chrome Desktop driver\n\t%s" % e)

    def closeMobileDriver(self):
        if self.mobileRunning == True:
            try:
                self.chromeMobileDriver.stop_client()
                self.chromeMobileDriver.close()
                self.chromeMobileDriver.quit()
                self.mobileRunning = False
            except Exception as e:
                print("Hit exception following exception when trying to close the Chrome Mobile driver\n\t%s" % e)
