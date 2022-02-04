#!/bin/sh
#Script ivokes AWS lambda function my-sourcecode-function1 to download and save the inrox data in AWS S3
#@author Bharath Chandra Anumukonda
export PATH=/home/ec2-user/anaconda3/bin:/home/ec2-user/anaconda3/condabin:/home/ec2-user/anaconda2/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/opt/aws/bin:/home/ec2-user/.local/bin:/home/ec2-user/bin
aws lambda invoke --function-name my-sourcecode-function1 --payload '{"key1": "value1", "key2": "value2", "key3": "value3"}' output.txt --profile testadmin
