from FirefoxWebDriver import FirefoxWebDriver
from ChromeWebDriver import ChromeWebDriver

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium
import getpass
import pickle
import os
import errno
import argparse
import sys
import platform
import shutil

from selenium.webdriver.common.action_chains import ActionChains

if hasattr(__builtins__, 'raw_input'):
    # Python 2 compatibility.
    # raw_input in python 2 is the same as input
    # in python 3
    input = raw_input

EMAILFIELD = (By.ID, "i0116")
LOGIN_HEADER = (By.ID, "loginHeader")
PASSWORDFIELD = (By.ID, "i0118")
NEXTBUTTON = (By.ID, "idSIButton9")
STAYSIGNEDIN = (By.ID, "idChkBx_PWD_KMSI0Pwd")

# Proof Page
TWO_FACTOR_TITLE = (By.ID, "idDiv_SAOTCS_Title")
TWO_FACTOR_DEVICES = (By.CLASS_NAME, 'table-row')

# "Verify your identity"
# idDiv_SAOTCS_Proofs_Section

# Proof Confirmation Page
PROOF_DESCRIPTION = (By.ID, "idDiv_SAOTCS_ProofConfirmationDesc")
PROOF_BOX = (By.ID, "idTxtBx_SAOTCS_ProofConfirmation")
SEND_CODE = (By.ID, "idSubmit_SAOTCS_SendCode")


OTC_TITLE = (By.ID, "idDiv_SAOTCC_Title")
OTC_DESCRIPTION = (By.ID, "idDiv_SAOTCC_Description")
OTC_BOX = (By.ID, "idTxtBx_SAOTCC_OTC")
REMEMBER_DEVICE_BOX = (By.ID, "idChkBx_SAOTCC_TD")
VERIFY_BOX = (By.ID, "idSubmit_SAOTCC_Continue")

BAD_USERNAME = (By.ID, "usernameError")
BAD_PASSWORD = (By.ID, "passwordError")
BAD_PROOF = (By.ID, "id_SAOTCS_Error_ProofConfirmation")
OTC_ERROR = (By.ID, "idSpan_SAOTCC_Error_OTC")


DISPLAY_NAME = (By.ID, "displayName")
ID_ALIAS = (By.ID, "idAliasHeadingText")

import time

def parseArgs():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-f', '--firefox', dest='firefox', action='store_true',
                        help='include this option to use firefox')
    group.add_argument('-c', '--chrome', dest='chrome', action='store_true', help='include this option to use chrome')
    parser.add_argument('--headless', dest='headless', action='store_true',
                        help='include this option to use headless mode')
    parser.add_argument('--ignore_cookies', dest='ignore_cookies', action='store_false',
                        help='include this option to avoid loading any cookies that exist in the artifact directory')
    parser.add_argument('--ignore_profile', dest='ignore_profile', action='store_false',
                        help='include this option to avoid loading the default browser profile. If this option is set '
                            'loading cookies may not work')    
    parser.add_argument('-a', '--artifact', dest='artifact_dir', type=str, help="Directory to both store bing rewards artifacts and look for "
                        "cookies created with the microsoftLogin.py script. If this option is not set the default value of None indicates to use "
                        "the users downloads directory")
    return parser.parse_args()
 

