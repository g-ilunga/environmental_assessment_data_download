#=========================
# Libraries
#========================
# Built-in libraries
import os

# Third-party libraries
import requests
import geopandas as gpd

#======================================================================
# Creating a function to download data from Geoportail de l'urbanisme
#======================================================================
def gpu_data_download(name_selected_municipality, output_folder, response):

    # The process to run if response status is 200
    if response.status_code == 200:
        if response.json()["features"] == []: # If the response content is empty, then there is no PLU/PLUi
           print(f"Aucun PLU/PLUi trouvé pour {name_selected_municipality}. Veuillez consultez www.geoportail-urbanisme.gouv.fr", flush=True)
            
        else: # If the response content is not empty, then there is PLU/PLUi that can fetched
            print(f"Il existe un PLU/PLUi pour {name_selected_municipality}.", flush=True)
            data_gdf = gpd.read_file(response.content) # Constructing a geodataframe from the response content
            gpu_doc_id= data_gdf["gpu_doc_id"].values[0]
            idurba = data_gdf["idurba"].values[0]
            download_url = f"https://www.geoportail-urbanisme.gouv.fr/api/document/{gpu_doc_id}/download/{idurba}.zip"
            
            # Downloading the data
            print(f"Le téléchargement du PLU/PLUi de {name_selected_municipality} est en cours...  ", flush=True)
            response = requests.get(download_url)
            output_file = f"{output_folder}{name_selected_municipality}_urbanisme.zip"
            with open(output_file, 'wb') as f:
                f.write(response.content)
            print(f"Fin du téléchargement. Le fichier est enregistré comme: {name_selected_municipality}_urbanisme.zip", flush=True)
    
    # The process to run if response status is not 200
    elif response.status_code != 200:
        print(response.status_code, flush=True)


#=============================================================================
# Creating a function to download the other dataset hosted by IGN Geoservices
#=============================================================================
def data_download(name_selected_municipality, item, output_folder, response):
    
    # The process to run if response status is 200
    if response.status_code == 200:
        if response.json()["features"] == []: # If the response content is empty, then there is no data for that municipality
            print(f"Il n'existe pas de données {item} pour la commune de {name_selected_municipality}.")

        else: # If the response content is not empty, there is data that can fetched
            print (f"Il existe des données {item} pour la commune de {name_selected_municipality}. Téléchargement en cours...")
            data_gdf = gpd.read_file(response.content) # Constructing a geodataframe from the response content

            os.makedirs(f"{output_folder}{item}", exist_ok=True) # Creating a folder to store data
            data_gdf.to_file(f"{output_folder}{item}/{item}.shp")
            print("Téléchargement terminé")

    # The process to run if response status is not 200
    elif response.status_code != 200:
        print(f"Received error {response.status_code} for the dataset {item}", flush=True)
