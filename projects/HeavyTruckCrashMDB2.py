#!/usr/bin/env python
# coding: utf-8

# In[50]:


# Input files should be (*.mdb or *.accdb)
inputfile = "/lss/research/itrns-otohpc/CrashTools/HeavyTruckCrash/working.mdb"
outputfile = "/lss/research/itrns-otohpc/CrashTools/HeavyTruckCrash/Output_test.csv"
outputcl = "/lss/research/itrns-otohpc/CrashTools/HeavyTruckCrash/CRASH_LEVEL_test.csv"
outputvl = "/lss/research/itrns-otohpc/CrashTools/HeavyTruckCrash/VEHICLE_LEVEL_test.csv"
outputpl = "/lss/research/itrns-otohpc/CrashTools/HeavyTruckCrash/PERSON_LEVEL_test.csv"


import pandas_access as mdb

db_filename = inputfile

# Listing the tables.
for tbl in mdb.list_tables(db_filename):
  print(tbl)

# Read a small table.
# df = mdb.read_table(db_filename, "MyTable")
# print(df)

# In[51]:


# import all the necessary libraries
import csv
import pyodbc
import pandas as pd
import numpy as np


# In[52]:


# create a connection between the source DataBase and Python

# conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};" + r"Dbq="+inputfile+";")
#conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};" + r"Dbq=C:\Users\davami\Box\CrashTools\HeavyTruckCrash\working.mdb;")
# curs = conn.cursor()


# In[53]:


# Curser execution through the DataBase and reading data as a DataFrame

# curs.execute('SELECT * FROM CRASH_LEVEL')

# col_headers = [ i[0] for i in curs.description ]
# rows = [ list(i) for i in curs.fetchall()]
# dfcl = pd.DataFrame(rows, columns=col_headers)
dfcl = mdb.read_table(db_filename, table_name="CRASH_LEVEL")
dfcl.to_csv(outputcl, index=False)

# In[54]:


dfCRASH_LEVEL = dfcl[['CASENUMBER','COUNTY','CRASH_DATE','CRASH_DAY','CRASH_KEY','CRASH_YEAR','CRASHMONTH','CRCOMANNER','CSEVERITY',
 'CSURFCOND','FATALITIES','FIRSTHARM','Latitude','LECASENUM','LIGHTING','Longitude','MAJINJURY','MAJORCAUSE','MININJURY','POSSINJURY',
 'PROPDMG','ROADCLASS','ROADTYPE','RURALURBAN','TIMEBIN1','UNKINJURY','WZ_RELATED',]]



#dfCRASH_LEVEL


# In[55]:


# curs.execute('SELECT * FROM VEHICLE_LEVEL')

# col_headers = [ i[0] for i in curs.description ]
# rows = [ list(i) for i in curs.fetchall()]

# dfvl = pd.DataFrame(rows, columns=col_headers)

dfvl = mdb.read_table(db_filename, table_name="VEHICLE_LEVEL")
dfvl.to_csv(outputvl, index=False)

#exit(0)
# In[56]:


dfvl2 = dfvl[['CRASH_KEY','VCONFIG']]
dfvl3 = dfvl2.loc[(dfvl2['VCONFIG'] >= 7) & (dfvl2['VCONFIG'] <= 16)]
dfOverall = dfvl3.rename(columns=({'CRASH_KEY':'OriginalCrashKey','VCONFIG':'OverallConfiguration'}))


#dfOverall


# In[57]:


dfJoin1 = pd.merge(dfCRASH_LEVEL, dfOverall, how='inner', left_on=['CRASH_KEY'], right_on=['OriginalCrashKey'])


#dfJoin1


# In[58]:


# curs.execute('SELECT * FROM PERSON_LEVEL')

# col_headers = [ i[0] for i in curs.description ]
# rows = [ list(i) for i in curs.fetchall()]
# dfpl = pd.DataFrame(rows, columns=col_headers)


dfpl = mdb.read_table(db_filename, table_name="PERSON_LEVEL")
dfpl.to_csv(outputpl, index=False)


