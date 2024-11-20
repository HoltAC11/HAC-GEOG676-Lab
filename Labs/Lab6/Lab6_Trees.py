import arcpy

PROJ_PATH = r"C:\Users\holtc\HAC-GEOG676-Lab\Labs\Lab6\Lab6Project\Lab6Project.aprx"

project = arcpy.mp.ArcGISProject(PROJ_PATH)

map_obj = project.listMaps('Map')[0]

for layer in map_obj.listLayers():
    if layer.isFeatureLayer:
        symbology = layer.symbology
        if hasattr(symbology, 'renderer') and layer.name == "Trees":
            symbology.updateRenderer('GraduatedColorsRenderer')
            symbology.renderer.classificationField = "Shape_Area"
            symbology.renderer.breakCount = 5
            symbology.renderer.colorRamp = project.listColorRamps('Oranges (5 Classes)')[0]
            layer.symbology = symbology
        elif not hasattr(symbology, 'renderer') and layer.name == "Trees":
            print('No desired feature class...')

project.saveACopy(r'C:\Users\holtc\HAC-GEOG676-Lab\Labs\Lab6\Lab6Project\Lab6Project_trees.aprx')
