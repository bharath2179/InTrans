#!/bin/bash
#export PATH=/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/opt/aws/bin:/home/ec2-user/.local/bin:/home/ec2-user/bin
export PATH=/home/ec2-user/anaconda3/bin:/home/ec2-user/anaconda3/condabin:/home/ec2-user/anaconda2/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/opt/aws/bin:/home/ec2-user/.local/bin:/home/ec2-user/bin
rm -rf /home/ec2-user/logs/monitoring_file.html
echo "<!DOCTYPE html>" >> /home/ec2-user/logs/monitoring_file.html
echo "<H3> Files count on Directory </H2>"  >> /home/ec2-user/logs/monitoring_file.html
echo "<table  width=70%> <tr style="text-align:left" bgcolor='#ADD8E6'><th>Date</th><th>Directory</th><th>Actual count</th><th>Expected count</th></tr>"  >> /home/ec2-user/logs/monitoring_file.html
monitoring_missing_list()
{
        day=`date | awk '{print $3}'`

        if [ $day == '1' ]
        then
                day=`date -d "-$(date +%d) days" | awk '{ print $3}'`
                month=$( date +%m )
                                month=`echo $month | sed 's/^0*//'`
                                if [ $month == '1' ]
                                then
                                        month="12"
                                        year=`date | awk '{print $6}'`
                                        year=$(( $year - 1 ))
                fi
        else
                day=`date | awk '{print $3}'`
                day=$(( $day - 1 ))
                month=$( date +%m )
                                month=`echo $month | sed 's/^0*//'`
                year=`date | awk '{print $6}'`
        fi

        y="year="
        m="month="
        d="day="
        c="-"
        date_name=$year$c$month$c$day

        files_count=`s3cmd ls -l --recursive $bucket_name/$y$year/$m$month/$d$day | wc -l`

        if [ ${files_count} ==  ${expected_files_count} ]
                then
            echo "<tr><td>${date_name}</td><td>${print_name}</td><td>${files_count}</td><td>${expected_files_count}</td></tr>" >> /home/ec2-user/logs/monitoring_file.html
        else
            echo "<tr bgcolor='red'><td>${date_name}</td><td>${print_name}</td><td>${files_count}</td><td>${expected_files_count}</td></tr>" >> /home/ec2-user/logs/monitoring_file.html
        fi
}




######################################
monitoring_missing_list1()
{
    day=`date | awk '{print $3}'`


        if [ $day == '1' ]
        then
        day=`date -d "-$(date +%d) days" | awk '{ print $3}'`
        month=`date -d "-$(date +%d) days" | awk '{ print $2}'`
                if [ $month == 'Jan' ]
                then
                        month=Dec
                        year=`date | awk '{print $6}'`
                        year=$(( $year - 1 ))
                fi
        else
        day=`date | awk '{print $3}'`
        day=$(( $day - 1 ))
        month=`date | awk '{print $2}'`
        year=`date | awk '{print $6}'`
        fi


        if [ $day -lt 10 ]
        then
        date_name=$month-0$day-$year
        else
        date_name=$month-$day-$year
        fi

        files_count=`s3cmd ls -l --recursive $bucket_name/$date_name | wc -l`

        if [ ${files_count} ==  ${expected_files_count} ]
        then
        echo "<tr><td>${date_name}</td><td>${print_name}</td><td>${files_count}</td><td>${expected_files_count}</td></tr>" >> /home/ec2-user/logs/monitoring_file.html
        else
        echo "<tr bgcolor='red'><td>${date_name}</td><td>${print_name}</td><td>${files_count}</td><td>${expected_files_count}</td></tr>" >> /home/ec2-user/logs/monitoring_file.html
        fi
}

###################################


monitoring_missing_list2()
{
    day=`date | awk '{print $3}'`


        if [ $day == '1' ]
        then
        day=`date -d "-$(date +%d) days" | awk '{ print $3}'`
        month=`date -d "-$(date +%d) days" | awk '{ print $2}'`
                if [ $month == 'Jan' ]
                then
                        month=Dec
                        year=`date | awk '{print $6}'`
                        year=$(( $year - 1 ))
                fi
        else
        day=`date | awk '{print $3}'`
        day=$(( $day - 1 ))
        month=`date | awk '{print $2}'`
        year=`date | awk '{print $6}'`
        fi


        if [ $day -lt 10 ]
        then
        date_name=$month-0$day-$year
        else
        date_name=$month-$day-$year
        fi

        files_count=`ls -ltr $folder_name/$date_name | wc -l`

        if [ ${files_count} ==  ${expected_files_count} ]
        then
        echo "<tr><td>${date_name}</td><td>${print_name}</td><td>${files_count}</td><td>${expected_files_count}</td></tr>" >> /home/ec2-user/logs/monitoring_file.html
        else
        echo "<tr bgcolor='red'><td>${date_name}</td><td>${print_name}</td><td>${files_count}</td><td>${expected_files_count}</td></tr>" >> /home/ec2-user/logs/monitoring_file.html
        fi
}

#######################################



bucket_name=s3://intrans-feed/wavetronix
expected_files_count=1
print_name=wavetronix

##Calling function for 1st Directory
monitoring_missing_list > /home/ec2-user/logs/monitoring.log


bucket_name=s3://intrans-feed/inrix
expected_files_count=1
print_name=inrix

##Calling function for 2nd Directory
monitoring_missing_list > /home/ec2-user/logs/monitoring.log


bucket_name=s3://intrans-feed/rwis
expected_files_count=288
print_name=rwis

##Calling function for 3rd Directory
monitoring_missing_list1 > /home/ec2-user/logs/monitoring.log


bucket_name=s3://intrans-feed/tpims
expected_files_count=1440
print_name=tpims

##Calling function for 4th Directory
monitoring_missing_list1 > /home/ec2-user/logs/monitoring.log

##5th function
files_count=`s3cmd ls -l --recursive s3://intrans-feed/TCP_Work_Zone_Performance/EventLog.csv | wc -l`

        if [ ${files_count} ==  '1' ]
        then
        echo "<tr><td>${date_name}</td><td>TCP_Work_Zone_Performance</td><td>${files_count}</td><td>1</td></tr>" >> /home/ec2-user/logs/monitoring_file.html
        else
        echo "<tr bgcolor='red'><td>${date_name}</td><td>TCP_Work_Zone_Performance</td><td>${files_count}</td><td>1</td></tr>" >> /home/ec2-user/logs/monitoring_file.html
        fi


##
folder_name=/home/ec2-user/wavetronix
expected_files_count=4320
print_name=wavetronix_raw

##Calling function for 6th Directory
monitoring_missing_list2 > /home/ec2-user/logs/monitoring.log



folder_name=/home/ec2-user/inrix
expected_files_count=1441
print_name=inrix_raw

##Calling function for 7th Directory
monitoring_missing_list2 > /home/ec2-user/logs/monitoring.log


folder_name=/home/ec2-user/tpims
expected_files_count=1441
print_name=tpims_raw

##Calling function for 8th Directory
monitoring_missing_list2 > /home/ec2-user/logs/monitoring.log


folder_name=/home/ec2-user/data/rwis
expected_files_count=289
print_name=rwis_raw

##Calling function for 9th Directory
monitoring_missing_list2 > /home/ec2-user/logs/monitoring.log



##HTML end
echo "</table>" >> /home/ec2-user/logs/monitoring_file.html
echo "</html>" >>         /home/ec2-user/logs/monitoring_file.html
echo "-- function complete --" >> /home/ec2-user/logs/monitoring.log




aws s3 cp /home/ec2-user/logs/monitoring_file.html s3://intrans-mon/
