#!/bin/sh
#Copy TPIMS raw data from EC2 to S3
export PATH=/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/opt/aws/bin:/home/ec2-user/.local/bin:/home/ec2-user/bin
cd /home/ec2-user/tpims
folder=`ls -ltr | tail -2 | head -1 | awk '{print $9}'`
aws s3 cp --recursive ./$folder s3://intrans-feed/tpims/$folder
