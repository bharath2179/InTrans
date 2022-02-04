import os
import os.path
import re
from re import template
import sys, glob
import arcpy, csv

# Current Version
VERSION = '0.39'

# If the dataset is large, we'll need to use the hard disk instead of in-memory to prevent crashing.
large_dataset = False

# Constants
DATASET = ('zlos', 'zcta', 'zctb', 'zcvo', 'zdrv', 'zenv', 'zinj', 'zloc', 'zltp', 'znmt', 'zrda',
           'zrdb', 'zsev', 'zshp', 'zuni', 'zvdm', 'zveh', 'zwkz', 'zcit')
IOWA_COUNTY = ('adair', 'adams', 'allamakee', 'appanoose', 'audubon', 'benton', 'black hawk', 'boone',
               'bremer', 'buchanan', 'buena_vista', 'butler', 'calhoun', 'carroll', 'cass', 'cedar',
               'cerro_gordo', 'cherokee', 'chickasaw', 'clarke', 'clay', 'clayton', 'clinton', 'crawford',
               'dallas', 'davis', 'decatur', 'delaware', 'des moines', 'dickinson', 'dubuque', 'emmet',
               'fayette', 'floyd', 'franklin', 'fremont', 'greene', 'grundy', 'guthrie', 'hamilton',
               'hancock', 'hardin', 'harrison', 'henry', 'howard', 'humboldt', 'ida', 'iowa', 'jackson',
               'jasper', 'jefferson', 'johnson', 'jones', 'keokuk', 'kossuth', 'lee', 'linn', 'louisa',
               'lucas', 'lyon', 'madison', 'mahaska', 'marion', 'marshall', 'mills', 'mitchell', 'monona',
               'monroe', 'montgomery', 'muscatine', "o'brien", 'osceola', 'page', 'palo alto', 'plymouth',
               'pocahontas', 'polk', 'pottawattamie', 'poweshiek', 'ringgold', 'sac', 'scott', 'shelby',
               'sioux', 'story', 'tama', 'taylor', 'union', 'van buren', 'wapello', 'warren', 'washington',
               'wayne', 'webster', 'winnebago', 'winneshiek', 'woodbury', 'worth', 'wright')
VALID_YEAR = ('2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018','2019')

# Define data levels
CRASH_LEVEL = ('zcta', 'zenv', 'zloc', 'zltp', 'zrda', 'zsev', 'zwkz')
VEHICLE_LEVEL = ('zcvo', 'zctb', 'zdrv', 'zrdb', 'zvdm', 'zveh', 'zcit')
PERSON_LEVEL = ('zinj', 'znmt', 'zuni')
OTHER = {'zinj': 'INJURED', 'zlos': 'LOCATION_TOOL_2', 'znmt': 'NON_MOTORIST', 'zuni': 'UNINJURED'}

# Define aliases to use for fields in corresponding tables

zcvo_ALIASES = {'Crash_Key':'Crash Key - SAVER Internal Unique Identifier','UnitNum':'Commercial Vehicle Unit Number','UnitKey':'Combined Crash_Key and CUnitNum','Axles':'Number of Axles',
'CMVGVWR':'Gross Vehicle Weight Rating','HazMatRel':'Hazardous Materials Released?','HazMatInv':'Hazardous Materials Involvement','HazMatPlc':'Hazardous Materials Placard',
'HazMat_PL':'HazMat Placard Number','CVLPState1':'License Plate State (power unit attached)','CVLPYear1':'License Plate Year (power unit attached)',
'CVLPState2':'License Plate State (trailer 1 attached)','CVLPYear2':'License Plate Year (trailer 1 attached)','CVLPState3':'License Plate State (trailer 2 attached)',
'CVLPYear3':'License Plate Year (trailer 2 attached)','CMVCvDlly':'Converter Dolly Used?','CMVDlyPlSt':'Converter Dolly License Plate State','CMVDlyPlYr':'Converter Dolly License Plate Year',
'UnderOver':'Underride/Override'
}

zshp_ALIASES = {'Crash_Key':'Crash Key - SAVER Internal Unique Identifier','CaseNumber':'Case Number - Iowa DOT','LECaseNum':'Law Enforcement Case Number',
'XCoord':'X-Coordinate (UTM NAD 83 Zone 15)','YCoord':'Y-Coordinate (UTM NAD 83 Zone 15)','ReportType':'Report Type','DOTDstrct':'Iowa Department of Transportation District',
'ISPDstrct':'Iowa State Patrol District','RPA':'Regional Planning Association','MPO':'Metropolitan Planning Organization','County':'County','CityBR':'Base Records City Number',
'UrbanArea':'FHWA Urban Area Code','CvlTwpID':'Civil Township ID','TwnRngSect':'Township, Range, Section','SchDst1011':'School District (2010-2011)','AEA1011':'Area Education Agency (2010-2011)',
'StID1011':'School District State ID (2010-2011)','DNRDstrct':'Iowa Department of Natural Resources District','DNRWldMgmt':'Iowa DNR Wildlife Management Area',
'DNRWldDepr':'Iowa DNR Wildlife Depredation Program Area','DNRFldOff':'Iowa DNR Field Offices (no longer applicable?)','Crash_Year':'Crash Year'
}

