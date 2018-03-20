#!/bin/bash

SAVED_DIR=$(pwd)

if [ -f /etc/redhat-release ]; then
	PKG_MGR="sudo yum"
	system=redhat
fi

if [ -f /etc/lsb-release ]; then
	PKG_MGR="sudo apt-get"
	system=ubuntu
fi

echo "Updating the system"
eval $PKG_MGR update
eval $PKG_MGR -y upgrade

echo "Installing vim"
eval $PKG_MGR install -y vim

echo "Installing firefox"
eval $PKG_MGR install -y firefox

#install chrome
cd ~/Downloads

if [ "$system" = ubuntu ]; then
	if ! [ -f /etc/apt/sources.list.d/google.list ]; then
		echo "Adding chrome repo to sources"
		wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add - 
		sudo sh -c 'echo "deb https://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
	fi
	eval $PKG_MGR update
	echo "Installing chrome"
	eval $PKG_MGR install -y google-chrome-stable
	
	echo "Installing a Desktop Enviroment"
	eval $PKG_MGR install -y ubuntu-desktop
fi

if [ "$system" = redhat ]; then
	wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
	eval $PKG_MGR install -y redhat-lsb libXScrnSaver
	echo "Installing chrome"
	eval $PKG_MGR localinstall google-chrome-stable_current_x86_64.rpm
	
	echo "Installing a Desktop Enviroment"
	eval $PKG_MGR -y groups install "GNOME Desktop" 
fi

echo "Installing pip"
eval $PKG_MGR install -y python3-pip

echo "Updating pip"
sudo -H pip3 install --upgrade pip
echo "Installing python dependencies for Bing Tool"
sudo pip3 install setuptools 
sudo pip3 install feedparser
sudo pip3 install selenium
sudo pip3 install beautifulsoup4

echo "installing git"
eval $PKG_MGR install -y git

GIT_DIR=~/git/
if [ ! -d $GIT_DIR ]; then
  mkdir -p $GIT_DIR;
fi

cd $GIT_DIR
if [ ! -d $GIT_DIR ]; then
  git clone https://github.com/jprince14/BingTool
else
  git pull origin master
fi


BING_DIR=$(pwd)/BingTool
echo "BingTool is located at $(pwd)/BingTool"

#Update the permissions of the git directory
chmod -R 777 $BING_DIR

cd $SAVED_DIR

#Add the script to the root chrontab
echo "Adding BingTool as a daily scheduled cron job"
croncmd="python3 $BING_DIR/main.py -f -c --headless >/dev/null 2>&1"
minute=$(((1 + RANDOM % 60)-1))
hour=$(((1 + RANDOM % 24)-1))
fullcroncmd="$minute $hour * * * $croncmd"
( sudo crontab -l | grep -v -F "$croncmd" ; echo "$fullcroncmd" ) | sudo crontab -

update_time_cmd="$BING_DIR/update_bingrewards_run_time.sh >/dev/null 2>&1"
#Update the time at midnight every day
full_update_time_cmd="* 0 * * * $update_time_cmd"
( sudo crontab -l | grep -v -F "$update_time_cmd" ; echo "$full_update_time_cmd" ) | sudo crontab -

sudo /etc/init.d/cron reload

echo "User needs to either enable xrdp or set up vnc then sign into Microsoft account on browsers to use with BingTool"

