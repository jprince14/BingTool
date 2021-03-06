from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import selenium
import platform
import pickle
import bs4 as BeautifulSoup
import os
import sys
import zipfile
import tarfile
import io


class FirefoxWebDriver(object):

    def __init__(self, artifact_storage_dir, desktopUA=None, mobileUA=None, useHeadless=False, loadCookies=False, load_default_profile=True):
        self.desktopUA = desktopUA
        self.mobileUA = mobileUA
        self.logged_in = False
        self.driverURL = "https://github.com/mozilla/geckodriver/releases/latest"
        self.githubUrl = "https://github.com"
        self.mobileRunning = False
        self.desktopRunning = False
        self.windowsURL = None
        self.macURL = None
        self.linuxURL = None
        self.getWebdriverURL(self.driverURL)
        self.driverBinary = None
        self.useHeadless = useHeadless
        self.loadCookies = loadCookies
        self.cookies = None
        self.loadDefaultProfile = load_default_profile
        self.artifact_storage_dir = artifact_storage_dir

        if platform.system() == "Windows":
            profilesDir = os.path.join(os.getenv('APPDATA'), "Mozilla", "Firefox", "Profiles")
            self.getDefaultProfile(profilesDir)
            self.checkIfGeckoDriverAlreadyExists()
            self.getGeckoDriver_zip(self.windowsURL)

        elif platform.system() == "Darwin":
            # Mac
            profilesDir = os.path.join(os.environ['HOME'], "Library", "Application Support", "Firefox", "Profiles")
            self.getDefaultProfile(profilesDir)
            self.checkIfGeckoDriverAlreadyExists()
            self.getGeckoDriver_tar_gz(self.macURL)

        elif platform.system() == "Linux":
            profilesDir = os.path.join(os.environ['HOME'], ".mozilla", "firefox")
            self.getDefaultProfile(profilesDir)
            self.checkIfGeckoDriverAlreadyExists()
            self.getGeckoDriver_tar_gz(self.linuxURL)

        for file in os.listdir(self.artifact_storage_dir):
            if (file.startswith("geckodriver")) and (not file.endswith(".zip")) and (not file.endswith(".gz")) and (not file.endswith(".log")) and os.path.isfile(os.path.join(self.artifact_storage_dir, file)):
                self.driverBinary = os.path.join(self.artifact_storage_dir, file)
                os.chmod(self.driverBinary, 0o777)

        self.cookie_file = os.path.join(self.artifact_storage_dir, "bing_cookies", "firefox_cookies.pkl")
        if self.loadCookies == True:
            if os.path.exists(self.cookie_file):
                self.cookies = pickle.load(open(self.cookie_file, "rb"))
                print("Loading Cookies from %s in firefox" % self.cookie_file)

    def getDefaultProfile(self, profileDir):
        for file in os.listdir(profileDir):
            if file.endswith(".default"):
                self.ffProfileDir = os.path.join(profileDir, file)
                return

        raise ("Unable to find default firefox profile directory")

    def checkIfGeckoDriverAlreadyExists(self):
        for file in os.listdir(self.artifact_storage_dir):
            if (file.startswith("geckodriver")) and (not file.endswith(".zip")) and (not file.endswith(".gz")) and (not file.endswith(".log")) and os.path.isfile(os.path.join(self.artifact_storage_dir, file)):
                os.remove(os.path.join(self.artifact_storage_dir, file))

    def getGeckoDriver_zip(self, URL):
        if sys.version_info.major <= 2:
            import urllib2
            zipDriver = urllib2.urlopen(URL).read()
            zip_ref = zipfile.ZipFile(io.BytesIO(zipDriver))
            zip_ref.extractall(self.artifact_storage_dir)
            zip_ref.close()
        elif sys.version_info.major >= 3:
            import urllib.request
            zipDriver = urllib.request.urlopen(URL).read()
            zip_ref = zipfile.ZipFile(io.BytesIO(zipDriver))
            zip_ref.extractall(self.artifact_storage_dir)
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
        tar.extractall(path=self.artifact_storage_dir)
        tar.close()

    def __del__(self):
        if self.desktopRunning == True:
            self.closeDesktopDriver()
        if self.mobileRunning == True:
            self.closeMobileDriver()
        try:
            os.remove(self.driverBinary)
        except:
            if self.driverBinary == None:
                print("ERROR: driverBinary = None")
            else:
                print("Failed to delete firefox web driver binary \"%s\"" % (self.driverBinary))

        print("Firefox Cleanup Complete")

    def getWebdriverURL(self, driverPageURL):
        if sys.version_info.major <= 2:
            import urllib2
            html_page = urllib2.urlopen(driverPageURL)

        elif sys.version_info.major >= 3:
            import urllib.request
            html_page = urllib.request.urlopen(driverPageURL)

        soup = BeautifulSoup.BeautifulSoup(html_page, "html.parser")

        # Old way