zcta_ALIASES = {'Crash_Key':'Crash Key - SAVER Internal Unique Identifier','FirstHarm':'First Harmful Event','CrCoManner':'Manner of Crash/Collision','MajorCause':'Major Cause',
'DrugAlcRel':'Drug or Alcohol Related'
}

zctb_ALIASES = {'Crash_Key':'Crash Key - SAVER Internal Unique Identifier','UnitNum':'Vehicle Unit Number','UnitKey':'Combined Crash_Key and V3UnitNum','SeqEvents1':'Sequence of Events 1st Event',
'SeqEvents2':'Sequence of Events 2nd Event','SeqEvents3':'Sequence of Events 3rd Event','SeqEvents4':'Sequence of Events 4th Event','MostHarm':'Most Harmful Event',
'FixObjStr':'Fixed Object Struck (by vehicle)'
}

zdrv_ALIASES = {'Crash_Key':'Crash Key - SAVER Internal Unique Identifier','UnitNum':'Vehicle Unit Number','UnitKey':'Combined Crash_Key and D1UnitNum','DriverAge':'Driver Age',
'DAgeBin1':'Driver Age - 5 year Bins','DriverGen':'Driver Gender','Charged':'Driver Charged?','AlcTest':'Alcohol Test Given?','AlcResult':'Alcohol Test Results','DrugTest':'Drug Test Given?',
'DrugResult':'Drug Test Results','DriverCond':'Driver Condition','DContCirc1':'Contributing Circumstances 1 - Driver','DContCirc2':'Contributing Circumstances 2 - Driver','VisionObs':'Vision Obscured',
'DriverDist':'Driver Distraction','DL_State':"Driver's License State"
}

zenv_ALIASES = {'Crash_Key':'Crash Key - SAVER Internal Unique Identifier','EContCirc':'Contributing Circumstances - Environment','Weather1':'Weather Conditions 1','Weather2':'Weather Conditions 2',
'Light':'Light Conditions','CSurfCond':'Surface Conditions'
}

zinj_ALIASES = {'Crash_Key':'Crash Key - SAVER Internal Unique Identifier','UnitNum':'Vehicle Unit Number','UnitKey':'Combined Crash_Key and IUnitNum','PersonNum':'Injured Person Number',
'PersonKey':'Combined Crash_Key and INumber','InjStatus':'Injury Status/Severity','InjuredAge':'Age of Injured Person','InjuredGen':'Gender of Injured Person','Seating':'Seating Position',
'OccProtect':'Occupant Protection','Ejection':'Ejection','EjectPath':'Ejection Path','AirbagDep':'Airbag Deployment','Trapped':'Occupant Trapped?','DeathLctn':'Died at Scene/Enroute',
'TrnsprtSrc':'Source of Transport'
}

zltp_ALIASES = {'Month':'Month','DayOfMonth':'Day of Month','Year':'Year','Day':'Day of Week','Time':'Time of Crash','TimeStr':'Time - as string','TimeDay':'Time of Day - Day of Week',
'TimeBin':'Time of Day in 2 hour bins.','TimeBin1':'Time of Day in 1 hour bins.','TimeBin30':'Time of Day in 30 minute bins.','Lighting':'Derived Light Conditions',
'Daylight':'Daylight Hours on Day of Crash','Darkness':'Darkness Hours on Day of Crash','LocFstHarm':'Location of First Harmful Event','RuralUrban':'Rural/Urban','County':'County','City':'City',
'CityBR':'City','CityName':'City Name','UrbanArea':'FHWA Urban Area Code'
}

zloc_ALIASES = {'Crash_Key':'Crash Key - SAVER Internal Unique Identifier','XCoord':'X-Coordinate (UTM NAD 83)','YCoord':'Y-Coordinate (UTM NAD 83)','ZCoord':'Y-Coordinate (UTM NAD 83)',
'LaneDir':'Location Tool  Lane Direction','OverUnder':'Overpass - Underpass','LitDesc':'Location Tool Literal Description','GIMSDate':'GIMS Snapshot Date','LocToolV':'Location Tool Version',
'Captured':'Date of Location Assignment/Capture'
}

zlos_ALIASES = {'Crash_Key':'Crash Key - SAVER Internal Unique Identifier','MSLink':'MSLink Key Field for GIMS'
}

znmt_ALIASES = {'Crash_Key':'Crash Key - SAVER Internal Unique Identifier','UnitNum':'Unit Number of Vehicle Striking (Vehicle Unit Number)','UnitKey':'Combined Crash_Key and NMUnitNum',
'PersonNum':'Number of Non-Motorist','PersonKey':'Combined Crash_Key and NMNumber','NM_Type':'Non-Motorist Type','NM_Loc':'Non-Motorist Location','NM_Action':'Non-Motorist Action',
'NM_Cond':'Non-Motorist Condition','NM_Safety':'Non-Motorist Safety Equipment','NMContCirc':'Contributing Circumstancs - Non-Motorist','AlcTest':'Alcohol Test Given?',
'AlcResult':'Alcohol Test Results','DrugTest':'Drug Test Given?','DrugResult':'Drug Test Results','NMTCharged':'Non-Motorist Charged?'
}

