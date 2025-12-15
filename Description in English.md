## Context

<p><strong>Note: This tool is built in accordance with the environmental assessment procedure in France.</strong></p>

When conducting an environmental assessment, one of the major steps is data acquisition. The data acquisition step usually involves retrieving data from various public platform such as Geoportail, Géoportail de l'urbanisme or Georisques. This step can be time consumming as you need to retrieve data from many platforms especially if you are only concerned about running a quick diagnosis. Luckily, IGN, the French National Geographic Institute which the reference for geographic data in France, has developped a couple of API to allowed experienced users to access public data and realise advanced manipulation not always available in the aformentionned platforms. 

It is from that observation that the idea to optimise to create a tool that will optimise the data acquisition step in environmental assessment procedures. The present tool has two modules:
* The data download module
* The rapid environmental assessment tool

## Data download module

This module allows to download data that are frequently used during environmental assessment projects. As a result, the expert does not have to browse through various platforms to retrieve data. 
The tool functions as follow: The user indicates the city where the project is located and the tool will download all the data that exist for that specific city. The downloaded data can be then manipulated in a GIS software like QGIS or ArcGIS.
To date, the tool allows to download the following data:
* ZNIEFF
* Sites Natura 2000
* Parcs Naturels Régionaux
* Parcs Naturels Marins
* Parcs Nationaux
* Servitudes (sites inscrits/classés, monuments historiques, etc.)
* PLU et PLUi


## Rapid environmental assessment module

This module allows the user to carry out a rapid environmental assessment using the data commonly used for such task. 
The module works as follow: the user import the area of interest and the tool will identify all the environmental challenges to look out for.
To date, the tool takes into account the following data:
* ZNIEFF
* Sites Natura 2000
* Parcs Naturels Régionaux
* Parcs Naturels Marins
* Parcs Nationaux
* Servitudes (sites inscrits/classés, monuments historiques, etc.)
* The tool also allows to identify urban zoning defined in urban planning documents such as PLU/PLUi. It does not allow yet to determine if the project is located within a "emplacement réservé", "espace boisé classé", or intersect an "alignement d'arbres", etc.


## Perspectives
This is an early prototype. Upcoming improvements includes developping a user interface. Only data available through IGN WFS API are currently supported. Additional data will be progressively added.
