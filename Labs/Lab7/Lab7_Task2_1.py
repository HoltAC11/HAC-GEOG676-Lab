# Holt Chambers
# Lab 7 - Task 2.1
import arcpy

# red, green, and blue bands
red_band_path = r"C:\Users\holtc\HAC-GEOG676-Lab\Labs\Lab7\Lab 7 Data\LandSAT\LT05_L2SP_026039_20110803_20200820_02_T1_SR_B3.tiff"
blue_band_path = r"C:\Users\holtc\HAC-GEOG676-Lab\Labs\Lab7\Lab 7 Data\LandSAT\LT05_L2SP_026039_20110803_20200820_02_T1_SR_B1.tiff"
green_band_path = r"C:\Users\holtc\HAC-GEOG676-Lab\Labs\Lab7\Lab 7 Data\LandSAT\LT05_L2SP_026039_20110803_20200820_02_T1_SR_B2.tiff"

# convert LandSAT dataset into rasters
band_RED = arcpy.sa.Raster(red_band_path)
band_GREEN = arcpy.sa.Raster(green_band_path)
band_BLUE = arcpy.sa.Raster(blue_band_path)

# Composite RGB function
arcpy.management.CompositeBands(
    [band_RED, band_GREEN, band_BLUE],
    r"C:\Users\holtc\HAC-GEOG676-Lab\Labs\Lab7\Lab 7 Data\LandSAT\compbands.tif"
    )