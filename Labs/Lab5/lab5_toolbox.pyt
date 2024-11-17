# Holt Chambers

import arcpy
import os

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Lab5_Toolbox"
        self.alias = "Lab5_Toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [Lab5_Tool]


class Lab5_Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Lab5_Tool"
        self.description = ""
        self.canRunInBackground = False

    # using the FAC Code as my input (i.e. NSG)
    def getParameterInfo(self):
        """Define parameter definitions"""
        param_GDB_Folder = arcpy.Parameter(
            displayName="GDB Folder",
            name="gdbfolder",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param_GDB_Name = arcpy.Parameter(
            displayName="GDB Name",
            name="gdbname",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param_Campus_GDB = arcpy.Parameter(
            displayName="Campus GDB",
            name="campusgdb",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param_garage_layer = arcpy.Parameter(
            displayName="Garage Layer Name",
            name="garagelayername",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param_garage_csv = arcpy.Parameter(
            displayName="Garage CSV",
            name="garagecsv",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param_Selected_Garage_Code = arcpy.Parameter(
            displayName="Selected Garage Code",
            name="selectedgaragecode",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param_Buffer_Radius = arcpy.Parameter(
            displayName="Buffer Radius",
            name="bufferadius",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input"
        )

        params = [ 
            param_GDB_Folder,
            param_GDB_Name,
            param_Campus_GDB,
            param_garage_layer,
            param_garage_csv,
            param_Selected_Garage_Code,
            param_Buffer_Radius
            ]
        return params

    def execute(self, parameters, messages):
        """The source code of the tool."""
        #query user input
        GDB_Folder = parameters[0].valueAsText
        GDB_Name= parameters[1].valueAsText
        Campus_GDB = parameters[2].valueAsText
        Garage_Layer_Name = parameters[3].valueAsText
        Garage_CSV_File = parameters[4].valueAsText
        Selected_Garage_Code = parameters[5].valueAsText
        Buffer_Input = parameters[6].valueAsText
        Buffer_Radius = Buffer_Radius = Buffer_Input + " meters"

        #create gdb
        arcpy.management.CreateFileGDB(GDB_Folder, GDB_Name)
        GDB_Full_Path = GDB_Folder + '/' + GDB_Name 

        #import garage csv
        garages = arcpy.management.MakeXYEventLayer(Garage_CSV_File, 'X', 'Y', Garage_Layer_Name)
        arcpy.FeatureClassToGeodatabase_conversion(garages, GDB_Full_Path)

        ### >>>>>> Add your code here
        #search cursor
        garage_points = Campus_GDB + "/GaragePoints"
        where_clause = "FAC_CODE = '%s'" % Selected_Garage_Code
        cursor = arcpy.da.SearchCursor(garage_points, "FAC_Code", where_clause)

        shouldProceed = False

        for row in cursor:
            if Selected_Garage_Code in row:
                shouldProceed = True
                break

        if shouldProceed == True:
            #select garage as feature layer
            selected_garage_layer = os.path.join(Campus_GDB, Selected_Garage_Code)
            garage_feature = arcpy.Select_analysis(garages, selected_garage_layer, where_clause)

            # Buffer the selected building
            garage_buff_name = Campus_GDB + "/building_buffed"
            arcpy.Buffer_analysis(garage_feature, garage_buff_name, Buffer_Radius)

            #clip
            structures = Campus_GDB + "/Structures"
            garage_clip_name = Campus_GDB + "/building_clipped"
            arcpy.Clip_analysis(structures, garage_buff_name, garage_clip_name)

            # copy created features to the Lab 5 geodatabase
            arcpy.management.CopyFeatures(selected_garage_layer, os.path.join(GDB_Full_Path, 'garage_selected'))
            arcpy.management.CopyFeatures(garage_buff_name, os.path.join(GDB_Full_Path, 'building_buffed'))
            arcpy.management.CopyFeatures(garage_clip_name, os.path.join(GDB_Full_Path, 'garage_clipped'))

            arcpy.AddMessage("Success!")
        else:
            arcpy.AddError("Unable to locate the building you entered. Please try a different FAC Code like NSG")

        return
