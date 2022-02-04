#!/bin/bash
#RWIS raw data download
rm /home/ec2-user/scripts/exec.sh
#echo "Hello"
cd /home/ec2-user/data/rwis
#cat files.log
fc=`ls -ld $(date +"%b-%d-%Y") |wc -l`
#echo $fc
if [ $fc == '0' ]
then
        mkdir $(date +"%b-%d-%Y")
fi

for i in {0..72..1}
do
        if [ $i -lt 10 ]
        then
        station=IA00$i
        else
        station=IA0$i
        fi
        #echo $station
        command="curl \"https://api.dtn.com/weather/stations/$station/traffic-observations?units=us&p0ecision=0&apikey=xugHpAdVsPSpOqqvbbfzspu6x0MAaVRw\" -H \"accept: application/json\" -H \"apikey: xugHpAdVsPSpOqqvbbfzspu6x0MAaVRw\" >> /home/ec2-user/data/rwis/$(date +"%b-%d-%Y")/common_`date +%Y-%m-%d-%H-%M`.json"
        echo $command >> /home/ec2-user/scripts/exec.sh
done

sh  /home/ec2-user/scripts/exec.sh
