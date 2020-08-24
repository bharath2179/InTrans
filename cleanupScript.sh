#!/bin/sh
export PATH=/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/opt/aws/bin:/home/ec2-user/.local/bin:/home/ec2-user/bin
folder=/home/ec2-user/inrix/
find $folder -type d   -mtime +1 -exec rm -rf {} \;

folder=/home/ec2-user/wavetronix/
find $folder -type d -mtime +1 -exec rm -rf {} \;

folder=/home/ec2-user/tpims/
find $folder -type d -mtime +1 -exec rm -rf {} \;

folder=/home/ec2-user/rwis/
find $folder -type d -mtime +1 -exec rm -rf {} \;