# In[59]:


import pandas as pd
dfcsv = pd.read_csv(r'/lss/research/itrns-otohpc/CrashTools/GeneralFiles/MVE_ISP_Counties.csv')


# In[60]:


dfcsv2 = dfcsv.drop(columns=['County Name','Patrol Area'])	
dfMVE_ISP_Counties = dfcsv2.rename(columns=({'NUMBER':'County'}))


#dfMVE_ISP_Counties


# In[61]:


dfJoin4 = pd.merge(dfJoin1, dfMVE_ISP_Counties, how='inner', left_on=['COUNTY'], right_on=['County'])



#dfJoin4


# In[62]:


dfClean3 = dfJoin4.drop(columns=['County'])



#dfClean3


# In[63]:


dfvl12 = dfvl[['CRASH_KEY','DCONTCIRC1','UNITKEY','VACTION','VCONFIG',]]


# In[64]:


dfvl13 = dfvl12.rename(columns=({'VACTION':'VACTION-Car','VCONFIG':'VCONFIG-Car','UNITKEY':'UNITKEY-Car','DCONTCIRC1':'DCONTCIRC1-Car','CRASH_KEY':'CRASH_KEY-Car'}))


# In[65]:


dfCarVehicleLevel = dfvl13.loc[(dfvl13['VCONFIG-Car'] < 7) | (dfvl13['VCONFIG-Car'] > 16)]


#dfCarVehicleLevel


# In[66]:


dfvl22 = dfvl[['ALCRESULT','ALCTEST','AXLES','CARGOBODY','CHARGED','CMVGVWR','CRASH_KEY','DAGEBIN1','DCONTCIRC1','DEFECT','DRIVERCOND',
 'DRIVERDIST','DRUGRESULT','DRUGTEST','HAZMAT_PL','HAZMATINV','HAZMATPLC','HAZMATREL','HORIZALIGN','SPEEDLIMIT','UNITKEY','VACTION',
 'VCONFIG']]


# In[67]:


dfvl23 = dfvl22.rename(columns=({'DEFECT':'DEFECT-Truck','VACTION':'VACTION-Truck','CARGOBODY':'CARGOBODY-Truck','VCONFIG':'VCONFIG-Truck',
                           'SPEEDLIMIT':'SPEEDLIMIT-Truck','HORIZALIGN':'HORIZALIGN-Truck','DRIVERDIST':'DRIVERDIST-Truck','DCONTCIRC1':'DCONTCIRC1-Truck',
                              'DRIVERCOND':'DRIVERCOND-Truck','DRUGRESULT':'DRUGRESULT-Truck','DRUGTEST':'DRUGTEST-Truck','ALCTEST':'ALCTEST-Truck',
                                 'ALCRESULT':'ALCRESULT-Truck','DAGEBIN1':'DAGEBIN1-Truck','CHARGED':'CHARGED-Truck','UNITKEY':'UNITKEY-Truck',
                                'CRASH_KEY':'CRASH_KEY-Truck'}))


# In[68]:


dfTruckVehicleLevel = dfvl23.loc[(dfvl23['VCONFIG-Truck']>6)&(dfvl23['VCONFIG-Truck']<17)]


#dfTruckVehicleLevel


# In[69]:


dfJoin2 = pd.merge(dfCarVehicleLevel,dfTruckVehicleLevel,how='right',left_on=['CRASH_KEY-Car'],right_on=['CRASH_KEY-Truck'])


#dfJoin2


# In[70]:


dfClean2 = dfJoin2.drop(columns=['CRASH_KEY-Car'])


#dfClean2


# In[71]:


dfpl2 = dfpl[['OCCPROTECT','SEATING','UNITKEY']]


# In[72]:


dfPersonLevel = dfpl2.rename(columns=({'UNITKEY':'UNITKEY-Person'}))



#dfPersonLevel


# In[73]:


dfJoin3 = pd.merge(dfClean2,dfPersonLevel,how='left',left_on=['UNITKEY-Truck'],right_on=['UNITKEY-Person'])


