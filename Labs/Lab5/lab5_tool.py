import arcpy
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = r'C:\Users\holtc\HAC-GEOG676-Lab\Labs\Lab5\Lab 5 Data'

arcpy.env.workspace = INPUT_DIR

### >>>>>> Add your code here
print("Please input the following parameters:\n")
GDB_Folder = r'C:\Users\holtc\HAC-GEOG676-Lab\Labs\Lab5'
GDB_Name = 'Lab5.gdb'
Garage_CSV_File = r'C:\Users\holtc\HAC-GEOG676-Lab\Labs\Lab5\Lab 5 Data\garages.csv'
Garage_Layer_Name = 'garages'
Campus_GDB = r'C:\Users\holtc\HAC-GEOG676-Lab\Labs\Lab5\Lab 5 Data\Campus.gdb'
Selected_Garage_Code = input('Enter the Garage FAC Code:')  # using the FAC Code as my input (i.e. NSG)
Buffer_Input = input('Enter the garage buffer radius in meters:')
Buffer_Radius = Buffer_Input + " meters"
### <<<<<< End of your code here

### >>>>>> Add your code here
#create gdb
arcpy.management.CreateFileGDB(GDB_Folder, GDB_Name)

GDB_Full_Path = GDB_Folder + '/' + GDB_Name 

#import garage csv
garages = arcpy.management.MakeXYEventLayer(Garage_CSV_File, 'X', 'Y', Garage_Layer_Name)
arcpy.FeatureClassToGeodatabase_conversion(garages, GDB_Full_Path)
### <<<<<< End of your code here

### >>>>>> Add your code here
#search cursor
garage_points = Campus_GDB + "/GaragePoints"
where_clause = "FAC_Code = '%s'" % Selected_Garage_Code
cursor = arcpy.da.SearchCursor(garage_points, "FAC_Code", where_clause)

shouldProceed = False

for row in cursor:
    if Selected_Garage_Code in row:
        shouldProceed = True
        break

if shouldProceed == True:
    #select garage as feature layer
    selected_garage_layer = os.path.join(Campus_GDB, Selected_Garage_Code)
    garage_feature = arcpy.analysis.Select(garages, selected_garage_layer, where_clause)

    # Buffer the selected building
    garage_buff_name = Campus_GDB + "/building_buffed"
    arcpy.analysis.Buffer(garage_feature, garage_buff_name, Buffer_Radius)

    #clip
    structures = Campus_GDB + "/Structures"
    garage_clip_name = Campus_GDB + "/building_clipped"
    arcpy.analysis.Clip(structures, garage_buff_name, garage_clip_name)

    arcpy.management.CopyFeatures(selected_garage_layer, os.path.join(GDB_Full_Path, 'garage_selected'))
    arcpy.management.CopyFeatures(garage_buff_name, os.path.join(GDB_Full_Path, 'building_buffed'))
    arcpy.management.CopyFeatures(garage_clip_name, os.path.join(GDB_Full_Path, 'garage_clipped'))

    print("Success!")
else:
    print("Unable to locate the building you entered. Please try a different FAC Code like NSG")
### <<<<<< End of your code here