#         downloadsSection = soup.find('ul', {"class": "release-downloads"})
#         if downloadsSection == None:
#             downloadsSection= soup.find('ul', {"class": "Latest release"})
#         driverList = downloadsSection.findAll("a")
        driverList = soup.findAll("a")

        for driver in driverList:
            driverUrl = driver['href']
            if "linux64.tar.gz" in driverUrl:
                self.linuxURL = self.githubUrl + driverUrl
            elif "macos.tar.gz" in driverUrl:
                self.macURL = self.githubUrl + driverUrl
            elif "win64.zip" in driverUrl:
                self.windowsURL = self.githubUrl + driverUrl

        if self.windowsURL == None or self.macURL == None or self.linuxURL == None:
            raise Exception("Failed to find URL's for Firefox Webdrivers")

    def startDesktopDriver(self):

        options = Options()
        options.set_headless(self.useHeadless)
        if self.loadDefaultProfile == True:
            firefoxDeskopProfile = webdriver.FirefoxProfile(profile_directory=self.ffProfileDir)
        else:
            firefoxDeskopProfile = None
        if self.desktopUA != None:
            firefoxDeskopProfile.set_preference("general.useragent.override", self.desktopUA)

        self.firefoxDesktopDriver = webdriver.Firefox(
            firefox_profile=firefoxDeskopProfile, executable_path=self.driverBinary, firefox_options=options)
        self.desktopRunning = True
        if self.loadCookies == True and self.cookies != None:
            self.firefoxDesktopDriver.delete_all_cookies()
            # Loading cookies only works if we are at a site the cookie would work for
            self.getDesktopUrl("https://login.live.com")
            for cookie in self.cookies:
                # print("Adding cookie to Firefox Desktop Driver: %s" % str(cookie))
                new_cookie = {}
                new_cookie['name'] = cookie['name']
                new_cookie['value'] = cookie['value']
                try:
                    self.firefoxDesktopDriver.add_cookie(new_cookie)
                except selenium.common.exceptions.InvalidCookieDomainException:
                    continue

        self.check_if_logged_in()

    def check_if_logged_in(self):
        
        DISPLAY_NAME = (By.ID, "displayName")
        ID_ALIAS = (By.ID, "idAliasHeadingText")
        self.firefoxDesktopDriver.get("https://account.live.com/names/Manage?mkt=en-US&refd=account.microsoft.com&refp=profile")
    
        try:
            title_elem = WebDriverWait(self.firefoxDesktopDriver, 5).until(EC.visibility_of_element_located(DISPLAY_NAME))
            print("Logged in as %s" % (title_elem.text))
            self.logged_in = True
        except:
            try:
                WebDriverWait(self.firefoxDesktopDriver, 5).until(EC.visibility_of_element_located(ID_ALIAS))
                print("Logged in but unable to confirm the user name")
                self.logged_in = True
            except:        
                print("Not logged in")
                self.logged_in = False

    def startMobileDriver(self):

        options = Options()
        options.set_headless(self.useHeadless)
        if self.loadDefaultProfile == True:
            firefoxMobileProfile = webdriver.FirefoxProfile(profile_directory=self.ffProfileDir)
        else:
            firefoxMobileProfile = None
        if self.mobileUA != None:
            firefoxMobileProfile.set_preference("general.useragent.override", self.mobileUA)

        self.firefoxMobileDriver = webdriver.Firefox(
            firefox_profile=firefoxMobileProfile, executable_path=self.driverBinary, firefox_options=options)
        self.mobileRunning = True
        if self.loadCookies == True and self.cookies != None:
            self.firefoxMobileDriver.delete_all_cookies()
            # Loading cookies only works if we are at a site the cookie would work for
            self.getMobileUrl("https://login.live.com")
            for cookie in self.cookies:
                # print("Adding cookie to Firefox Mobile Driver: %s" % str(cookie))
                # new_cookie = {}
                # new_cookie['name'] = cookie['name']
                # new_cookie['value'] = cookie['value']
                try:
                    self.firefoxMobileDriver.add_cookie(cookie)
                except selenium.common.exceptions.InvalidCookieDomainException:
                    contine


    def getDesktopUrl(self, url):
        if self.desktopRunning == True:
            if not url.startswith("http"):
                url = "http://" + url
            self.firefoxDesktopDriver.get(url)
        else:
            print("Firefox desktop webdriver is not open")

    def getMobileUrl(self, url):
        if self.mobileRunning == True:
            if not url.startswith("http"):
                url = "http://" + url
            self.firefoxMobileDriver.get(url)
        else:
            print("Firefox desktop webdriver is not open")

    def closeDesktopDriver(self):
        if self.desktopRunning == True:
            try:
                self.firefoxDesktopDriver.quit()
                self.desktopRunning = False
            except Exception as e:
                print("Hit exception following exception when trying to close the Firefox Desktop driver\n\t%s" % e)

    def closeMobileDriver(self):
        if self.mobileRunning == True:
            try:
                self.firefoxMobileDriver.quit()
                self.mobileRunning = False
            except Exception as e:
                print("Hit exception following exception when trying to close the Firefox Mobile driver\n\t%s" % e)
