#!/bin/sh
#make a directory in the tpims folder in the LSS with yesterday's date of format Apr-20-2020
mkdir ./tpims/$(date +"%b-%d-%Y")
#use curl commmand to download data from the externa; url specified after passing username.No password and hece left empty.The shell script invoked through NiFi
curl --user "1gCQn7YxaPdfEUXA3oo2: " -o ./tpims/$(date +"%b-%d-%Y")/tpims_`date +%Y-%m-%d-%H-%M-%S`.json http://onlineparkingnetwork.net/api/maasto/archive.json