zrda_ALIASES = {'Crash_Key':'Crash Key - SAVER Internal Unique Identifier','System':'Road System','Route':'Route','SystemStr':'Route in String Format with System',
'Cardinal':'Cardinal Direction of Vehicles','Ramp':'Mainline or Ramp','CoRoadRte':'County Road Route','Literal':'Derived Literal Description','RoadClass':'Road Classification',
'IntClass':'Intersection Class','SystemConc':'Concatenated System','RContCirc':'Contributing Circumstances - Roadway','RoadType':'Type of Roadway Junction/Feature','FRA':'FRA Number',
'Paved':'Paved or not'
}

zrdb_ALIASES = {'Crash_Key':'Crash Key - SAVER Internal Unique Identifier','UnitNum':'Vehicle Unit Number','UnitKey':'Combined Crash_Key and RUnitNum','SpeedLimit':'Speed Limit',
'TrafCont':'Traffic Controls','HorizAlign':'Horizontal Alignment (curve)','VertAlign':'Vertical Alignment (grade)'
}

zsev_ALIASES = {'Crash_Key':'Crash Key - SAVER Internal Unique Identifier','CSeverity':'Crash Severity','Fatalities':'Number of Fatalities','Injuries':'Number of Injuries',
'MajInjury':'Number of Major Injuries','MinInjury':'Number of Minor Injuries','PossInjury':'Number of Possible Injuries','UnkInjury':'Number of Unknown Injuries','PropDmg':'Amount of Property Damage',
'Vehicles':'Number of Vehicles','TOccupants':'Total Number of Occupants'
}

zuni_ALIASES = {'Crash_Key':'Crash Key - SAVER Internal Unique Identifier','UnitNum':'Vehicle Unit Number','UnitKey':'Combined Crash_Key and IUnitNum','PersonNum':'Injured Person Number',
'PersonKey':'Combined Crash_Key and INumber','InjStatus':'Injury Status/Severity','InjuredAge':'Age of Injured Person','InjuredGen':'Gender of Injured Person','Seating':'Seating Position',
'OccProtect':'Occupant Protection','Ejection':'Ejection','EjectPath':'Ejection Path','AirbagDep':'Airbag Deployment','Trapped':'Occupant Trapped?','DeathLctn':'Died at Scene/Enroute',
'TrnsprtSrc':'Source of Transport'
}

zveh_ALIASES = {'UnitNum':'Vehicle Unit Number','UnitKey':'Combined Crash_Key and V1UnitNum','VConfig':'Vehicle Configuration','VYear':'Vehicle Year','Color':'Vehicle Color','Make':'Vehicle Make',
'Model':'Vehicle Model','Style':'Vehicle Style','EmerVeh':'Special Function of Vehicle','EmerStatus':'Emergency Status','BusUse':'Bus Use','Occupants':'Vehicle Occupants',
'CargoBody':'Cargo Body Type','Defect':'Vehicle Defect','InitDir':'Initial Direction of Travel','VAction':'Vehicle Action','VLP_State':'License Plate State','VLP_Year':'License Plate Year',
'TRL_State':'Trailer Plate State','TRL_Year':'Trailer Plate Year'
}

zvdm_ALIASES = {'Crash_Key':'Crash Key - SAVER Internal Unique Identifier','UnitNum':'Vehicle Unit Number','UnitKey':'Combined Crash_Key and V2UnitNum','InitImpact':'Point of Initial Impact',
'MostDamage':'Most Damaged Area','Damage':'Extent of Damage','RepairCost':'Approximate Cost to Repair or Replace','Towed':'Towed?'
}

zwkz_ALIASES = {'Crash_Key':'Crash Key - SAVER Internal Unique Identifier','WZ_Related':'Workzone Related?','WZ_Loc':'Location','WZ_Type':'Type','WZ_Actvty':'Work Zone Activity',
'Workers':'Workers Present?'
}

# Function to format the user input
def formatInput(string, delimiter):
    string = string.lower()  # Convert to lower case
    inputList = string.split(delimiter)  # create a delimited list

    for i in range(len(inputList)):
        inputList[i] = inputList[i].strip()  # Remove white-space

    return inputList

def dbf2csv(dbfpath, csvpath):
    ''' To convert .dbf file or any shapefile/featureclass to csv file
    Inputs:
        dbfpath: full path to .dbf file [input] or featureclass
        csvpath: full path to .csv file [output]

    '''
    #import csv
    rows = arcpy.SearchCursor(dbfpath)
    csvFile = csv.writer(open(csvpath + ".csv", 'wb')) #output csv  
    fieldnames = [f.name for f in arcpy.ListFields(dbfpath)]

    allRows = []
    for row in rows:
        rowlist = []
        for field in fieldnames:
            rowlist.append(row.getValue(field))
        allRows.append(rowlist)

    csvFile.writerow(fieldnames)
    for row in allRows:
        csvFile.writerow(row)
    row = None
    rows = None

