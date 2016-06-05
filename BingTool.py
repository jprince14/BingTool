'''
Created on Jun 2, 2016

'''
import pip

#Make sure that Selenium is installed
installed_packages = pip.get_installed_distributions()
flat_installed_packages = [package.project_name for package in installed_packages]
if "selenium" not in flat_installed_packages:
    pip.main(['install', '-U', 'selenium'])

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import random
from time import sleep
import platform
import os,sys

controlKey = Keys.CONTROL
base_url = "http://www.bing.com/search?q="

if platform.system() == "Windows":
    ffdirect = os.path.join(os.getenv('APPDATA') , "Mozilla\\Firefox\\Profiles\\")
    ffdirect = os.path.join(ffdirect, os.listdir(ffdirect)[0]).replace("\\","/")
    chromedirect = os.path.join(os.getenv('LOCALAPPDATA'),"Google\\Chrome\\User Data\\").replace("\\","/")
    controlKey = Keys.CONTROL
elif platform.system() == "Darwin":
#Mac
    controlKey = Keys.COMMAND
    chromedirect = os.path.join(os.environ['HOME'], "Library/Application Support/Google/Chrome/Default/")
    ffdirect = os.path.join(os.environ['HOME'], "Library/Application Support/Firefox/Profiles/")
    ffdirect = os.path.join(ffdirect + os.listdir(ffdirect)[0])
    
    
Edge = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36 Edge/12.0"
SafariMobile = "Mozilla/5.0 (iPhone; CPU iPhone OS 9_2 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/47.0.2526.70 Mobile/13C71 Safari/601.1.46"

if platform.system() == "Windows":
    scriptsDir = os.path.join(os.path.dirname(sys.executable) , "Scripts")
    if "chromedriver.exe" not in os.listdir(scriptsDir):
            print ("Need to install chromedriver to directory \"%s\"\n" % (scriptsDir))
            exit(0)
if platform.system() == "Darwin":

searches = ["BALTIMORE RAVENS",
"BALTIMORE ORIOLES",
"Baltimore Blast",
"Baltimore Thunder",
"NCAA Basketball scored",
"nfl preseason rankings",
"Alabama",
"Alaska",
"Arizona",
"Arkansas",
"California",
"Colorado",
"Connecticut",
"Delaware",
"Florida",
"Georgia",
"Hawaii",
"Idaho",
"Illinois",
"Indiana",
"Iowa",
"Kansas",
"Kentucky",
"Louisiana",
"Maine",
"Maryland",
"Massachusetts",
"Michigan",
"Minnesota",
"Mississippi",
"Missouri",
"Montana",
"Nebraska",
"Nevada",
"New Hampshire",
"New Jersey",
"New Mexico",
"New York",
"North Carolina",
"North Dakota",
"Ohio",
"Oklahoma",
"Oregon",
"Pennsylvania",
"Rhode Island",
"South Carolina",
"South Dakota",
"Tennessee",
"Texas",
"Utah",
"Vermont",
"Virginia",
"Washington",
"West Virginia",
"Wisconsin",
"Wyoming",
"District of Columbia",
"Puerto Rico",
"Guam",
"American Samoa",
"U.S. Virgin Islands",
"Northern Mariana Islands",
]

DESKTOP = True
MOBILE = True
FF = False
CHRO = True


if DESKTOP == True:
    if FF == True:
        firefox_edge_profile = webdriver.FirefoxProfile(ffdirect)
        firefox_edge_profile.set_preference("general.useragent.override", Edge)
        firefox_edge = webdriver.Firefox(firefox_edge_profile)

    if CHRO == True:
        chrome_desktop_opts = Options()
        chrome_desktop_opts.add_argument("user-agent=" + Edge)
        #TODO: When I comment out this line chrome works
        chrome_desktop_opts.add_argument("user-data-dir=" + chromedirect)
        chromeDesktopDriver = webdriver.Chrome(chrome_options=chrome_desktop_opts)

    for x in range(1):
        pick = random.randint(0,len(searches)-1)
        new = searches[pick].replace(' ', '%20')
        website = base_url + new
        if FF == True:
            firefox_edge.get(website)
            firefox_edge.find_element_by_tag_name("body").send_keys(controlKey + "t")
        if CHRO == True:
            chromeDesktopDriver.get(website)
            chromeDesktopDriver.find_element_by_tag_name("body").send_keys(controlKey + "t")
            chromeDesktopDriver.find_element_by_tag_name("body").send_keys(controlKey + Keys.TAB)
#             tabs = chromeDesktopDriver.getWindowHandles()
#             chromeDesktopDriver.switchTo().window(tabs.get(x));
        sleep(random.uniform(2.0,5.25))

    if FF == True:
        firefox_edge.quit()
    if CHRO == True:
        chromeDesktopDriver.quit()



if MOBILE == True:
    if FF == True:   
        firefox_mobile_profile = webdriver.FirefoxProfile(ffdirect)
        firefox_mobile_profile.set_preference("general.useragent.override", SafariMobile)
        firefox_mobile = webdriver.Firefox(firefox_mobile_profile)
 
    if CHRO == True:   
        chrome_mobile_opts = Options()
        chrome_mobile_opts.add_argument("user-agent=" + SafariMobile)
        chrome_mobile_opts.add_argument("user-data-dir=" + chromedirect)
        chromeMobileDriver = webdriver.Chrome(chrome_options=chrome_mobile_opts)
            
    for x in range(25):
        pick = random.randint(0,len(searches)-1)
        new = searches[pick].replace(' ', '%20')
        website = base_url + new
        if FF == True:
            firefox_mobile.get(website)
            firefox_mobile.find_element_by_tag_name("body").send_keys(controlKey + "t")
        if CHRO == True:
            chromeMobileDriver.get(website)
            chromeMobileDriver.find_element_by_tag_name("body").send_keys(controlKey + "t")
            chromeMobileDriver.find_element_by_tag_name("body").send_keys(controlKey + Keys.TAB)

        sleep(random.uniform(2.0,5.25))

    if FF == True:
        firefox_mobile.quit()
    if CHRO == True:
        chromeMobileDriver.quit()


# chromeDriver.get("http://www.whoishostingthis.com/tools/user-agent/")


