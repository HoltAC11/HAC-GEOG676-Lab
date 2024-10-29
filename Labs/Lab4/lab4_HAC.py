import arcpy
import os

import arcpy.analysis
import arcpy.management

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

### >>>>>> Add your code here
INPUT_DB_PATH = r"C:\Users\holtc\HAC-GEOG676-Lab\Labs\Lab4\Lab 4 Data\Campus.gdb"
CSV_PATH = r"C:\Users\holtc\HAC-GEOG676-Lab\Labs\Lab4\Lab 4 Data\garages.csv"
OUTPUT_DB_PATH = r"C:\Users\holtc\HAC-GEOG676-Lab\Labs\Lab4\Output_GDB"
### <<<<<< End of your code here

arcpy.env.workspace = INPUT_DB_PATH

# Layers need to be kept
layers_to_keep = ["GaragePoints", "LandUse", "Structures", "Trees"]

# list all feature clases
feature_classes = arcpy.ListFeatureClasses()

# delete other classes
for fc in feature_classes:
    if fc not in layers_to_keep:
        arcpy.management.Delete(fc)

# create GDB management
if not os.path.exists(OUTPUT_DB_PATH + "\Lab4GDB.gdb"):
    ### >>>>>> Add your code here
    arcpy.management.CreateFileGDB(OUTPUT_DB_PATH, "Lab4GDB.gdb")
    ### <<<<<< End of your code here

# Load .csv file to input GDB
### >>>>>> Add your code here
arcpy.management.XYTableToPoint(CSV_PATH,"garages", "X", "Y")
    
### <<<<<< End of your code here

# Print spatial references before re-projection
print(f"Before Re-Projection...")
print(f"garages layer spatial reference: {arcpy.Describe('garages').spatialReference.name}.")
print(f"Structures layer spatial reference: {arcpy.Describe('Structures').spatialReference.name}.")

# Re-project
## >>>>>>>>> change the codes below
target_ref = arcpy.SpatialReference('GCS_WGS_1984')
arcpy.management.Project(
   'Structures',
   'Structures_Projected',
   target_ref
)
## <<<<<<<< End of your code here
# print spatial references after re-projection
print(f"After Re-Projection...")
print(f"garages layer spatial reference: {arcpy.Describe('garages').spatialReference.name}.")
print(f"re-projected Structures layer spatial reference: {arcpy.Describe('structures_projected').spatialReference.name}")

### >>>>>> Add your code here
# Buffer analysis
radiumStr = "150 meter"
arcpy.analysis.Buffer('garages', 'garages_buffered', radiumStr)
# Intersect analysis
arcpy.analysis.Intersect(['garages_buffered', 'structures_projected'], 'intersection')
# Output features to the created GDB
if not os.path.exists(OUTPUT_DB_PATH + "\Lab4GDB.gdb" + "\Garages"):  # Check if the files exist already to prevent errors
    arcpy.management.CopyFeatures('garages', os.path.join(OUTPUT_DB_PATH, 'Lab4GDB.gdb', 'Garages'))
    arcpy.management.CopyFeatures('Structures', os.path.join(OUTPUT_DB_PATH, 'Lab4GDB.gdb', 'Structures'))
    arcpy.management.CopyFeatures('garages_buffered', os.path.join(OUTPUT_DB_PATH, 'Lab4GDB.gdb', 'Garages_Buffered'))
    arcpy.management.CopyFeatures('intersection', os.path.join(OUTPUT_DB_PATH, 'Lab4GDB.gdb', 'Intersection'))