#dfJoin3


# In[74]:


dfJoin5 = pd.merge(dfClean3,dfJoin3,how='left',left_on=['OriginalCrashKey'],right_on=['CRASH_KEY-Truck'])


#dfJoin5


# In[75]:


dfclean41=dfJoin5
cond1 = (dfclean41['VCONFIG-Truck']==7)|(dfclean41['VCONFIG-Truck']==8)|(dfclean41['VCONFIG-Truck']==9)|(dfclean41['VCONFIG-Truck']==10)|(dfclean41['VCONFIG-Truck']==11)|(dfclean41['VCONFIG-Truck']==12)|(dfclean41['VCONFIG-Truck']==13)|(dfclean41['VCONFIG-Truck']==14)|(dfclean41['VCONFIG-Truck']==15)|(dfclean41['VCONFIG-Truck']==16)
dfclean41['Truck']=np.select([cond1],[dfclean41['UNITKEY-Truck']],'')


# In[76]:


dfclean42=dfclean41
cond1 = (dfclean42['Truck']=='')
dfclean42['Other']=np.select([cond1],[dfclean42['UNITKEY-Car']],[''])


# In[77]:


dfclean43=dfclean42
cond1 = ((dfclean43['VCONFIG-Truck']==7)|(dfclean43['VCONFIG-Truck']==8)|(dfclean43['VCONFIG-Truck']==9)|(dfclean43['VCONFIG-Truck']==10)|(dfclean43['VCONFIG-Truck']==11)|(dfclean43['VCONFIG-Truck']==12)|(dfclean43['VCONFIG-Truck']==13)|(dfclean43['VCONFIG-Truck']==14)|(dfclean43['VCONFIG-Truck']==15)|(dfclean43['VCONFIG-Truck']==16))&(dfclean43['SEATING']==1)
dfclean43['DriverProtect']=np.select([cond1],[dfclean43['OCCPROTECT']],[''])


# In[78]:


dfclean44=dfclean43
cond1 = (dfclean44['DRIVERCOND-Truck']==6)
cond2 = (dfclean44['ALCTEST-Truck']==9)
cond3 = (dfclean44['ALCRESULT-Truck']>0)&(dfclean44['ALCRESULT-Truck']<9)
dfclean44['AlcoholRelated']=np.select([cond1,cond2,cond3],[1,1,1],[0])


# In[79]:


dfclean45=dfclean44
cond1 = (dfclean45['DRIVERCOND-Truck']==7)
cond2 = (dfclean45['DRUGTEST-Truck']==9)
cond3 = (dfclean45['DRUGRESULT-Truck']<=9)
dfclean45['DrugRelated']=np.select([cond1,cond2,cond3],[1,1,1],[0])


# In[80]:


dfclean46=dfclean45
cond1 = dfclean46['AlcoholRelated']+dfclean46['DrugRelated']==2
cond2 = dfclean46['AlcoholRelated']==1
cond3 = dfclean46['DrugRelated']==1
dfclean46['DrugAlcRelated']=np.select([cond1,cond2,cond3],['BOTH','Alcohol','Drugs'],'None')


# In[81]:


