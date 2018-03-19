from FirefoxWebDriver import FirefoxWebDriver

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
import getpass

EMAILFIELD = (By.ID, "i0116")
PASSWORDFIELD = (By.ID, "i0118")
NEXTBUTTON = (By.ID, "idSIButton9")
STAYSIGNEDIN = (By.ID, "idChkBx_PWD_KMSI0Pwd")

import time
from distutils import dir_util

if __name__ == "__main__":
    
    print("This script is not yet complete, at present state logins made through selenium are not saved back to the browser profile")
    
    #This works but chranges made with selenium sessoins are not being saved 

    ff_driver = FirefoxWebDriver(useHeadless=False)
    ff_driver.startDesktopDriver()
    
    profiletmp = ff_driver.firefoxDesktopDriver.firefox_profile.path
    
    ff_driver.firefoxDesktopDriver.get('https://login.live.com')
#     
    # wait for email field and enter email
    username = input("Enter Microsoft username:")
    WebDriverWait(ff_driver.firefoxDesktopDriver, 10).until(EC.element_to_be_clickable(EMAILFIELD)).send_keys(username)
    # Click Next
    WebDriverWait(ff_driver.firefoxDesktopDriver, 10).until(EC.element_to_be_clickable(NEXTBUTTON)).click()
    # wait for password field and enter password
    thepasswd = getpass.getpass("Enter the password:")
    WebDriverWait(ff_driver.firefoxDesktopDriver, 10).until(EC.element_to_be_clickable(STAYSIGNEDIN)).click()
      
    WebDriverWait(ff_driver.firefoxDesktopDriver, 10).until(EC.element_to_be_clickable(PASSWORDFIELD)).send_keys(thepasswd)
      
    # Click Login - same id?
    WebDriverWait(ff_driver.firefoxDesktopDriver, 10).until(EC.element_to_be_clickable(NEXTBUTTON)).click()
    
    #TODO - What about two factor login
    
    time.sleep(5.0)
    dir_util.copy_tree(profiletmp,ff_driver.ffProfileDir, update=1)

#     if os.system("cp -R " + profiletmp + "/* " + ff_driver.ffProfileDir ):
#         print ("files should be copied :/")
