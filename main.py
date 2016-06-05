# def seleniumCheck():
#     import pip
#     #Make sure that Selenium is installed
#     installed_packages = pip.get_installed_distributions()
#     flat_installed_packages = [package.project_name for package in installed_packages]
#     if "selenium" not in flat_installed_packages:
#         pip.main(['install', '-U', 'selenium'])
    

from FirefoxWebDriver import FirefoxWebDriver
from ChromeWebDriver import ChromeWebDriver

Edge = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36 Edge/12.0"
SafariMobile = "Mozilla/5.0 (iPhone; CPU iPhone OS 9_2 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/47.0.2526.70 Mobile/13C71 Safari/601.1.46"



if __name__ == '__main__':
    firefox = FirefoxWebDriver(Edge,SafariMobile)
    firefox.startDesktopDriver()
    firefox.getDesktopUrl("http://www.cnn.com")
    firefox.closeDesktopDriver()
    
    chrome = ChromeWebDriver(Edge,SafariMobile)
    chrome.startDesktopDriver()
    chrome.getDesktopUrl("http://www.cnn.com")
    chrome.closeDesktopDriver()