# Function to apply aliases to fields
def fieldAlias(tab, Level, createMode):
    if createMode == 'f':
        fields = arcpy.ListFields(tab)
        for setName in Level:
            # Apply aliases
            if setName == "zshp":
                for key, value in zshp_ALIASES.iteritems():
                    for field in fields:
                        if key.upper() == field.name.upper():
                            arcpy.AlterField_management(tab, key, new_field_alias=value)
            elif setName == "zcvo":
                for key, value in zcvo_ALIASES.iteritems():
                    for field in fields:
                        if key.upper() == field.name.upper():
                            arcpy.AlterField_management(tab, key, new_field_alias=value)
            elif setName == "zcta":
                for key, value in zcta_ALIASES.iteritems():
                    for field in fields:
                        if key.upper() == field.name.upper():
                            arcpy.AlterField_management(tab, key, new_field_alias=value)
            elif setName == "zctb":
                for key, value in zctb_ALIASES.iteritems():
                    for field in fields:
                        if key.upper() == field.name.upper():
                            arcpy.AlterField_management(tab, key, new_field_alias=value)
            elif setName == "zdrv":
                for key, value in zdrv_ALIASES.iteritems():
                    for field in fields:
                        if key.upper() == field.name.upper():
                            arcpy.AlterField_management(tab, key, new_field_alias=value)
            elif setName == "zenv":
                for key, value in zenv_ALIASES.iteritems():
                    for field in fields:
                        if key.upper() == field.name.upper():
                            arcpy.AlterField_management(tab, key, new_field_alias=value)
            elif setName == "zinj":
                for key, value in zinj_ALIASES.iteritems():
                    for field in fields:
                        if key.upper() == field.name.upper():
                            arcpy.AlterField_management(tab, key, new_field_alias=value)
            elif setName == "zltp":
                for key, value in zltp_ALIASES.iteritems():
                    for field in fields:
                        if key.upper() == field.name.upper():
                            arcpy.AlterField_management(tab, key, new_field_alias=value)
            elif setName == "zloc":
                for key, value in zloc_ALIASES.iteritems():
                    for field in fields:
                        if key.upper() == field.name.upper():
                            arcpy.AlterField_management(tab, key, new_field_alias=value)
            elif setName == "zlos":
                for key, value in zlos_ALIASES.iteritems():
                    for field in fields:
                        if key.upper() == field.name.upper():
                            arcpy.AlterField_management(tab, key, new_field_alias=value)
            elif setName == "znmt":
                for key, value in znmt_ALIASES.iteritems():
                    for field in fields:
                        if key.upper() == field.name.upper():
                            arcpy.AlterField_management(tab, key, new_field_alias=value)
            elif setName == "zrda":
                for key, value in zrda_ALIASES.iteritems():
                    for field in fields:
                        if key.upper() == field.name.upper():
                            arcpy.AlterField_management(tab, key, new_field_alias=value)
            elif setName == "zrdb":
                for key, value in zrdb_ALIASES.iteritems():
                    for field in fields:
                        if key.upper() == field.name.upper():
                            arcpy.AlterField_management(tab, key, new_field_alias=value)
            elif setName == "zsev":
                for key, value in zsev_ALIASES.iteritems():
                    for field in fields:
                        if key.upper() == field.name.upper():
                            arcpy.AlterField_management(tab, key, new_field_alias=value)
            elif setName == "zuni":
                for key, value in zuni_ALIASES.iteritems():
                    for field in fields:
                        if key.upper() == field.name.upper():
                            arcpy.AlterField_management(tab, key, new_field_alias=value)
            elif setName == "zveh":
                for key, value in zveh_ALIASES.iteritems():
                    for field in fields:
                        if key.upper() == field.name.upper():
                            arcpy.AlterField_management(tab, key, new_field_alias=value)
            elif setName == "zvdm":
                for key, value in zvdm_ALIASES.iteritems():
                    for field in fields:
                        if key.upper() == field.name.upper():
                            arcpy.AlterField_management(tab, key, new_field_alias=value)
            elif setName == "zwkz":
                for key, value in zwkz_ALIASES.iteritems():
                    for field in fields:
                        if key.upper() == field.name.upper():
                            arcpy.AlterField_management(tab, key, new_field_alias=value)

    return 'test'


# Get list of initial crash keys from zshp feature class
crashKey = []
setQuery = ''
setCounty = ''
fy = 0

PROJECT_FOLDER = "D:/"

arcpy.AddMessage('---Welcome to Project Starter v' + VERSION + '!---\n')  # Greet the user

# Prompt user for project name
projectName = "HeavyTruck_20200828"

# Prompt user for project number
projectNumber = "1"

userYear = "2020"  # Create list from input
finalYear = []

for year in userYear:
    finalYear.append(year)

userDataset = formatInput("zcit;zcta;zctb;zcvo;zdrv;zenv;zinj;zloc;zlos;zltp;znmt;zrda;zrdb;zsev;zuni;zvdm;zveh;zwkz", ';')  # Process selection into a list

dataset = ['zshp']  # List to hold user-specified datasets (zshp automatically included)

for i in range(len(userDataset)):
    dataset.append(userDataset[i])

