#!/bin/bash

#Since this will be run as root and not from the directory of the file we need to
#get the location of the bingtool script from the location of this script
BINGDIR=$(dirname "$(readlink -f "$0")")
echo $BINGDIR

croncmd="python3 $BINGDIR/bingtool.py -f -c --headless --cookies >/dev/null 2>&1"

#Remove the current entry from the root crontab
( sudo crontab -l | grep -v -F "$croncmd" ) | sudo crontab -

minute=$(shuf -i 0-59 -n 1)
hour=$(shuf -i 0-23 -n 1)
fullcroncmd="$minute $hour * * * $croncmd"
#update the root crontab
( sudo crontab -l | grep -v -F "$croncmd" ; echo "$fullcroncmd" ) | sudo crontab -

sudo /etc/init.d/cron reload
