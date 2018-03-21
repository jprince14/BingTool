#!/bin/bash

GIT_DIR=~/git/
BING_DIR=$GIT_DIR/BingTool


croncmd="python3 $BING_DIR/bingtool.py -f -c --headless --cookies >/dev/null 2>&1"

#Remove the current entry from the root crontab
( sudo crontab -l | grep -v -F "$croncmd" ) | sudo crontab -

minute=$(((1 + RANDOM % 60)-1))
hour=$(((1 + RANDOM % 24)-1))
fullcroncmd="$minute $hour * * * $croncmd"
#update the root crontab
( sudo crontab -l | grep -v -F "$croncmd" ; echo "$fullcroncmd" ) | sudo crontab -

sudo /etc/init.d/cron reload