# Get queries from user
query = []
userInput = ''
queries = "zveh, vconfig>=7 and vconfig<=16"


userQuery = formatInput(queries, ',')

    if userQuery[0]:
        # Check if something was entered wrong
        if userQuery[0] in DATASET and len(userQuery) == 2: # and userQuery[1].count('"') == 2 and userQuery[1].endswith('"') == False:
            query.append(userQuery)  # Add the query to the list
        elif userQuery[0] not in dataset:
            arcpy.AddMessage('\nERROR!  "' + userQuery[0] + '" is not a dataset in your selection!')
            quit()
        elif len(userQuery) != 2:# or userQuery[1].count('"') != 2 or userQuery[1].endswith('"'):
            arcpy.AddMessage('\nERROR!  You have not formulated the query correctly!')
            quit()

# Ask user if they would like the results in a geodatabase
#if arcpy.GetParameterAsText(7) == 'Shapefile':
if "File Geodatabase" == 'Shapefile':
    createMode = 's'
else:
    createMode = 'f'

if createMode == 'f':
    # Ask the user if they would like to create domains for their data
    createDomain = "true"
else:
    createDomain = False  # Can't do domains without a file geodatabase, bro

if createMode == 's':
    tableOutput = "." + "GDB Table"
else:
    tableOutput = False

if "true" == "true":
    latlong = 'y'
else:
    latlong = 'n'



mergedfolder = "D:/2020/".path


#------------------------------ Begin script used by both versions

finalYear.sort()  # Sort the list of years so that they are in ascending order
dataset.sort()  # Sort the dataset selection in alphabetical order

# Set environment variables
arcpy.env.overwriteOutput = True

arcpy.AddMessage('\nSelecting crashes...')

# Only select crashes if a query was made
if query:
    # Construct long query for zshp
    for sqlStatement in query:
        if sqlStatement[0] == 'zshp':
            fy = 1
            if setQuery:
                setQuery = setQuery + ' AND ' + '(' + sqlStatement[1] + ')'
            else:
                setQuery = setQuery + '(' + sqlStatement[1] + ')'


for year in finalYear:  # Loop through years
    if fy == 0:
        if setQuery:
            setQuery = setQuery + ' OR ' + '("CRASH_YEAR" = ' + year + ')'
        else:
            setQuery = setQuery + '(("CRASH_YEAR" = ' + year + ')'
    else:
        setQuery = setQuery +  ' AND ' + '(("CRASH_YEAR" = ' + year + ')'
        fy = 0

setQuery = setQuery + ')'

inFeatureClass = arcpy.GetParameterAsText(0)
inFeatureClass = os.path.join(inFeatureClass, "")
#print("check path: ", os.path.isdir(inFeatureClass));

if large_dataset:
    tempLocation = arcpy.env.scratchGDB + os.path.sep
else:
    tempLocation = 'in_memory/'

iTableName = tempLocation + 'zshp_i'

arcpy.MakeFeatureLayer_management (inFeatureClass, "stateslyr")

arcpy.SelectLayerByAttribute_management ("stateslyr", "NEW_SELECTION", setQuery)

arcpy.CopyFeatures_management("stateslyr", iTableName)

arcpy.SelectLayerByAttribute_management ("stateslyr", "CLEAR_SELECTION")

crashPoint = arcpy.da.SearchCursor(iTableName, ['CRASH_KEY'])  # Make search cursor

# Loop through records and add all crash keys to the list
for record in crashPoint:
    crashKey.append(record[0])



# Loop through remaining datasets and remove crash keys which do not match
for setName in dataset:
    arcpy.AddMessage('\nSelecting ' + setName)
    if setName != 'zshp':
        # Generate single SQL statement
        setQuery = ''
        setCounty = ''



        for sqlStatement in query:
            if sqlStatement[0] == setName:
                if setQuery:
                    setQuery = setQuery + ' AND ' + '(' + sqlStatement[1] + ')'
                else:
                    setQuery = setQuery + '(' + sqlStatement[1] + ')'

        if setQuery:
        # Generate list of valid keys
            validKey = []


            inputTable = mergedfolder + '/' + setName + '.dbf'

            arcpy.AddMessage('\n' + setQuery)
            crashTable = arcpy.SearchCursor(inputTable, setQuery)  # Make search cursor

            for record in crashTable:
                # Append each key in the selection to the list of valid keys
                validKey.append(record.CRASH_KEY)


            # Remove invalid keys from master list
            i = 0
            while i < len(crashKey):
                if crashKey[i] not in validKey:
                    crashKey.pop(i)
                else:
                    i += 1

# Check if any crashes were selected before continuing
if not crashKey:
    arcpy.AddMessage('ERROR!  No crashes were selected!  The script will now terminate.')
    quit()

# Create table for selected crashes
arcpy.CreateTable_management('in_memory', 'crash')
arcpy.AddField_management('in_memory/crash', 'CRASH_KEY', 'DOUBLE',11,0)
crashKeyTable = 'in_memory/crash'
crashCursor = arcpy.InsertCursor(crashKeyTable)
for key in crashKey:  # Loop through list of CRASH_KEYs and place key in table
    record = crashCursor.newRow()
    record.CRASH_KEY = key

    crashCursor.insertRow(record)

