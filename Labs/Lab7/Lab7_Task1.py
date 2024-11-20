# Holt Chambers
# Lab 7 - Task 1
import arcpy

# file paths for DEMs
input_dem = r"C:\Users\holtc\HAC-GEOG676-Lab\Labs\Lab7\Lab 7 Data\DEM\n30_w097_1arc_v3.tif"
output_hillshade = r"C:\Users\holtc\HAC-GEOG676-Lab\Labs\Lab7\Lab 7 Data\DEM\hillshade.tif"
output_slope = r"C:\Users\holtc\HAC-GEOG676-Lab\Labs\Lab7\Lab 7 Data\DEM\slope.tif"

# Hillshade function
arcpy.ddd.HillShade(
    in_raster = input_dem,
    out_raster = output_hillshade,
    azimuth = 315,
    altitude = 45,
    model_shadows = "NO_SHADOWS"
)

# Slope Function
arcpy.ddd.Slope(
    in_raster = input_dem,
    out_raster = output_slope,
)