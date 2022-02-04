import os
import sys
import fileinput
import json
import csv
import datetime

yesterday=datetime.date.today()-datetime.timedelta(days=1)
path=yesterday.strftime("%b-%d-%Y")
#input_path='/home/ec2-user/data/rwis/'+path+'/*'
input_path='./'
data_files= [ fol for fol in os.listdir(input_path) if fol.endswith('json')]
i=0
tempFile = open( "temp.json", 'w' )
tempFile.write("{\"rwis\":[")
while i<len(data_files):
    for line in fileinput.input( input_path+'/'+data_files[i] ):
        if line.find("\n",0,200)==-1:
            line1=line.replace( "[]", "" )
            line1=line1.replace( "][", "," )
            line1=line1.replace( "[", "" )
            line1=line1.replace("]",",")
            line1=line1.replace(",,",",")
            tempFile.write(line1.replace("}{","},{"))
    i=i+1
tempFile.write("{}]}")
tempFile.close()

tempFile = open( "temp1.json", 'w' )
for line in fileinput.input('temp.json'):
    tempFile.write(line.replace("}{","},{"))
tempFile.close()

with open('temp1.json') as json_file:
    data = json.load(json_file)

rwis_data=data["rwis"]
data_file = open('temp.csv','w')
csv_writer = csv.writer(data_file)
count = 0
for emp in rwis_data:
    if count == 0:
        # Writing headers of CSV file
        header = emp.keys()
        csv_writer.writerow(header)
        count += 1
# Writing data of CSV file
    csv_writer.writerow(emp.values())
os.remove("temp.json")
os.remove("temp1.json")
data_file.close()
data_file=open(path+'.csv', 'w')
csv_writer = csv.writer(data_file)
with open('temp.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        try:
            if row[0].startswith('IA') or row[0].startswith('st'):
                csv_writer.writerow(row)
        except:
            pass
data_file.close()
os.remove("temp.csv")
