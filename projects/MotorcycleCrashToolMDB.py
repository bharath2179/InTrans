#!/usr/bin/env python
# coding: utf-8

# In[6]:


# Input files should be (*.mdb or *.accdb)
inputfile = "/lss/research/itrns-otohpc/CrashTools/MotorcycleCrashTool/working.mdb"
outputfile = "/lss/research/itrns-otohpc/CrashTools/MotorcycleCrashTool/Output_test.csv"
outputdir = "/lss/research/itrns-otohpc/CrashTools/MotorcycleCrashTool/"
outputcl = "/lss/research/itrns-otohpc/CrashTools/MotorcycleCrashTool/CRASH_LEVEL_test.csv"
outputvl = "/lss/research/itrns-otohpc/CrashTools/MotorcycleCrashTool/VEHICLE_LEVEL_test.csv"
outputpl = "/lss/research/itrns-otohpc/CrashTools/MotorcycleCrashTool/PERSON_LEVEL_test.csv"


# In[7]:


# import all the necessary libraries
import csv
import pyodbc
import pandas as pd
import numpy as np


# In[8]:

import pandas_access as mdb

db_filename = inputfile

# Listing the tables.
for tbl in mdb.list_tables(db_filename):
  print(tbl)


# create a connection between the source DataBase and Python

#conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};" + r"Dbq="+inputfile+";")
#curs = conn.cursor()


# In[9]:


# Curser execution through the DataBase and reading data as a DataFrame
# Read the Crash Level table from the Data Source
#curs.execute('SELECT * FROM CRASH_LEVEL')

#col_headers = [ i[0] for i in curs.description ]
#rows = [ list(i) for i in curs.fetchall()]
#dfcl = pd.DataFrame(rows, columns=col_headers)
#dfcl.to_csv(outputcl, index=False)

dfcl = mdb.read_table(db_filename, table_name="CRASH_LEVEL")
dfcl.to_csv(outputcl, index=False)


# In[10]:


# Read the Vehicle Level table from the Data Source
#curs.execute('SELECT * FROM VEHICLE_LEVEL')

#col_headers = [ i[0] for i in curs.description ]
#rows = [ list(i) for i in curs.fetchall()]
#dfvl = pd.DataFrame(rows, columns=col_headers)
#dfvl.to_csv(outputvl, index=False)

dfvl = mdb.read_table(db_filename, table_name="VEHICLE_LEVEL")
dfvl.to_csv(outputvl, index=False)


# In[11]:


# Read the Person Level table from the Data Source
#curs.execute('SELECT * FROM PERSON_LEVEL')

#col_headers = [ i[0] for i in curs.description ]
#rows = [ list(i) for i in curs.fetchall()]
#dfpl = pd.DataFrame(rows, columns=col_headers)
#dfpl.to_csv(outputpl, index=False)

dfcl = mdb.read_table(db_filename, table_name="PERSON_LEVEL")
dfcl.to_csv(outputpl, index=False)


# In[12]:
from geopandas import GeoDataFrame
from shapely.geometry import Point
import os
import fiona

inputfile = "/lss/research/itrns-otohpc/CrashTools/MotorcycleCrashTool/working.mdb"
outputfile = "/lss/research/itrns-otohpc/CrashTools/MotorcycleCrashTool/Output_test.csv"
outputdir = "/lss/research/itrns-otohpc/CrashTools/MotorcycleCrashTool/"
outputcl = "/lss/research/itrns-otohpc/CrashTools/MotorcycleCrashTool/CRASH_LEVEL_test.csv"
outputvl = "/lss/research/itrns-otohpc/CrashTools/MotorcycleCrashTool/VEHICLE_LEVEL_test.csv"
outputpl = "/lss/research/itrns-otohpc/CrashTools/MotorcycleCrashTool/PERSON_LEVEL_test.csv"

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

#Convert the Crash_Level CSV file to Shape file using ArcPy library
#import arcpy
#from arcpy import env

#try:
    # Set the local variables
    #in_Table = outputcl
    #x_coords = "Longitude"
    #y_coords = "Latitude"
    #out_Layer = "MotorcycleCrash_AllConfig"
    #out_dir = outputdir
    # Set the spatial reference
    #spRef = r"Coordinate Systems\Geographic Coordinate Systems\World\WGS 1984.prj"

    # Make the XY event layer...
    #arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, spRef)

    # Save to shapefile
    #arcpy.FeatureClassToShapefile_conversion(out_Layer, out_dir)

#except:
    # If an error occurred print the message to the screen
    #print ("error")


# In[ ]:
