#!/usr/bin/env python
# coding: utf-8
# In[1]:

# Input files should be (*.mdb or *.accdb)
inputfile = "/lss/research/itrns-otohpc/CrashTools/NonMotoristCrashTool/working.mdb"
outputfile = "/lss/research/itrns-otohpc/CrashTools/NonMotoristCrashTool/Output.csv"
outputdir = "/lss/research/itrns-otohpc/CrashTools/NonMotoristCrashTool/"
outputcl = "/lss/research/itrns-otohpc/CrashTools/NonMotoristCrashTool/CRASH_LEVEL.csv"
outputvl = "/lss/research/itrns-otohpc/CrashTools/NonMotoristCrashTool/VEHICLE_LEVEL.csv"
outputpl = "/lss/research/itrns-otohpc/CrashTools/NonMotoristCrashTool/PERSON_LEVEL.csv"

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


# In[4]:
dfcl = mdb.read_table(db_filename, table_name="CRASH_LEVEL")
dfcl.to_csv(outputcl, index=False)

# In[5]:
dfvl = mdb.read_table(db_filename, table_name="VEHICLE_LEVEL")
dfvl.to_csv(outputcl, index=False)

# In[6]:
dfpl = mdb.read_table(db_filename, table_name="PERSON_LEVEL")
dfpl.to_csv(outputpl, index=False)


# In[7]:
import csv
import pyodbc
import pandas as pd
import numpy as np

#Convert the Crash_Level CSV file to Shape file using ArcPy library
#test
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
