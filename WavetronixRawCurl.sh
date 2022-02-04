#!/bin/sh
#Download wavetronixRawData
export PATH=/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/opt/aws/bin:/home/ec2-user/.local/bin:/home/ec2-user/bin
curl -o /home/ec2-user/wavetronix/$(date +"%b-%d-%Y")/wavetronix_`date +%Y-%m-%d-%H-%M-%S`.xml --create-dirs https://iowa-atms.cloud-q-free.com/api/rest/dataprism/detector