def browser_login(wrapper_class, browserobj):
    
    login_status = wrapper_class.logged_in
    if login_status is False:
        
        browserobj.get('https://login.live.com')
    
        # wait for email field and enter email
        username = input("Enter Microsoft username : ")
        WebDriverWait(browserobj, 10).until(EC.element_to_be_clickable(EMAILFIELD)).send_keys(username)
        # Click Next
        WebDriverWait(browserobj, 10).until(EC.element_to_be_clickable(NEXTBUTTON)).click()
    
        try:
            password_title = WebDriverWait(browserobj, 10).until(EC.visibility_of_element_located(LOGIN_HEADER))
        except selenium.common.exceptions.TimeoutException:
            bad_user = WebDriverWait(browserobj, 10).until(EC.visibility_of_element_located(BAD_USERNAME))
            print("Error : \"%s\"" % bad_user.text.encode('ascii','ignore'))
            sys.exit(1)
    
        # wait for password field and enter password
        thepasswd = getpass.getpass("%s : " % "Enter Password")
        WebDriverWait(browserobj, 10).until(EC.element_to_be_clickable(STAYSIGNEDIN)).click()
    
        WebDriverWait(browserobj, 10).until(EC.element_to_be_clickable(PASSWORDFIELD)).send_keys(thepasswd)
    
        WebDriverWait(browserobj, 10).until(EC.element_to_be_clickable(NEXTBUTTON)).click()
    
        try:
            password_error = WebDriverWait(browserobj, 3).until(EC.visibility_of_element_located(BAD_PASSWORD))
            print("Error : \"%s\"" % password_error.text.encode('ascii','ignore'))
            sys.exit(2)
        except selenium.common.exceptions.TimeoutException:
            # The password was correct
            pass
    
        # Check if two factor is enabled on the account
        try:
            title_elem = WebDriverWait(browserobj, 3).until(EC.visibility_of_element_located(TWO_FACTOR_TITLE))
            two_factor = True
    
        except selenium.common.exceptions.TimeoutException:
            two_factor = False
    
        if (two_factor == True):
             # Select the two factor method
            tables = WebDriverWait(browserobj, 10).until(EC.presence_of_all_elements_located(TWO_FACTOR_DEVICES))
    
            print("Two Factor Authentication Page : %s" % title_elem.text.encode('ascii','ignore'))
    
            # Print the available two factor devices
            for num in range(len(tables)):
                print("%d : \"%s\"" % (num, tables[num].text.encode('ascii','ignore')))
    
            # Select the two factor device
            while True:
                selection = input("Enter a selection : ")
                selection = selection.encode('ascii', 'ignore')
    
                if (selection.isdigit()) and (int(selection) in list(range(len(tables)))):
                    selection = int(selection)
                    break
                print("Error Invalid Input")
    
            box_loc = tables[selection].location
            ac = ActionChains(browserobj)
            ac.move_to_element(tables[selection]).move_by_offset(
                box_loc['x'], box_loc['y']).click(on_element=tables[selection]).perform()
    
            # Verify the two factor method
            title_elem = WebDriverWait(browserobj, 10).until(EC.visibility_of_element_located(TWO_FACTOR_TITLE))
            print("%s" % title_elem.text.encode('ascii','ignore'))
    
            page_description = WebDriverWait(browserobj, 10).until(EC.visibility_of_element_located(PROOF_DESCRIPTION))
    
            verification = input("%s : " % page_description.text.encode('ascii','ignore'))
    
            WebDriverWait(browserobj, 10).until(EC.element_to_be_clickable(PROOF_BOX)).send_keys(verification)
    
            WebDriverWait(browserobj, 10).until(EC.element_to_be_clickable(SEND_CODE)).click()
    
            try:
                proof_error = WebDriverWait(browserobj, 3.0).until(EC.visibility_of_element_located(BAD_PROOF))
                print("Error : \"%s\"" % proof_error.text.encode('ascii','ignore'))
                sys.exit(3)
            except selenium.common.exceptions.TimeoutException:
                # The proof confirmation was correct
                pass
    
            # Enter the two factor one time code
            page_description = WebDriverWait(browserobj, 10).until(EC.visibility_of_element_located(OTC_DESCRIPTION))
            print("%s" % page_description.text.encode('ascii','ignore'))
    
            title_elem = WebDriverWait(browserobj, 10).until(EC.visibility_of_element_located(OTC_TITLE))
    
            otc_code = input("%s : " % title_elem.text.encode('ascii','ignore'))
    
            WebDriverWait(browserobj, 10).until(EC.element_to_be_clickable(OTC_BOX)).send_keys(otc_code)
    
            WebDriverWait(browserobj, 10).until(EC.element_to_be_clickable(REMEMBER_DEVICE_BOX)).click()
    
            WebDriverWait(browserobj, 10).until(EC.element_to_be_clickable(VERIFY_BOX)).click()
    
            try:
                otc_error = WebDriverWait(browserobj, 3).until(EC.visibility_of_element_located(OTC_ERROR))
                print("Error : \"%s\"" % otc_error.text.encode('ascii','ignore'))
                sys.exit(4)
            except selenium.common.exceptions.TimeoutException:
                # The proof confirmation was correct
                pass
            
    if not os.path.exists(os.path.dirname(wrapper_class.cookie_file)):
        try:
            os.makedirs(os.path.dirname(wrapper_class.cookie_file))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    browserobj.get('https://login.live.com')
#     pickle.dump(browserobj.get_cookies(), open(wrapper_class.cookie_file, "wb"), protocol=2)

    wrapper_class.check_if_logged_in()
    login_status = wrapper_class.logged_in
    
    
    if login_status is True:
#         shutil.move(wrapper_class.cookie_file + ".tmp", wrapper_class.cookie_file)
        import pdb
        pdb.set_trace()
        profiletmp = browserobj.profile.profile_dir
        import distutils.dir_util
        distutils.dir_util.copy_tree(os.path.join(profiletmp, "*"), wrapper_class.ffProfileDir)
        print("writing from %s to %s" % (os.path.join(profiletmp, "*"), wrapper_class.ffProfileDir))
#         print("Saving cookie to file %s" % wrapper_class.cookie_file)
    else:
        print("Do nothing")
#         os.remove(wrapper_class.cookie_file + ".tmp")
  
def main():
    args = parseArgs()

    if platform.system() == "Windows":
        downloads_dir = os.path.join(os.getenv('HOMEPATH'), "Downloads")
    elif platform.system() == "Darwin":
        downloads_dir = os.path.join(os.getenv('HOME'), "Downloads")
    elif platform.system() == "Linux":
        downloads_dir = os.path.join(os.getenv('HOME'), "Downloads")

    if args.artifact_dir == None:
        artifacts_dir = downloads_dir
    else:
        if os.path.exists(args.artifact_dir):
            artifacts_dir = args.artifact_dir
        else:
            raise Exception("The location %s does not exist" % args.artifact_dir)

    if args.firefox == True:

        browser_wrapper = FirefoxWebDriver(artifacts_dir, useHeadless=args.headless,
                                           loadCookies=args.ignore_cookies, load_default_profile=args.ignore_profile)
        browser_wrapper.startDesktopDriver()
        browser_obj = browser_wrapper.firefoxDesktopDriver
        print("Firefox Login")
        browser_login(browser_wrapper, browser_obj)

    if args.chrome == True:
        browser_wrapper = ChromeWebDriver(artifacts_dir, useHeadless=args.headless,
                                          loadCookies=args.ignore_cookies, load_default_profile=args.ignore_profile)
        browser_wrapper.startDesktopDriver()
        browser_obj = browser_wrapper.chromeDesktopDriver
        print("Chrome Login")
        browser_login(browser_wrapper, browser_obj)


if __name__ == "__main__":
    main()
