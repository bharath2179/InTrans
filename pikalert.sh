#!/bin/sh
#Script for pikalert download raw data with CURL
export PATH=/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/opt/aws/bin:/home/ec2-user/.local/bin:/home/ec2-user/bin
curl -o /home/ec2-user/pikalert/$(date +"%b-%d-%Y")/pikalert_`date +%Y-%m-%d-%H-%M-%S`.json --create-dirs http://emdss.pikalert.org/district_alerts/?path=/district_alerts\&state=iowa