# Create project folder
arcpy.AddMessage('\nCreating project folder...')
arcpy.CreateFolder_management(PROJECT_FOLDER, projectNumber + '-' + projectName.replace(' ', '_'))
arcpy.AddMessage('done!')

# Set project folder variable
projectFolder = PROJECT_FOLDER + '/' + projectNumber + '-' + projectName.replace(' ', '_')

if createMode == 'f':
    # Create geodatabase for output
    arcpy.AddMessage('\nCreating working Geodatabase...')
    arcpy.CreateFileGDB_management(projectFolder, 'working.gdb')
    workspace = projectFolder + '/working.gdb'
else:
    # Create working folder for output
    arcpy.AddMessage('\nCreating working directory...')
    arcpy.CreateFolder_management(projectFolder, 'working')
    workspace = projectFolder + '/working'

arcpy.AddMessage('done!\n')

# Loop through datasets
crashLevel = []
vehicleLevel = []
personLevel = []
otherLevel = []
fieldList = []  # List to hold field names (used for Geodatabase domains




for setName in dataset:
    # Get list of fields for dataset and append to list
    datasetFieldList = arcpy.ListFields(mergedfolder + r'/' + setName
                                        + '.dbf')
    for field in datasetFieldList:
        fieldList.append(field.name)

    tableList = []  # List to hold table names

    # Merge years and locations within dataset
    arcpy.AddMessage('Merging ' + setName + ' tables...')


    inputTable = mergedfolder + "/" + setName + ".dbf"
    # Name for in-memory table
    iTableName = tempLocation + setName + '_i'
    tableName = tempLocation + setName + '_t'

    if setName != 'zshp':
        # Copy table to memory
        arcpy.CopyRows_management(inputTable, iTableName)


    # Join selected crash list
    arcpy.JoinField_management(iTableName, 'CRASH_KEY', crashKeyTable, 'CRASH_KEY')

    if setName == 'zshp':
        # Make feature layer to determine final selection
        arcpy.MakeFeatureLayer_management(iTableName, 'tempTable', """ "CRASH_KEY_1" is not null """)


        if latlong == 'y':
            # Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
            # The following inputs are layers or table views: "CRASH_LEVEL"
            arcpy.AddGeometryAttributes_management(Input_Features="tempTable", Geometry_Properties="POINT_X_Y_Z_M", Length_Unit="", Area_Unit="", Coordinate_System="GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]")
            arcpy.AlterField_management("tempTable","POINT_X", "Longitude")
            arcpy.AlterField_management("tempTable","POINT_Y", "Latitude")

        arcpy.CopyFeatures_management('tempTable', tableName)

    else:
        # Make table view to determine final selection
        arcpy.MakeTableView_management(iTableName, 'tempTable', """ "CRASH_KEY_1" is not null """)
        arcpy.CopyRows_management('tempTable', tableName)

    # Remove un-needed tables
    if setName == 'zshp':
        arcpy.DeleteFeatures_management(iTableName)
    else:
        arcpy.DeleteRows_management(iTableName)

    arcpy.Delete_management('tempTable')  # Delete feature layer or table view
    arcpy.DeleteField_management(tableName, 'CRASH_KEY_1')  # Remove duplicate field

    tableList.append(tableName)  # Append the table to the list

    # Determine where to place the merge
    if setName == 'zshp':
        arcpy.Merge_management(tableList, tempLocation + 'zshp')
    elif setName in CRASH_LEVEL:  # Check if the dataset is crash-level
        crashLevel.append(setName)  # Append it to the crash-level list

        # Merge years together for dataset
        template = mergedfolder + r'/' + setName + '.dbf'
        arcpy.CreateTable_management(tempLocation, setName, template)  # Create empty table

        arcpy.Append_management(tableList, tempLocation + setName, 'NO_TEST')  # Append selection to table
    elif setName in VEHICLE_LEVEL:  # Check if the dataset is vehicle-level
        vehicleLevel.append(setName)  # Append the dataset to the vehicle-level list

        # Merge years together for dataset
        template = mergedfolder + r'/' + setName + '.dbf'

        arcpy.CreateTable_management(tempLocation, setName, template)  # Create empty table

        arcpy.Append_management(tableList, tempLocation + setName, 'NO_TEST')  # Append selection to table
    elif setName in PERSON_LEVEL:  # Check if dataset is person-level
        personLevel.append(setName)  # Append it to the person-level list

        # Merge years together for dataset
        template = mergedfolder + r'/' + setName + '.dbf'
        arcpy.CreateTable_management(tempLocation, setName, template)  # Create empty table
        arcpy.Append_management(tableList, tempLocation + setName, 'NO_TEST')  # Append selection to table
    else:
        # Merge years together for dataset
        template = mergedfolder + r'/' + setName + '.dbf'

        otherLevel.append(setName)  # Append it to the other-level list

        # Set table location
        if createMode == 'f':
            otherTable = OTHER[setName]
        else:
            otherTable = OTHER[setName] + '.dbf'

        # Create empty table
        arcpy.CreateTable_management(workspace, otherTable, template)


        arcpy.Append_management(tableList, workspace + '/' + otherTable, 'NO_TEST')  # Append selection to table



    # Delete in-memory tables to free up memory
    for table in tableList:
        arcpy.Delete_management(table)

    arcpy.AddMessage('done!')  # Done merging datasets

