import arcpy
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = r'C:\Users\holtc\HAC-GEOG676-Lab\Labs\Lab5\Lab 5 Data'

"""
You can change the `workspace` path as your wish.
"""
arcpy.env.workspace = INPUT_DIR

"""
Here are some hints of what values the following variables should accept.
When running, the following code section will accept user input from terminal
Use `input()` method.

GDB_Folder = "***/Labs/Lab5"
GDB_Name = "Lab5.gdb"
Garage_CSV_File = "***/Labs/Lab5/garages.csv"
Garage_Layer_Name = "garages"
Campus_GDB = "***/Labs/Lab5/Campus.gdb"
Selected_Garage_Name = "Northside Parking Garage"
Buffer_Radius = "150 meter"
"""
### >>>>>> Add your code here
print("Please input the following parameters:\n")
GDB_Folder = r'C:\Users\holtc\HAC-GEOG676-Lab\Labs\Lab5'
GDB_Name = 'Lab5.gdb'
Garage_CSV_File = r'C:\Users\holtc\HAC-GEOG676-Lab\Labs\Lab5\Lab 5 Data\garages.csv'
Garage_Layer_Name = 'garages'
Campus_GDB = r'C:\Users\holtc\HAC-GEOG676-Lab\Labs\Lab5\Lab 5 Data\Campus.gdb'
Selected_Garage_Name = input('Enter the Garage Name:')
Buffer_Input = input('Enter the garage buffer radius in meters:')
Buffer_Radius = Buffer_Input + " meters"
### <<<<<< End of your code here

"""
In this section, you can re-use your codes from Lab4.

"""
### >>>>>> Add your code here
#create gdb
arcpy.management.CreateFileGDB(GDB_Folder, GDB_Name)

GDB_Full_Path = GDB_Folder + '/' + GDB_Name 

#import garage csv
garages = arcpy.management.MakeXYEventLayer(Garage_CSV_File, 'X', 'Y', Garage_Layer_Name)
arcpy.FeatureClassToGeodatabase_conversion(garages, GDB_Full_Path)
### <<<<<< End of your code here

"""
Create a searchCursor.
Select the garage with `where` or `SQL` clause using `arcpy.analysis.Select` method.
Apply `Buffer` and `Clip` analysis on the selected feature.
Use `arcpy.analysis.Buffer()` and `arcpy.analysis.Clip()`.
"""
### >>>>>> Add your code here
#search cursor
garage_points = Campus_GDB + "/GaragePoints"
where_clause = "LotName = '%s'" % Selected_Garage_Name
cursor = arcpy.da.SearchCursor(garage_points, "LotName", where_clause)

shouldProceed = False

for row in cursor:
    if Selected_Garage_Name in row:
        shouldProceed = True
        break

if shouldProceed == True:
    #select garage as feature layer
    selected_garage_layer_name = Selected_Garage_Name
    garage_feature = arcpy.analysis.Select(garages, selected_garage_layer_name, where_clause)

    # Buffer the selected building
    garage_buff_name = "/building_buffed"
    arcpy.analysis.Buffer(garage_feature, garage_buff_name, Buffer_Radius)

    #clip
    structures = Campus_GDB + "/Structures"
    garage_clip_name = "/building_clipped"
    arcpy.analysis.Clip(structures, garage_buff_name, garage_clip_name)

    arcpy.management.CopyFeatures(selected_garage_layer_name, os.path.join(GDB_Full_Path, 'garage_selected'))
    arcpy.management.CopyFeatures(garage_buff_name, os.path.join(GDB_Full_Path, 'building_buffed'))
    arcpy.management.CopyFeatures(garage_clip_name, os.path.join(GDB_Full_Path, 'garage_clipped'))

    print("success")
else:
    print("error")
### <<<<<< End of your code here