dfclean47=dfclean46
cond1 = (dfclean47['CRASH_YEAR']==2012)&(dfclean47['CRASHMONTH']>9)
cond2 = (dfclean47['CRASH_YEAR']==2013)&(dfclean47['CRASHMONTH']<10)
cond3 = (dfclean47['CRASH_YEAR']==2013)&(dfclean47['CRASHMONTH']>9)
cond4 = (dfclean47['CRASH_YEAR']==2014)&(dfclean47['CRASHMONTH']<10)
cond5 = (dfclean47['CRASH_YEAR']==2014)&(dfclean47['CRASHMONTH']>9)
cond6 = (dfclean47['CRASH_YEAR']==2015)&(dfclean47['CRASHMONTH']<10)
cond7 = (dfclean47['CRASH_YEAR']==2015)&(dfclean47['CRASHMONTH']>9)
cond8 = (dfclean47['CRASH_YEAR']==2016)&(dfclean47['CRASHMONTH']<10)
cond9 = (dfclean47['CRASH_YEAR']==2016)&(dfclean47['CRASHMONTH']>9)
cond10 = (dfclean47['CRASH_YEAR']==2017)&(dfclean47['CRASHMONTH']<10)
cond11 = (dfclean47['CRASH_YEAR']==2017)&(dfclean47['CRASHMONTH']>9)
cond12 = (dfclean47['CRASH_YEAR']==2018)&(dfclean47['CRASHMONTH']<10)
cond13 = (dfclean47['CRASH_YEAR']==2018)&(dfclean47['CRASHMONTH']>9)
cond14 = (dfclean47['CRASH_YEAR']==2019)&(dfclean47['CRASHMONTH']<10)
cond15 = (dfclean47['CRASH_YEAR']==2019)&(dfclean47['CRASHMONTH']>9)
cond16 = (dfclean47['CRASH_YEAR']==2020)&(dfclean47['CRASHMONTH']<10)
cond17 = (dfclean47['CRASH_YEAR']==2020)&(dfclean47['CRASHMONTH']>9)
cond18 = (dfclean47['CRASH_YEAR']==2021)&(dfclean47['CRASHMONTH']<10)
dfclean47['FiscalYear']=np.select([cond1,cond2,cond3,cond4,cond5,cond6,cond7,cond8,cond9,cond10,cond11,cond12,cond13,cond14,cond15,cond16,cond17,cond18],['FY2013','FY2013','FY2014','FY2014','FY2015','FY2015','FY2016','FY2016','FY2017','FY2017','FY2018','FY2018','FY2019','FY2019','FY2020','FY2020','FY20201','FY2021'],'ERROR')


# In[82]:


dfClean4=dfclean47



#dfClean4


# In[83]:


dfAggregate11=dfClean4.groupby('OriginalCrashKey')


# In[84]:


#dfAggregate111=dfAggregate11.agg({'Truck':'count','Other':'count'})
#dfAggregate111.rename(columns={'Truck':'TruckCount','Other':'OtherCount'},inplace=True)


# In[85]:


dfAggregate111=dfAggregate11.agg({'UNITKEY-Truck':pd.Series.nunique,'UNITKEY-Car':pd.Series.nunique})
dfAggregate111.rename(columns={'UNITKEY-Truck':'TruckCount','UNITKEY-Car':'OtherCount'},inplace=True)


# In[86]:


dfAggregate1=dfAggregate111



#dfAggregate1


# In[87]:


dfJoin6 = pd.merge(dfClean4,dfAggregate1,how='inner',left_on=['CRASH_KEY'],right_on=['OriginalCrashKey'])



#dfJoin6


# In[88]:


dfClean4.DriverProtect = pd.to_numeric(dfClean4.DriverProtect,errors='coerce')


# In[89]:


dfAggregate22=dfClean4.groupby('UNITKEY-Truck')
dfAggregate222=dfAggregate22.agg({'DriverProtect':'mean'})


# In[90]:


dfAggregate2=dfAggregate222



#dfAggregate2


# In[91]:


dfJoin7 = pd.merge(dfJoin6,dfAggregate2,how='inner',left_on=['UNITKEY-Truck'],right_on=['UNITKEY-Truck'])


#dfJoin7


# In[92]:


dfclean71=dfJoin7
cond1 = dfclean71['TruckCount']+dfclean71['OtherCount']==1
cond2 = dfclean71['OtherCount']>0
cond3 = dfclean71['TruckCount']>1
dfclean71['CrashType']=np.select([cond1,cond2,cond3],['SingleVehicle','HeavyTruck and Other Vehicle','Multi Heavy Truck(no other vehicle types)'],'')


# In[93]:


dfClean7=dfclean71


#dfClean7


# In[94]:


dfClean7.to_csv(outputfile, index=False)


# In[ ]:

