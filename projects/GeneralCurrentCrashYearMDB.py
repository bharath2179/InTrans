#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Input files should be (*.mdb or *.accdb)
inputfile = "/lss/research/itrns-otohpc/CrashTools/GeneralCurrentCrashYear/working.mdb"
outputfile = "/lss/research/itrns-otohpc/CrashTools/GeneralCurrentCrashYear/Output.csv"
outputdir = "/lss/research/itrns-otohpc/CrashTools/GeneralCurrentCrashYear/"
outputcl = "/lss/research/itrns-otohpc/CrashTools/GeneralCurrentCrashYear/CRASH_LEVEL.csv"
outputvl = "/lss/research/itrns-otohpc/CrashTools/GeneralCurrentCrashYear/VEHICLE_LEVEL.csv"
outputpl = "/lss/research/itrns-otohpc/CrashTools/GeneralCurrentCrashYear/PERSON_LEVEL.csv"


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
import arcpy
from arcpy import env

try:
    # Set the local variables
    in_Table = outputcl
    x_coords = "Longitude"
    y_coords = "Latitude"
    out_Layer = "CRASH_LEVEL"
    out_dir = outputdir
    # Set the spatial reference
    spRef = r"Coordinate Systems\Geographic Coordinate Systems\World\WGS 1984.prj"

    # Make the XY event layer...
    arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, spRef)

    # Save to shapefile
    arcpy.FeatureClassToShapefile_conversion(out_Layer, out_dir)

except:
    # If an error occurred print the message to the screen
    print ("error")


# In[ ]:
