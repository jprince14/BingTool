from FirefoxWebDriver import FirefoxWebDriver

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
import getpass
import pickle
import os
import errno
import argparse

EMAILFIELD = (By.ID, "i0116")
PASSWORDFIELD = (By.ID, "i0118")
NEXTBUTTON = (By.ID, "idSIButton9")
STAYSIGNEDIN = (By.ID, "idChkBx_PWD_KMSI0Pwd")

import time
from distutils import dir_util

def parseArgs():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-f', '--firefox', dest='firefox', action='store_true', help='include this option to use firefox')
    parser.add_argument('-c', '--chrome', dest='chrome', action='store_true', help='include this option to use chrome')
    parser.add_argument('--headless', dest='headless', action='store_true', help='include this option to use headless mode')
    return parser.parse_args()

def main():
    args = parseArgs()
    print("This script is not yet complete, at present state logins made through selenium are not saved back to the browser profile")

    if args.firefox == True:    

        ff_driver = FirefoxWebDriver(useHeadless=args.headless)
        ff_driver.startDesktopDriver()  

        ff_driver.firefoxDesktopDriver.get('https://login.live.com')

        # wait for email field and enter email
        username = input("Enter Microsoft username:")
        WebDriverWait(ff_driver.firefoxDesktopDriver, 10).until(EC.element_to_be_clickable(EMAILFIELD)).send_keys(username)
        # Click Next
        WebDriverWait(ff_driver.firefoxDesktopDriver, 10).until(EC.element_to_be_clickable(NEXTBUTTON)).click()
        # wait for password field and enter password
        thepasswd = getpass.getpass("Enter the password:")
        WebDriverWait(ff_driver.firefoxDesktopDriver, 10).until(EC.element_to_be_clickable(STAYSIGNEDIN)).click()
          
        WebDriverWait(ff_driver.firefoxDesktopDriver, 10).until(EC.element_to_be_clickable(PASSWORDFIELD)).send_keys(thepasswd)
          
        WebDriverWait(ff_driver.firefoxDesktopDriver, 10).until(EC.element_to_be_clickable(NEXTBUTTON)).click()

        print("TODO - What about two factor login")

        if not os.path.exists(os.path.dirname(ff_driver.cookie_file)):
            try:
                os.makedirs(os.path.dirname(ff_driver.cookie_file))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        
        #Save the cookies
        pickle.dump(ff_driver.firefoxDesktopDriver.get_cookies() , open(ff_driver.cookie_file,"wb"))          
    
        
    if args.chrome == True:
        pass
    


if __name__ == "__main__":
    main()