# Join crash-level tables together
arcpy.AddMessage('\nJoining crash-level attributes together...')

for setName in crashLevel:  # Loop through each crash-level dataset and join it

    # #    # BEGIN DEBUG
    # #    fields = arcpy.ListFields('in_memory/zshp')
    # #    for field in fields:
    # #        print(field.name)
    # #    fields = arcpy.ListFields('in_memory/' + setName)
    # #    for field in fields:
    # #        print(field.name)
    # #    # END DEBUG

    arcpy.JoinField_management(tempLocation + 'zshp', 'CRASH_KEY', tempLocation + setName, 'CRASH_KEY')

    # Remove duplicate CRASH_KEY field
    arcpy.DeleteField_management(tempLocation + 'zshp', 'CRASH_KEY_1')

arcpy.AddMessage('done!')

# Create a feature layer in the geodatabase from the join
arcpy.AddMessage('Writing to feature class...')

# Determine feature-class and table locations
if createMode == 'f':
    crashLevelFC = '/CRASH_LEVEL'
    vehicleLevelTab = '/VEHICLE_LEVEL'
    personLevelTab = '/PERSON_LEVEL'
else:
    crashLevelFC = '/CRASH_LEVEL.shp'
    vehicleLevelTab = '/VEHICLE_LEVEL.dbf'
    personLevelTab = '/PERSON_LEVEL.dbf'

# Remove any remaining duplicate fields
fieldList = arcpy.ListFields(tempLocation + 'zshp')
for field in fieldList:
    # If field is a duplicate, remove it
    if field.name.endswith('_1'):
        arcpy.DeleteField_management(tempLocation + 'zshp', field.name)

# Copy to file
arcpy.CopyFeatures_management(tempLocation + 'zshp', workspace + crashLevelFC)

fieldAlias(workspace + crashLevelFC, ['zshp'], createMode)

if crashLevel:
    fieldAlias(workspace + crashLevelFC, crashLevel, createMode)

arcpy.AddMessage('done!')

# Join vehicle-level tables together (if any)
if vehicleLevel:
    # Set the base of the join as the first item in the list, but not zcvo or zcit
    if vehicleLevel[0] == 'zcvo' and len(vehicleLevel) > 1:
        if vehicleLevel[1] == 'zcit':
            joinBase = vehicleLevel[2]
            vehicleLevel.pop(2)
        else:
            joinBase = vehicleLevel[1]
            vehicleLevel.pop(1)
    elif vehicleLevel[0] == 'zcit' and len(vehicleLevel) > 1:
        if vehicleLevel[1] == 'zcvo':
            joinBase = vehicleLevel[2]
            vehicleLevel.pop(2)
        else:
            joinBase = vehicleLevel[1]
            vehicleLevel.pop(1)
    else:
        joinBase = vehicleLevel[0]
        vehicleLevel.pop(0)
else:
    joinBase = ''

if vehicleLevel and joinBase:
    arcpy.AddMessage('\nJoining vehicle-level attributes together...')

    # Loop through each remaining vehicle-level dataset and join it
    for setName in vehicleLevel:
        arcpy.JoinField_management(tempLocation + joinBase, 'UNITKEY', tempLocation + setName, 'UNITKEY')

        # Remove duplicate fieldS
        arcpy.DeleteField_management(tempLocation + joinBase, 'UNITKEY_1')
        arcpy.DeleteField_management(tempLocation + joinBase, 'UNITNUM_1')
        arcpy.DeleteField_management(tempLocation + joinBase, 'CRASH_KEY_1')

    arcpy.AddMessage('done!')

if joinBase:
    # Create a table in the geodatabase from the join
    arcpy.AddMessage('Writing to table...')
    arcpy.CopyRows_management(tempLocation + joinBase, workspace + vehicleLevelTab)
    fieldAlias(workspace + vehicleLevelTab, [joinBase], createMode)
    if tableOutput == ".csv":
            dbf2csv(workspace + vehicleLevelTab, workspace  + vehicleLevelTab[:-4])
            arcpy.Delete_management(workspace + vehicleLevelTab)
    arcpy.AddMessage('done!')

if vehicleLevel:
    fieldAlias(workspace + vehicleLevelTab, vehicleLevel, createMode)
    if tableOutput == ".csv":
            dbf2csv(workspace + vehicleLevelTab, workspace  + vehicleLevelTab[:-4])
            arcpy.Delete_management(workspace + '/' + otherTable)


# Append injuries and non-injuries together
if 'zinj' in personLevel and 'zuni' in personLevel:
    arcpy.Append_management(tempLocation + 'zuni', tempLocation + 'zinj', 'NO_TEST')
    arcpy.Sort_management(tempLocation + 'zinj', tempLocation + 'person', 'PERSONKEY')
    personAppend = True
else:
    personAppend = False

