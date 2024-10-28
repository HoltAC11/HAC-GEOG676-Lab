# Holt Chambers - GEOG 676 - Lab 3
import os
import geopandas as gpd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'Lab3') 

class CensusTract:
    def __init__(self, geoid, population, geometry):
        self.geoid = geoid
        self.population = population
        self.geometry = geometry
    
    def calculate_population_density(self):
        # calculate the population density based on geometry
        ### >>>>>>>>>>>> YOUR CODE HERE <<<<<<<<<<< ###
        pop_temp = gdf['Pop']  # population
        geometry_temp = gdf.to_crs(epsg=3081)  # Convert the CRS to the Texas State Mapping System so it's in a projected CRS
        area_temp = geometry_temp.area / 10**6  # Covert the area to be in square kilometers
        population_density = pop_temp / area_temp  # calculate the population density based on the geometry
        return population_density
        ### <<<<<<<<<<< END OF YOUR CODE <<<<<<<<<<< ###

if __name__ == "__main__":
    # read data
    file_path = os.path.join(DATA_DIR, 'data.geojson')
    # load data into GeoDataFrame
    gdf = gpd.read_file(file_path)
    # preview data
    print(gdf.head(10))  # view the first 10 rows of data
    print(gdf.columns)
    print(gdf.shape)
    print(gdf.dtypes)

    ### >>>>>>>>>>>> YOUR CODE HERE <<<<<<<<<<< ###
    # instantiate the CensusTract class
    CT_temp = CensusTract(geoid = gdf['GeoId'], population = gdf['Pop'], geometry = gdf['geometry'])

    # calculate the population density for each census tract
    for index,row in gdf.iterrows():  # loop through the data set
        CT_temp  # pull in the variables for each row of a data using the CT_Temp class
        pop_density_temp = CT_temp.calculate_population_density()  # usse the pop. density function to calculate for each row
        gdf = gdf.assign(Pop_Den_new = pop_density_temp)  # create the pop. density column ('Pop_Den_new') and assign the values for each row

    ### <<<<<<<<<<< END OF YOUR CODE <<<<<<<<<<< ###

    # preview the first 10 data rows again with the new column
    print(gdf.head(10))
    