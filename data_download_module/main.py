#=======================================================================================================
# LIBRARIES
#=======================================================================================================
# Built-in packages
import json
import os

# Third_party packages
import pandas as pd
import geopandas as gpd
import requests
from shapely.geometry import Polygon, MultiPolygon
import xml.etree.ElementTree as ET

# Local modules to download data from geoportail de l'urbanisme
from xml_builder_gpu import urban_data_to_post
from download_functions import gpu_data_download

# Local modules to download the other data hosted by IGN Geoservices
from xml_builder import data_to_post
from download_functions import data_download

#======================================================================================================
# INITIAL CONFIGURATION
#======================================================================================================
# Paths to necessary input file
municipalities_points_file = "C:/Users/ilung/Documents/Portfolio/eia_data_download/download_tool/base_dataset/municipalities_points.csv" # CSV that Contains the lat/lon of each municipality
municipalities_boundary_file = "C:/Users/ilung/Documents/Portfolio/eia_data_download/download_tool/base_dataset/municipalities_boundary.gpkg" # Geographic layer of municipalities
config_urls_file = "config_urls.json" # Contains the urls we need to download data
config_dataset_file = "config_dataset.json" # Contains the name of environmental dataset we want to download

# Loading relevant files
municipalities_points = pd.read_csv(municipalities_points_file)
municipalities_boundary = gpd.read_file(municipalities_boundary_file)
with open(config_urls_file) as f:
    urls_dict = json.load(f)
with open(config_dataset_file) as f:
    dataset_dict = json.load(f)

# Preparing the necessary urls
wfs_url = urls_dict["wfs_url"]

#=======================================================================================================
# USER CONFIGURATION (the configuration that needs to be set by the user)
#=======================================================================================================

# Path to where downloaded data will be saved
output_folder = "C:/Users/ilung/Documents/Portfolio/eia_data_download/output/"

# Selecting the municipality of interest
name_selected_municipality = "TOULON" # This will be a dropdown menu from the municipalities_point

#=======================================================================================================
# DOWNLOADING OTHER DATA FROM IGN GEOSERVICES (listed in the config_dataset_file)
#=======================================================================================================
# The selected municipality geodataframe
selected_municipality_gdf = municipalities_boundary[municipalities_boundary["nom_officiel_en_majuscules"]==name_selected_municipality]

for item in dataset_dict: # Looping over each item of the environmental dataset dictionnary

    # Building and sending the POST request
    layer_name = dataset_dict[item]["layer_name"]  # The name of the environmental layer as per IGN standard
    layer_geometry = dataset_dict[item]["geometry_key"] # The geometry_key of the environmental layer as per IGN standard

    data = data_to_post(selected_municipality_gdf, layer_name, layer_geometry)
    headers = {"Content-Type": "text/xml"}
    params={"outputFormat": "application/json"}

    response = requests.post(wfs_url, headers=headers, data=data, params=params)  # Sending the POST request

    # Data download process
    data_download(name_selected_municipality, item, output_folder, response)

print ("Toutes les données ont été téléchargées")

#===========================================================================================================
# DOWNLOADING DATA FROM GEOPORTAIL DE L'URBANISME
#===========================================================================================================

""" The logic is the following. 
    Using a random point from a municipality, we find the corresponding "zonage urbain" from IGN Géoservices WFS.
    The "zonage urbain" information comes with the necessary information about the PLU/PLUi in place should one exists.
    The PLU/PLUi information will be used to find and download the entire archive from Geoportail de l'urbanisme (GPU).
"""
# The selected municipality dataframe
selected_municipality_df = municipalities_points[municipalities_points["nom_officiel_en_majuscules"]==name_selected_municipality]

# The INSEE code and the EPCI siren
insee_code = selected_municipality_df["code_insee"].values[0]
epci_code = selected_municipality_df["codes_siren_des_epci"].values[0]

# Geographic coordinates of the municipality
latitude = selected_municipality_df["latitude"].values[0]
longitude = selected_municipality_df["longitude"].values[0]

# Information about the "zonage urbain" layer
layer_name = "wfs_du:zone_urba" # The name of the layer as per IGN standard
layer_geometry = "the_geom" # The geometry_key as per IGN standard

# Sending the POST requests
data = urban_data_to_post(layer_name, layer_geometry, latitude, longitude)
headers = {"Content-Type": "text/xml"}
params={"outputFormat": "application/json"}

print(f"Recherche de l'existance d'un PLU/PLUi pour {name_selected_municipality}...")
response = requests.post(wfs_url, headers=headers, data=data, params=params)  # Sending the POST request

# Downloading the PLU/PLUi should one exist
gpu_data_download(name_selected_municipality, output_folder, response)