if personAppend:
    # Join non-motorist info (in any) and create person-level table
    if 'znmt' in personLevel:
        arcpy.AddMessage('\nJoining person-level attributes together...')
        arcpy.JoinField_management(tempLocation + 'person', 'PERSONKEY', tempLocation + 'znmt', 'PERSONKEY')

        # Remove duplicate fields
        arcpy.DeleteField_management(tempLocation + 'person', 'PERSONKEY_1')
        arcpy.DeleteField_management(tempLocation + 'person', 'PERSONNUM_1')
        arcpy.DeleteField_management(tempLocation + 'person', 'UNITKEY_1')
        arcpy.DeleteField_management(tempLocation + 'person', 'UNITNUM_1')
        arcpy.DeleteField_management(tempLocation + 'person', 'CRASH_KEY_1')

        arcpy.AddMessage('done!')
    arcpy.AddMessage('Writing to table...')
    arcpy.CopyRows_management(tempLocation + 'person', workspace + personLevelTab)
    arcpy.AddMessage('done!')
else:
    # Create separate tables
    for setName in personLevel:
        arcpy.AddMessage('Writing data to table...')

        # Set table location
        if createMode == 'f':
            otherTable = OTHER[setName]
        else:
            otherTable = OTHER[setName] + '.dbf'

        # Create table
        arcpy.CopyRows_management(tempLocation + setName, workspace + '/' + otherTable)
        fieldAlias(workspace + '/' + otherTable, [setName], createMode)
        if tableOutput == ".csv":
            dbf2csv(workspace + '/' + otherTable, workspace + '/' + OTHER[setName])
            arcpy.Delete_management(workspace + '/' + otherTable)
    arcpy.AddMessage('done!')

if personAppend:
    fieldAlias(workspace + personLevelTab, personLevel, createMode)
    if tableOutput == ".csv":
            dbf2csv(workspace + personLevelTab, workspace  + personLevelTab[:-4])
            arcpy.Delete_management(workspace + '/' + otherTable)

if otherLevel:
    for setName in otherLevel:
        # Set table location
        if createMode == 'f':
            otherTable = OTHER[setName]
        else:
            otherTable = OTHER[setName] + '.dbf'
        fieldAlias(workspace + '/' + otherTable, [setName], createMode)
        if tableOutput == ".csv":
            dbf2csv(workspace + '/' + otherTable, workspace + '/' + OTHER[setName])
            arcpy.Delete_management(workspace + '/' + otherTable)

# Get list of lookup tables
if createDomain:
    arcpy.AddMessage('\nCreating Geodatabase domains...')
    arcpy.AddMessage(os.path.dirname(os.path.realpath(__file__)))
    if not os.path.exists(os.path.dirname(os.path.realpath(__file__)) + r'/2015 Domain Tab Delimited Text Files') or not os.path.isdir(os.path.dirname(os.path.realpath(__file__)) + r'/2015 Domain Tab Delimited Text Files'):
        arcpy.AddMessage('Error: Missing domain folder ' + os.path.dirname(os.path.realpath(__file__)) + r'/2015 Domain Tab Delimited Text Files')
    else:
        for gdb in dataset:
            tabname = ''
            arcpy.AddMessage(gdb)
            for fpath in glob.glob(os.path.dirname(os.path.realpath(__file__)) + r'/2015 Domain Tab Delimited Text Files/' + gdb + r'*.tab'):
                tabname = fpath
            if tabname:
                with open(tabname, 'r') as f:
                    first_line = f.readline()
                fieldNameList = re.split(r'\s+', first_line)

                # Loop through fields
                for fieldName in fieldNameList:
                    if fieldName[-4:] != 'DESC' and fieldName != '':

                        arcpy.AddMessage('\nAssigning domain(s) to table ' + fieldName + '...')

                        arcpy.TableToDomain_management(tabname, fieldName, fieldName + 'DESC',
                                                   workspace, gdb+ '_' + fieldName, '', 'APPEND')

                        if gdb in CRASH_LEVEL or gdb == 'zshp':
                            if fieldName != 'SCHDST1011':
                                try:
                                    arcpy.AssignDomainToField_management(workspace + crashLevelFC, fieldName, gdb+ '_' + fieldName)
                                except:
                                    arcpy.AddMessage('Domain for ' + fieldName + ' not included')
                                arcpy.AddMessage('done!')
                        if gdb in VEHICLE_LEVEL:
                                arcpy.AssignDomainToField_management(workspace + vehicleLevelTab, fieldName, gdb+ '_' + fieldName)
                                arcpy.AddMessage('done!')
                        if gdb in PERSON_LEVEL:
                            if personAppend:
                                arcpy.AssignDomainToField_management(workspace + personLevelTab, fieldName, gdb+ '_' + fieldName)
                                arcpy.AddMessage('done!')
                        if gdb in OTHER:
                            otherTable = OTHER[gdb]
                            if arcpy.Exists(workspace + '/' + otherTable):
                                arcpy.AssignDomainToField_management(workspace + '/' + otherTable, fieldName, gdb+ '_' + fieldName)
                                arcpy.AddMessage('done!')

arcpy.AddMessage('done!')
