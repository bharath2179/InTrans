#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Input files should be (*.mdb or *.accdb)
inputfile = "/lss/research/itrns-otohpc/CrashTools/SpeedRelatedCrashTool/working.mdb"
outputfile = "/lss/research/itrns-otohpc/CrashTools/SpeedRelatedCrashTool/Output.csv"
outputcl = "/lss/research/itrns-otohpc/CrashTools/SpeedRelatedCrashTool/CRASH_LEVEL.csv"
outputvl = "/lss/research/itrns-otohpc/CrashTools/SpeedRelatedCrashTool/VEHICLE_LEVEL.csv"
outputpl = "/lss/research/itrns-otohpc/CrashTools/SpeedRelatedCrashTool/PERSON_LEVEL.csv"


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


# In[ ]:
