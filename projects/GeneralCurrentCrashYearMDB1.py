#!/usr/bin/env python
# coding: utf-8

# In[1]:


#subprocess.run('source activate environment-name && "enter command here" && source deactivate', shell=True)



# Input files should be (*.mdb or *.accdb)
inputfile = "/lss/research/itrns-otohpc/CrashTools/GeneralCurrentCrashYear/working.mdb"
outputfile = "/lss/research/itrns-otohpc/CrashTools/GeneralCurrentCrashYear/Output.csv"
outputdir = "/lss/research/itrns-otohpc/CrashTools/GeneralCurrentCrashYear/"
outputcl = "/lss/research/itrns-otohpc/CrashTools/GeneralCurrentCrashYear/CRASH_LEVEL.csv"
outputvl = "/lss/research/itrns-otohpc/CrashTools/GeneralCurrentCrashYear/VEHICLE_LEVEL.csv"
outputpl = "/lss/research/itrns-otohpc/CrashTools/GeneralCurrentCrashYear/PERSON_LEVEL.csv"

import os
os.system("source activate py27")


# In[2]:
import pandas_access as mdb

db_filename = inputfile

# Listing the tables.
for tbl in mdb.list_tables(db_filename):
  print(tbl)

# import all the necessary libraries
import csv
import pyodbc
import pandas as pd
import numpy as np



# In[3]:


# create a connection between the source DataBase and Python

#conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};" + r"Dbq="+inputfile+";")
#curs = conn.cursor()


# In[4]:


# Curser execution through the DataBase and reading data as a DataFrame
# Read the Crash Level table from the Data Source
#curs.execute('SELECT * FROM CRASH_LEVEL')

#col_headers = [ i[0] for i in curs.description ]
#rows = [ list(i) for i in curs.fetchall()]
#dfcl = pd.DataFrame(rows, columns=col_headers)

dfcl = mdb.read_table(db_filename, table_name="CRASH_LEVEL")
dfcl.to_csv(outputcl, index=False)


# In[5]:


# Read the Vehicle Level table from the Data Source
#curs.execute('SELECT * FROM VEHICLE_LEVEL')

#col_headers = [ i[0] for i in curs.description ]
#rows = [ list(i) for i in curs.fetchall()]
#dfvl = pd.DataFrame(rows, columns=col_headers)


dfvl = mdb.read_table(db_filename, table_name="VEHICLE_LEVEL")
dfvl.to_csv(outputvl, index=False)


# In[6]:


# Read the Person Level table from the Data Source
#curs.execute('SELECT * FROM PERSON_LEVEL')

#col_headers = [ i[0] for i in curs.description ]
#rows = [ list(i) for i in curs.fetchall()]
#dfpl = pd.DataFrame(rows, columns=col_headers)

dfpl = mdb.read_table(db_filename, table_name="PERSON_LEVEL")
dfpl.to_csv(outputpl, index=False)


# In[7]:


#Convert the Crash_Level CSV file to Shape file using ArcPy library
os.system("source activate test")

from geopandas import GeoDataFrame
from shapely.geometry import Point
import os
import fiona

#Ignoring files with endings different from .csv in your folder
input_file = outputcl
df = pd.read_csv(input_file)          #Reading your csv file with pandas

# 4 Create tuples of geometry by zipping Longitude and latitude columns in your csv file
geometry = [Point(xy) for xy in zip(df.Longitude, df.Latitude)]

# 5 Define coordinate reference system on which to project your resulting shapefile
crs = {'init': 'epsg:4326'}

# 6 Convert pandas object (containing your csv) to geodataframe object using geopandas
gdf = GeoDataFrame(df, crs = crs, geometry=geometry)

# 7 Save file to local destination
output_filename = os.path.join(outputdir, "CRASH_LEVEL_out_test.shp")
gdf.to_file(driver='ESRI Shapefile', filename=output_filename)
