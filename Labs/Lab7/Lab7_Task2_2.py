# Holt Chambers
# Lab 7 - Task 2.2
import arcpy

# red, green, blue, and near infrared bands
red_band_path = r"C:\Users\holtc\HAC-GEOG676-Lab\Labs\Lab7\Lab 7 Data\LandSAT\LT05_L2SP_026039_20110803_20200820_02_T1_SR_B3.tiff"
blue_band_path = r"C:\Users\holtc\HAC-GEOG676-Lab\Labs\Lab7\Lab 7 Data\LandSAT\LT05_L2SP_026039_20110803_20200820_02_T1_SR_B1.tiff"
green_band_path = r"C:\Users\holtc\HAC-GEOG676-Lab\Labs\Lab7\Lab 7 Data\LandSAT\LT05_L2SP_026039_20110803_20200820_02_T1_SR_B2.tiff"
NIR_band_path = r"C:\Users\holtc\HAC-GEOG676-Lab\Labs\Lab7\Lab 7 Data\LandSAT\LT05_L2SP_026039_20110803_20200820_02_T1_SR_B4.tiff"

# convert bands into rasters
band_RED = arcpy.sa.Raster(red_band_path)
band_GREEN = arcpy.sa.Raster(green_band_path)
band_BLUE = arcpy.sa.Raster(blue_band_path)
band_NIR = arcpy.sa.Raster(NIR_band_path)

# NDVI function
band_NDVI = ((band_NIR - band_RED) / (band_NIR + band_RED)) * 100 + 100

# Save NDVI output
band_NDVI.save(r"C:\Users\holtc\HAC-GEOG676-Lab\Labs\Lab7\Lab 7 Data\LandSAT\NDVI.tif")