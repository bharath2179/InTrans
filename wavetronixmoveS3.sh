#!/bin/bash
#export PATH=/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/opt/aws/bin:/home/ec2-user/.local/bin:/home/ec2-user/bin
#Process Wavetronix raw data amd copy the processed copy data to AWS S3
export PATH=/home/ec2-user/anaconda3/bin:/home/ec2-user/anaconda3/condabin:/home/ec2-user/anaconda2/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/opt/aws/bin:/home/ec2-user/.local/bin:/home/ec2-user/bin
#get yesterday's date.The regex pattern "+%b-%d-%Y" is used to get date in the format eg: Apr-20-2020
dt=$(date --date yesterday "+%b-%d-%Y")
#The additional variable dt1 is toname the output file of the format 04-20-2020.csv
dt1=$(date --date yesterday "+%m-%d-%Y")

#Exract the month from the date
m=$(date --date yesterday "+%-m")

#Extract the day from the date

d=$(date --date yesterday "+%-d")

Y=$(date --date yesterday "+%-Y")
#Move into the wavetronix raw data folder
cd /home/ec2-user/wavetronix/$dt

#Run the python script to convert the raw xml files to csv
python3 /home/ec2-user/wavetronix_abc.py > wavetronixlog$dt1.txt

# Transfer the csv file to the HDFS
aws s3 cp $dt1.csv s3://testhazard-intrans/wavetronix/year=$Y/month=$m/day=$d/
