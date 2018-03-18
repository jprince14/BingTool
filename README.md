# BingTool

About BingTool

BingTool supports automating bing rewards for two accounts at a time, the tools works by using the selenium browser automation platform. BingTool does not require any credentials, as long as you are logged into the browser that selenium launches then the searches will count towards bing rewards. BingTool emulates a mobile browser so users will get points for both desktop and mobile searches. Only firefox and chrome are supported, BingTool will run on Windows, macOS or Linux. BingTool can be run in the cloud and in non-gui enviroments using headless mode.

BingTool automates the downloading of selenium webdrivers, they are stored in the Downloads directory and deleted after the script completes.

Known Issues

1) Sometimes when firefox or chrome updates it takes selenium or webdrivers to start supporting the latest version. If the script starts crashing on one browser try running the following command:

	Linux/mac : sudo pip install -U selenium
	
	Windows : python -m pip install -U selenium

Instructions to set up BingTool

1) Download Python https://www.python.org/downloads/

2) Download and Update pip. If pip is not installed on your system follow the instuctions at https://pip.pypa.io/en/stable/installing/	
	
3) Install the prerequisite packages. Run the following commands:

	Linux/mac:
	
		sudo pip install selenium
		
		sudo pip install feedparser
		
		sudo pip install beautifulsoup4
		
	
	Windows (within an admin command prompt): 
	
		pip install selenium
		
		pip install feedparser
		
		pip install beautifulsoup4
		

Instructions for running BingTool

1) Determine how many bing accounts you want to automate (1 or 2). Sign into the account(s), only use one Bing account per browser so if you have 2 accounts sign into one in firefox and another in chrome. As long as you dont clear your cookies in the browser you shouldn't need to repeat this step. BingTool does not require 

2) Download the BingTool. If you dont know how to use git to clone the repo then just download this file https://github.com/jprince14/BingTool/archive/master.zip

3) Ensure that you are signed into your outlook/hotmail/live/bing account within each respective browser

4) Close all instances of the browser(s) that BingTool will be using

5) Review available command line arguments by running "python main.py --help". For non-gui enviroments the headless mode will need to be selected

6) Run the tool by running "python main.py OPTIONAL_ARGUMENTS"

7) Run BingTool once a day to get maximum rewards. After running BingTool for the first time start at step 3 for all subsequent runs.

8) The tool can be set up to run automatically by the windows scheduler or cron. It can also be run in headless mode on a VPS such as AWS.


Instructions for semi-automated setup up of BingTool on on Ubuntu Linux

Run the following command
	bash <(wget -qO- https://raw.githubusercontent.com/jprince14/BingTool/master/setupBing.sh)

After executing the setupBing.sh script you need to log into the Ubuntu machine and sign into you Microsoft accouts for Firefox and/or Chrome.


Tips

For Windows the pip commands need to be run in an admin command prompt

If the script stops working after a browser update run:

	Linux/mac:
	
		sudo pip install -U selenium
		
	Windows (within an admin command prompt)
	
		pip install -U selenium
