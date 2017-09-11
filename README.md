# BingTool

About BingTool

BingTool supports automating bing rewards for two accounts at a time, the tools works by using the selenium browser automation platform. BingTool does not require any credentials, as long as you are logged into the browser that selenium launches then the searches will count towards bing rewards. BingTool emulates a mobile browser so users will get points for both desktop and mobile searches. Only firefox and chrome are supported.

BingTool automates the downloading of selenium webdrivers, they are stored in the Downloads directory and deleted after the script completes.

Known Issues

1) Sometimes when firefox or chrome updates it takes selenium or webdrivers to start supporting the latest version. If the script starts crashing on one browser try running the following command:

	Linux/mac : sudo pip install -U selenium
	Windows : python -m pip install -U selenium

Instructions to set up BingTool

1) Download Python https://www.python.org/downloads/

2) Download and Update pip. Pip already ships with Python so just run the command below

	Linux/mac - "pip install -U pip"
	Windows - "python -m pip install -U pip"
	
3) Install the prerequisite packages. Run the following commands:
	Linux/mac:
		sudo pip install selenium
		sudo pip install feedparser
		sudo pip install beautifulsoup4
	Windows 
		python -m pip install selenium
		python -m pip install feedparser
		python -m pip install beautifulsoup4


Instructions for running BingTool

1) Determine how many bing accounts you want to automate (1 or 2). Sign into the account(s), only use one bin account per browser so if you have 2 accounts sign into one in firefox and another in chrome. As long as you dont clear your cookies in the browser you shouldn't need to repeat this step.

2) Download the BingTool. If you dont know how to use git to clone the repo then just download this file https://github.com/jprince14/BingTool/archive/master.zip

2) Update the main.py file to reflect what browser(s) you are using. set the useFirefox and useChrome variable to the appropriate boolean values (True or False).

3) Close all instances of the browser(s) that BingTool will be using

4) Run the tool by running "python main.py"

5) Run BingTool once a day to get maximum rewards. After running BingTool for the first time start at step 3 for all subsequent runs.

Tips

For Windows the pip commands need to be run in an admin command prompt
