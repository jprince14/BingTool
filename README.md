# BingTool

# About BingTool

BingTool supports automating bing rewards for two accounts at a time, the tools works by using the selenium browser automation platform. BingTool does not require any credentials, as long as you are logged into the browser that selenium launches then the searches will count towards bing rewards. BingTool emulates a mobile browser so users will get points for both desktop and mobile searches. Only firefox and chrome are supported, BingTool will run on Windows, macOS or Linux. BingTool can be run in the cloud and in non-gui enviroments using headless mode.

BingTool automates the downloading of selenium webdrivers, they are stored in the Downloads directory and deleted after the script completes.
	
BingTool can run in Python 2 or Python 3. Python 3 is preferred
	
# Instructions to set up BingTool

## Semi-automated setup up of BingTool on on Linux

Run one of the following commands
	
	bash <(wget -qO- https://raw.githubusercontent.com/jprince14/BingTool/master/setupBing.sh)
	
	bash <(curl -s https://raw.githubusercontent.com/jprince14/BingTool/master/setupBing.sh)

After executing the setupBing.sh script you need to log into the linux computer and sign into you Microsoft accouts for Firefox and/or Chrome. For computers without a GUI (such as a remote linux server) this can be done using the microsoftLogin.py script.

## Manual Instructions

1) Download Python https://www.python.org/downloads/ or install through a package manager in linux

2) Download and Update pip. If pip is not installed on your system follow the instuctions at https://pip.pypa.io/en/stable/installing/. In linux just install python3-pip and/or python-pip your
a package manager.
	
3) Install the prerequisite packages. Run the following commands:

	For python 2 replace pip3 with pip

	Linux/mac:
	
		sudo pip3 install selenium
		sudo pip3 install setuptools 
		sudo pip3 install feedparser
		sudo pip3 install beautifulsoup4
		
	
	Windows (within an admin command prompt): 
	
		pip3 install selenium
		pip3 install setuptools
		pip3 install feedparser
		pip3 install beautifulsoup4
		

# Instructions for running BingTool

1) Determine how many bing accounts you want to automate (1 or 2). Sign into the account(s), only use one Bing account per browser so if you have 2 accounts sign into one in firefox and another in chrome. As long as you dont clear your cookies in the browser you shouldn't need to repeat this step. BingTool does not require usernames or passwords, it relies on the browser having cookies which keep users logged in to their accounts.

2) Download the BingTool. If you dont know how to use git to clone the repo then just download this file https://github.com/jprince14/BingTool/archive/master.zip. If you used the setupBing.sh script BingTool is already download into ~/git/BingTool

3) Ensure that you are signed into your outlook/hotmail/live/bing account within each respective browser. This can be done either by opening the browser in the GUI and using the microsoftLogin.py script (This also requires setting the --cookies flag with running bingtool.py. 

4) Close all instances of the browser(s) that BingTool will be using

5) Review available command line arguments by running "python bingtool.py --help". For non-gui enviroments the headless mode will need to be selected

	```
	C:\Users\jprin\git\BingTool>bingtool.py --help
	usage: bingtool.py [-h] [-f] [-c] [-m MOBILE_SEARCHES] [-d DESKTOP_SEARCHES]
	                   [--cookies] [--headless]
	
	optional arguments:
	  -h, --help            show this help message and exit
	  -f, --firefox         include this option to use firefox (default: False)
	  -c, --chrome          include this option to use chrome (default: False)
	  -m MOBILE_SEARCHES, --mobile MOBILE_SEARCHES
	                        Number of Mobile Searches (default: 50)
	  -d DESKTOP_SEARCHES, --desktop DESKTOP_SEARCHES
	                        Number of Desktop Searches (default: 70)
	  --cookies             include this option to load cookies that were set
	                        using the microsoftLogin.py script.the script was not
	                        used or no cookies were saved this will work as is
	                        this flag was not set (default: False)
	  --headless            include this option to use headless mode (default:
	                        False)

	```

6) Run the tool by running "python bingtool.py OPTIONAL_ARGUMENTS"

7) Run BingTool once a day to get maximum rewards. After running BingTool for the first time start at step 3 for all subsequent runs.

8) The tool can be set up to run automatically by the windows scheduler or cron. It can also be run in headless mode on remote linux servers including Amazon Web Services.


# Tips

For Windows the pip commands need to be run in an admin command prompt

If the script stops working after a browser update run:

	Linux/mac:
	
		sudo pip install -U selenium
		
	Windows (within an admin command prompt)
	
		pip install -U selenium
