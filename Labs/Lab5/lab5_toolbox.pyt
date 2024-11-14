# -*- coding: utf-8 -*-

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

    def getParameterInfo(self):
        """Define parameter definitions"""
        param_GDB_folder = arcpy.Parameter(
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
        param_Garage_CSV_File = arcpy.Parameter(
            displayName="Garage CSV File",
            name="garagecsvfile",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param_Garage_Layer_Name = arcpy.Parameter(
            displayName="Garage Layer Name",
            name="garagelayername",
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
        param_Selected_Garage_Name = arcpy.Parameter(
            displayName="Selected Garage Name",
            name="selectedgaragename",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param_Buffer_Radius = arcpy.Parameter(
            displayName="Buffer Radius",
            name="bufferadius",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )

        params = [
            param_GDB_folder, 
            param_GDB_Name,
            param_Garage_CSV_File, 
            param_Garage_Layer_Name,
            param_Campus_GDB,
            param_Selected_Garage_Name,
            param_Buffer_Radius
            ]
        return params

    def execute(self, parameters, messages):
        """The source code of the tool."""
        #query user input
        GDB_Folder = parameters[0].valueAsText
        GDB_Name = parameters[1].valueAsText
        Garage_CSV_File = parameters[2].valueAsText
        Garage_Layer_Name = parameters[3].valueAsText
        Campus_GDB = parameters[4].valueAsText
        Selected_Garage_Name = parameters[5].valueAsText
        Buffer_Input = parameters[6].valueAsText

        print("User Input:")
        print("GDBFolder:" + GDB_Folder)
        print("GDB_Name: " + GDB_Name)
        print("Garage_CSV_File" + Garage_CSV_File)
        print("Garage_layer_Name: " + Garage_Layer_Name)
        print("Campus_GDB: " + Campus_GDB)
        print("Selected_Garage_Name: " + Selected_Garage_Name)
        print("Buffer_Radius: " + Buffer_Radius)

        #create gdb
        arcpy.management.CreateFileGDB(GDB_Folder, GDB_Name)
        GDB_Full_Path = GDB_Folder + '/' + GDB_Name 

        #import garage csv
        garages = arcpy.management.MakeXYEventLayer(Garage_CSV_File, 'X', 'Y', Garage_Layer_Name)
        arcpy.FeatureClassToGeodatabase_conversion(garages, GDB_Full_Path)

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
            Buffer_Radius = Buffer_Input + "meters"
            garage_buff_name = "/building_buffed"
            arcpy.analysis.Buffer(garage_feature, garage_buff_name, Buffer_Radius)

            #clip
            structures = Campus_GDB + "/Structures"
            garage_clip_name = "/building_clipped"
            arcpy.analysis.Clip(structures, garage_buff_name, garage_clip_name)

            arcpy.management.CopyFeatures(selected_garage_layer_name, os.path.join(GDB_Full_Path, 'garage_selected'))
            arcpy.management.CopyFeatures(garage_buff_name, os.path.join(GDB_Full_Path, 'building_buffed'))
            arcpy.management.CopyFeatures(garage_clip_name, os.path.join(GDB_Full_Path, 'garage_clipped'))

            arcpy.AddMessage("Success")
        else:
            arcpy.AddError("Seems we couldn't find the building name you entered")

        return
