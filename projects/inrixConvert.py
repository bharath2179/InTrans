#import rquired packages
import xml.etree.ElementTree as ET
import os
#read all the files in the current folder
data_files = [f for f in os.listdir('./') if '.xml' in f]
#data_files creates a list of file names
output_csv_file ='unprocessed.csv'
lines_to_print = []
name_space_tag = ""
#create an empty list result
result=[]
#specify headers of the data
headers=["Code","c-value","SegmentClosed","Score","Speed","Average","Reference","TraveltimeinMinutes","Time"]
result.append(",".join(headers))
i=0
#put a while loop to run as many times as the number of files
while i<len(data_files):
    res=[]
    tree = ET.parse(data_files[i])
    i=i+1
        #get the root tag
    root = tree.getroot()
    root_tags = root.tag.split('}')
        #parse through each tag and extract the data
    for child in root:
        for a in child:
            time=a.attrib['timestamp']
            for b in a:
                #code=b.find(name_space_tag + 'code')
                x=b.attrib
                code=(x['code'])
                if 'c-value' in x:
                    cvalue=x['c-value']
                else:
                    cvalue=""
                if 'segmentClosed' in x:
                    segmentclosed=x['segmentClosed']
                else:
                    segmentclosed=""
                if 'score' in x:
                    score=x['score']
                else:
                    score=""
                if 'speed' in x:
                    speed=x['speed']
                else:
                    speed=""
                if 'average' in x:
                    average=x['average']
                else:
                    average=""
                if 'reference' in x:
                    reference=x['reference']
                else:
                    reference=""
                if 'travelTimeMinutes' in x:
                    traveltime=x['travelTimeMinutes']
                else:
                    traveltime=""
                lines=[code,cvalue,segmentclosed,score,speed,average,reference,traveltime,	]
                result.append(",".join(lines))
#write or append the data to output file which is in csv format
with open(output_csv_file, 'w') as filehandle:
    for detectorData in result:
        filehandle.write('%s\n' % detectorData)
