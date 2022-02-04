#!/bin/sh
#invoke lambda with python file
export PATH=/home/ec2-user/anaconda3/bin:/home/ec2-user/anaconda3/condabin:/home/ec2-user/anaconda2/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/opt/aws/bin:/home/ec2-user/.local/bin:/home/ec2-user/bin
cd /home/ec2-user/my-inrix-function
python lambda_function.py
