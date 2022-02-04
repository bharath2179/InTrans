#!/bin/sh
#Copy RWIS raw data fro EC2 to S3
export PATH=/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/opt/aws/bin:/home/ec2-user/.local/bin:/home/ec2-user/bin
cd /home/ec2-user/data/rwis
folder=`ls -ltr | tail -2 | head -1 | awk '{print $9}'`
aws s3 cp --recursive ./$folder s3://intrans-feed/rwis/$folder
