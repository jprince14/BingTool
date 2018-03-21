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

#Proof Page
idDiv_SAOTCS_Title
"Verify your identity"
idDiv_SAOTCS_Proofs_Section

#Proof COnfirmation Page
PROOF_DESCRIPTION = (By.ID, "idDiv_SAOTCS_ProofConfirmationDesc")
PROOF_BOX = (By.ID, "idTxtBx_SAOTCS_ProofConfirmation")
SEND_CODE = (By.ID, "idSubmit_SAOTCS_SendCode")


PROOF_DESCRIPTION = (By.ID, "idDiv_SAOTCC_Description")
OTC_BOX = (By.ID, "idTxtBx_SAOTCC_OTC")
REMEMBER_DEVICE_BOX = (By.ID, "idChkBx_SAOTCC_TD")
VERIFY_BOX = (By.ID, "idSubmit_SAOTCC_Continue")







import time
from distutils import dir_util

def parseArgs():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-f', '--firefox', dest='firefox', action='store_true', help='include this option to use firefox')
    parser.add_argument('-c', '--chrome', dest='chrome', action='store_true', help='include this option to use chrome')
    parser.add_argument('--headless', dest='headless', action='store_true', help='include this option to use headless mode')
    return parser.parse_args()

def browser_login(self, wrapper_class, browserobj):
        browserobj.get('https://login.live.com')

        # wait for email field and enter email
        username = input("Enter Microsoft username:")
        WebDriverWait(browserobj, 10).until(EC.element_to_be_clickable(EMAILFIELD)).send_keys(username)
        # Click Next
        WebDriverWait(browserobj, 10).until(EC.element_to_be_clickable(NEXTBUTTON)).click()
        # wait for password field and enter password
        thepasswd = getpass.getpass("Enter the password:")
        WebDriverWait(browserobj, 10).until(EC.element_to_be_clickable(STAYSIGNEDIN)).click()
          
        WebDriverWait(browserobj, 10).until(EC.element_to_be_clickable(PASSWORDFIELD)).send_keys(thepasswd)
          
        WebDriverWait(browserobj, 10).until(EC.element_to_be_clickable(NEXTBUTTON)).click()

        print("TODO - What about two factor login")

        if not os.path.exists(os.path.dirname(wrapper_class.cookie_file)):
            try:
                os.makedirs(os.path.dirname(wrapper_class.cookie_file))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        
        #Save the cookies
        pickle.dump(browserobj.get_cookies() , open(wrapper_class.cookie_file,"wb"))          


def main():
    args = parseArgs()
    print("This script is not yet complete, at present state logins made through selenium are not saved back to the browser profile")

    if args.firefox == True:    

        browser_wrapper = FirefoxWebDriver(useHeadless=args.headless)
        browser_wrapper.startDesktopDriver()  
        browser_obj = browser_wrapper.firefoxDesktopDriver
        print("Firefox Login")
        browser_login(browser_wrapper, browser_obj)
    
    if args.chrome == True:
        browser_wrapper = ChromeWebDriver(useHeadless=args.headless)
        browser_wrapper.startDesktopDriver()  
        browser_obj = browser_wrapper.chromeDesktopDriver
        print("Chrome Login")
        browser_login(browser_wrapper, browser_obj)
    
    


if __name__ == "__main__":
    main()
