#!/bin/bash

SAVED_DIR=$(pwd)
USERNAME=$(whoami)

cd ~
HOMEDIR=$(pwd)

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
eval $PKG_MGR -y install vim

echo "Installing firefox"
eval $PKG_MGR -y install firefox

#install chrome
eval 'cd "$HOMEDIR"/Downloads'

if [ "$system" = ubuntu ]; then
	if ! [ -f /etc/apt/sources.list.d/google.list ]; then
		echo "Adding chrome repo to sources"
		wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add - 
		sudo sh -c 'echo "deb https://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
	fi
	eval $PKG_MGR update
	echo "Installing chrome"
	eval $PKG_MGR -y install google-chrome-stable
	
	echo "Installing a Desktop Enviroment"
	eval $PKG_MGR -y install ubuntu-desktop
fi

if [ "$system" = redhat ]; then
	wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
	eval $PKG_MGR -y install redhat-lsb libXScrnSaver
	echo "Installing chrome"
	eval $PKG_MGR localinstall google-chrome-stable_current_x86_64.rpm
	
	echo "Installing a Desktop Enviroment"
	eval $PKG_MGR -y groups install "GNOME Desktop" 
fi

echo "Installing pip"
eval $PKG_MGR -y install python3-pip

echo "Updating pip"
sudo -H pip3 install --upgrade pip
echo "Installing python dependencies for Bing Tool"
sudo pip3 install setuptools 
sudo pip3 install feedparser
sudo pip3 install selenium
sudo pip3 install beautifulsoup4

echo "installing git"
eval $PKG_MGR -y install git

cd $HOMEDIR

eval 'DOT_GIT_DIR="$HOMEDIR"/.git'
if [ ! -d $DOT_GIT_DIR ]; then
	sudo -u $USERNAME git init
fi

eval 'GIT_DIR="$HOMEDIR"/git'
if [ ! -d $GIT_DIR ]; then
  sudo -u $USERNAME mkdir -p $GIT_DIR;
fi

cd $GIT_DIR
eval 'BING_DIR="$GIT_DIR"/BingTool'

if [ ! -d $BING_DIR ]; then
  sudo -u $USERNAME git clone https://github.com/jprince14/BingTool
else
  cd $BING_DIR
  sudo -u $USERNAME git pull origin master
fi

echo "BingTool is located at $BING_DIR"

cd $SAVED_DIR

#Add the script to the root chrontab
echo "Adding BingTool as a daily scheduled cron job"
croncmd="python3 $BING_DIR/bingtool.py -f -c --headless --cookies >/dev/null 2>&1"
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

