import arcpy

PROJ_PATH = r'C:\Users\holtc\HAC-GEOG676-Lab\Labs\Lab6\Lab6Project\Lab6Project.aprx'

project = arcpy.mp.ArcGISProject(PROJ_PATH)

map_obj = project.listMaps('Map')[0]

for layer in map_obj.listLayers():
    print(layer)
    if layer.isFeatureLayer:
        symbology = layer.symbology
        if hasattr(symbology, 'renderer') and layer.name == "Structures":
            symbology.updateRenderer('UniqueValueRenderer')
            symbology.renderer.fields= ["Type"]
            layer.symbology = symbology
        elif not hasattr(symbology, 'renderer') and layer.name == "Structures":
            print('No desired feature class...')

project.saveACopy(r'C:\Users\holtc\HAC-GEOG676-Lab\Labs\Lab6\Lab6Project\Lab6Project_structures.aprx')
