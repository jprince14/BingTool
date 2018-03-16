#!/bin/bash

SAVED_DIR=pwd

echo "Updating the system"
sudo apt-get update
sudo apt-get -y upgrade

echo "Installing firefox"
sudo apt-get install -y firefox

#install chrome
cd ~/Downloads
echo "Adding chrome repo to sources"
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add - 
sudo sh -c 'echo "deb https://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
sudo apt-get update
echo "Installing chrome"
sudo apt-get install -y google-chrome-stable

echo "Installing pip"
sudo apt-get install -y python-pip

echo "Updating pip"
sudo pip install --upgrade pip
echo "Installing python dependencies for Bing Tool"
sudo pip install feedparser
sudo pip install selenium
sudo pip install beautifulsoup4

echo "Installing the default Ubuntu Desktop Enviroment"
sudo apt-get install -y ubuntu-desktop

echo "installing git"
sudo apt-get install -y git

GIT_DIR=~/git/
if [ ! -d $GIT_DIR ]; then
  mkdir -p $GIT_DIR;
fi

cd $GIT_DIR
git clone https://github.com/jprince14/BingTool
echo "BingTool is located at $(pwd)/BingTool"

cd $SAVED_DIR

echo "TODO - set up running BingTool as a cron job"


echo "User needs to either enable xrdp or set up vnc then sign into Microsoft account on browsers to use with BingTool"
