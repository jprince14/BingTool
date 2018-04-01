#!/bin/bash

#Since this will be run as root and not from the directory of the file we need to
#get the location of the bingtool script from the location of this script
BING_DIR=$(dirname "$(readlink -f "$0")")

#TODO Check if ARTIFACT_DIR is an enviromental variable and if so use it

if [ -z "$ARTIFACT_DIR"]; then
	croncmd="python3 $BING_DIR/bingtool.py -f -c --headless --cookies >/dev/null 2>&1"
else
	croncmd="python3 $BING_DIR/bingtool.py -f -c --headless --cookies -a $ARTIFACT_DIR >/dev/null 2>&1"
fi

#Remove the current entry from the root crontab
( sudo crontab -l | grep -v -F bingtool.py ) | sudo crontab -

minute1=$(shuf -i 0-59 -n 1)
minute2=$(shuf -i 0-59 -n 1)
hour1=$(shuf -i 0-11 -n 1)
hour2=$(shuf -i 12-23 -n 1)
fullcroncmd1="$minute1 $hour1 * * * $croncmd"
fullcroncmd1="$minute2 $hour2 * * * $croncmd"

#update the root crontab so the script is run twice a day
( sudo crontab -l | echo "$fullcroncmd1" ) | sudo crontab -
( sudo crontab -l | echo "$fullcroncmd2" ) | sudo crontab -


sudo /etc/init.d/cron reload

