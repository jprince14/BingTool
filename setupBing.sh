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
eval $PKG_MGR -y install python-pip



echo "Updating pip for both python 2 and python 3"
sudo -H pip3 install --upgrade pip
sudo -H pip install --upgrade pip
echo "Installing python dependencies for Bing Tool"
sudo pip3 install -U setuptools
sudo pip install -U setuptools 
sudo pip3 install -U feedparser
sudo pip install -U feedparser
sudo pip3 install -U selenium
sudo pip install -U selenium
sudo pip3 install -U beautifulsoup4
sudo pip install -U beautifulsoup4

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

#Save ARTIFACT_DIR as an enviromental variable to the users .bashrc
if grep -q ARTIFACT_DIR ~/.bashrc; then
	grep -v -F ARTIFACT_DIR ~/.bashrc > ~/deleteme.tmp
    echo "export ARTIFACT_DIR=$LOCAL_ARTIFACT_DIR" >> ~/deleteme.tmp
    mv ~/deleteme.tmp ~/.bashrc
    chmod 644 ~/.bashrc
else
	echo "export ARTIFACT_DIR=$LOCAL_ARTIFACT_DIR" >> ~/.bashrc
fi
source ~/.bashrc

#Update the root .bashrc
if sudo grep -q ARTIFACT_DIR /root/.bashrc; then
	sudo sh -c 'grep -v -F ARTIFACT_DIR /root/.bashrc > /root/deleteme.tmp'
    sudo sh -c 'echo "export ARTIFACT_DIR='$LOCAL_ARTIFACT_DIR'" >> /root/deleteme.tmp'
    sudo sh -c 'mv /root/deleteme.tmp /root/.bashrc'
else
	sudo sh -c 'echo "export ARTIFACT_DIR='$LOCAL_ARTIFACT_DIR'" >> /root/.bashrc'
fi


#Add the script to the root chrontab
echo "Adding BingTool as a daily scheduled cron job"
croncmd="python3 $BING_DIR/bingtool.py -f -c --headless --cookies -a $LOCAL_ARTIFACT_DIR >/dev/null 2>&1"
minute1=$(shuf -i 0-59 -n 1)
minute2=$(shuf -i 0-59 -n 1)
hour1=$(shuf -i 0-11 -n 1)
hour2=$(shuf -i 12-23 -n 1)
fullcroncmd1="$minute1 $hour1 * * * $croncmd"
fullcroncmd2="$minute2 $hour2 * * * $croncmd"
#update the root crontab so the script is run twice a day
( sudo crontab -l | grep -v -F bingtool.py ; echo "$fullcroncmd1\n$fullcroncmd2" ) | sudo crontab -

update_time_cmd="sh $BING_DIR/update_bingrewards_run_time.sh >/dev/null 2>&1"
#Update the time to run the cron job at midnight and noon
full_update_time_cmd="0 0,12 * * * $update_time_cmd"
( sudo crontab -l | grep -v -F "$update_time_cmd" ; echo "$full_update_time_cmd" ) | sudo crontab -

sudo /etc/init.d/cron reload

echo "User needs to sign into Microsoft account in Chrome and/or Firefox to use with BingTool. Either sign in using the GUI or use the microsoftLogin.py script"

