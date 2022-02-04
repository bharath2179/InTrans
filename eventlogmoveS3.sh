#!/bin/bash
#Eventlog copy to S3 script
export PATH=/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/opt/aws/bin:/home/ec2-user/.local/bin:/home/ec2-user/bin
aws s3 cp /home/ec2-user/EventLog.csv s3://intrans-feed/TCP_Work_Zone_Performance/
