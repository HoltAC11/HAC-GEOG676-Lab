import arcpy
import time

class Toolbox(object):
    def __init__(self):
        self.label = "Lab6_Toolbox"
        self.alias = "Lab6_Toolbox"
        self.tools = [Lab6_Tool]
    
class Lab6_Tool(object):
    def __init__(self):
        self.label = "Lab6_Tool"
        self.description = "Re-render feature classes"
        self.canRunInBackground = False

    def getParameterInfo(self):
        param0 = arcpy.Parameter(
            displayName="Input Project Path",
            name="inputprojectpath",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param1 = arcpy.Parameter(
            displayName="Feature Class",
            name="featureclass",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param2 = arcpy.Parameter(
            displayName="Output Project Path",
            name="outputprojectpath",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        params = [param0, param1, param2]
        return params
    
    def execute(self, parameters, messages):
        # progressor variable
        ReadTime = 2.5
        start = 0
        max = 100
        step = 25

        #set up the progressor
        arcpy.SetProgressor("step", "Checking building proximity...", start, max, step)
        time.sleep(ReadTime)
        arcpy.AddMessage("Init Tool...")

        # query user input
        Input_Project = parameters[0].valueAsText
        Feature_Class = parameters[1].valueAsText
        Output_Project = parameters[2].valueAsText

        # retrieve the project
        project = arcpy.mp.ArcGISProject(Input_Project)
        campus = project.listMaps('Map')[0]
        layers = campus.listLayers()
        
        if Feature_Class == "Structures": # run the renderer for the "Structures" fc
            for layer in layers:
                if layer.isFeatureLayer:
                    symbology = layer.symbology

                    # Advance progressor bar
                    arcpy.SetProgressorPosition(start + step)
                    arcpy.SetProgressorLabel('Confriming the layer is a feature layer...')
                    time.sleep(ReadTime)
                    arcpy.AddMessage('Confriming the layer is a feature layer...')

                    if hasattr(symbology, 'renderer') and layer.name == "Structures":
                        symbology.updateRenderer('UniqueValueRenderer')
                        symbology.renderer.fields= ["Type"]
                        layer.symbology = symbology

                        # advance the progressor bar
                        arcpy.SetProgressorPosition(start + step)
                        arcpy.SetProgressorLabel('Re-rendering the Structures feature class...')
                        time.sleep(ReadTime)
                        arcpy.AddMessage('Re-rendering the Structures feature class...')
                   
        elif Feature_Class == "Trees": # run the renderer for the "Trees" fc
            for layer in layers:
                if layer.isFeatureLayer:
                    symbology = layer.symbology

                    # Advance progressor bar
                    arcpy.SetProgressorPosition(start + step)
                    arcpy.SetProgressorLabel('Confriming the layer is a feature layer...')
                    time.sleep(ReadTime)
                    arcpy.AddMessage('Confriming the layer is a feature layer...')

                    if hasattr(symbology, 'renderer') and layer.name == "Trees":
                        symbology.updateRenderer('GraduatedColorsRenderer')
                        symbology.renderer.classificationField = "Shape_Area"
                        symbology.renderer.breakCount = 5
                        symbology.renderer.colorRamp = project.listColorRamps('Oranges (5 Classes)')[0]
                        layer.symbology = symbology

                        # advance the progressor bar
                        arcpy.SetProgressorPosition(start + step)
                        arcpy.SetProgressorLabel('Re-rendering the Trees feature class...')
                        time.sleep(ReadTime)
                        arcpy.AddMessage('Re-rendering the Trees feature class...')
        else:
            arcpy.AddError('No desired feature class...')

        project.saveACopy(Output_Project)
        return 