#!/bin/bash
#get yesterday's date.The regex pattern "+%b-%d-%Y" is used to get date in the format eg: Apr-20-2020
#export PATH=/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/opt/aws/bin:/home/ec2-user/.local/bin:/home/ec2-user/bin
export PATH=/home/ec2-user/anaconda3/bin:/home/ec2-user/anaconda3/condabin:/home/ec2-user/anaconda2/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/opt/aws/bin:/home/ec2-user/.local/bin:/home/ec2-user/bin
dt=$(date --date yesterday "+%b-%d-%Y")
#The additional variable dt1 is toname the output file of the format 04-20-2020.csv
dt1=$(date --date yesterday "+%m-%d-%Y")

#Exract the month from the date
m=$(date --date yesterday "+%-m")

#Extract the day from the date

d=$(date --date yesterday "+%-d")

Y=$(date --date yesterday "+%-Y")
#Move into the wavetronix raw data folder
cd /home/ec2-user/inrix/$dt



#Run the python script to convert the raw xml files to csv
python3 /home/ec2-user/inrix_xmltocsv.py > inrixlog$dt1.txt

#Rename the file to have the date in its name
mv unprocessed.csv $dt1.csv
# Transfer the csv file to the HDFS
aws s3 cp $dt1.csv s3://testhazard-intrans/inrix/year=$Y/month=$m/day=$d/
