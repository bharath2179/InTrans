#!/bin/bash
#Script to process RWIS data and copy to AWS S3
dt=$(date --date yesterday "+%b-%d-%Y")
dt1=$(date --date yesterday "+%m-%d-%Y")
m=$(date --date yesterday "+%-m")
d=$(date --date yesterday "+%-d")
source /home/ec2-user/anaconda3/etc/profile.d/conda.sh && \
conda activate base && \
cd /home/ec2-user/data/rwis/$dt && python3 /home/ec2-user/data/rwis_csv/rwis.py
aws s3 cp $dt.csv s3://intrans-feed/rwis_csv/year=2020/month=$m/day=$d/
