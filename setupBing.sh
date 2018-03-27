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
#eval $PKG_MGR -y upgrade

echo "Installing vim"
eval $PKG_MGR -y install vim

echo "Installing firefox"
eval $PKG_MGR -y install firefox

#install chrome
cd $HOME/Downloads

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


DOT_GIT_DIR=$HOME/.git
if [ ! -d $DOT_GIT_DIR ]; then
	sudo -u $USERNAME git init
fi

GIT_DIR=$HOME/git
if [ ! -d $GIT_DIR ]; then
  sudo -u $USERNAME mkdir -p $GIT_DIR;
fi

cd $GIT_DIR
BING_DIR=$GIT_DIR/BingTool

if [ ! -d $BING_DIR ]; then
  sudo -u $USERNAME git clone https://github.com/jprince14/BingTool
else
  cd $BING_DIR
  sudo -u $USERNAME git pull origin master
fi

echo "BingTool is located at $BING_DIR"

cd $SAVED_DIR


#Use a LOCAL_ARTIFACT_DIR incase ARTIFACT_DIR is already in the bashrc
LOCAL_ARTIFACT_DIR=$HOME/Downloads

#Save ARTIFACT_DIR as an enviromental variable
if grep -q ARTIFACT_DIR ~/.bashrc; then
	grep -v -F ARTIFACT_DIR ~/.bashrc > ~/deleteme.tmp
    echo "export ARTIFACT_DIR=$LOCAL_ARTIFACT_DIR" >> ~/deleteme.tmp
    mv ~/deleteme.tmp ~/.bashrc
    chmod 644 ~/.bashrc
else
	echo "export ARTIFACT_DIR=$LOCAL_ARTIFACT_DIR" >> ~/.bashrc
fi
source ~/.bashrc


#Add the script to the root chrontab
echo "Adding BingTool as a daily scheduled cron job"
croncmd="python3 $BING_DIR/bingtool.py -f -c --headless --cookies -a $LOCAL_ARTIFACT_DIR >/dev/null 2>&1"
minute=$(shuf -i 0-59 -n 1)
hour=$(shuf -i 0-23 -n 1)
fullcroncmd="$minute $hour * * * $croncmd"
( sudo crontab -l | grep -v -F bingtool.py ; echo "$fullcroncmd" ) | sudo crontab -

update_time_cmd="sh $BING_DIR/update_bingrewards_run_time.sh >/dev/null 2>&1"
#Update the time to run the cron job at midnight and noon
full_update_time_cmd="0 0,12 * * * $update_time_cmd"
( sudo crontab -l | grep -v -F "$update_time_cmd" ; echo "$full_update_time_cmd" ) | sudo crontab -

sudo /etc/init.d/cron reload

echo "User needs to sign into Microsoft account in Chrome and/or Firefox to use with BingTool. Either sign in using the GUI or use the microsoftLogin.py script"

