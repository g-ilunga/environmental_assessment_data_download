"""
This xml builder file is necessary to download the other environmental data (listed in the config_dataset_file) from IGN server.
The xml builder is made up of 3 functions that operate as as follow:
1. From the geodataframe of the selected municipality, a list of geographic coordinates of the municipality boundary is generated
2. Using the geographic coordinates, a xml filter is constructed (retrieving environmental layer intersecting the municipality)
3. Using the xml filter, a final xml string is constructed and sent to the IGN server using POST requests
"""

#======================================================================
# Libraries
#======================================================================
import xml.etree.ElementTree as ET
from shapely.geometry import Polygon, MultiPolygon

#==========================================================================================================
# Creating a function that generate the poslist that will be used in the xml filter
#==========================================================================================================
def get_poslists_from_gdf(geodataframe):
    
    """ Extracts poslists (coordinate strings) from polygons in a GeoDataFrame.
        Handles both Polygon and MultiPolygon geometries.
        Returns a list of poslist strings.
    """
    poslists = []

    for _, row in geodataframe.iterrows():
        geom = row.geometry

        if geom is None or geom.is_empty:
            continue

        # Handle MultiPolygon and Polygon
        polygons = [geom] if isinstance(geom, Polygon) else list(geom.geoms)

        for poly in polygons:
            coords = list(poly.exterior.coords)
            poslist = " ".join([f"{y:.6f} {x:.6f}" for x, y in coords])
            poslists.append(poslist)

    return poslists

#=======================================================================================================
# Creating a function that generate the xml filter
#=======================================================================================================
"""
The function creates a WFS 2.0 XML filter string that matches any polygon in the provided poslists using an <fes:Or> filter.
"""

def creating_xml_filter(layer_geometry, geodataframe):
    
    poslists = get_poslists_from_gdf(geodataframe)

    # Namespaces
    namespaces = {
        "fes": "http://www.opengis.net/fes/2.0",
        "gml": "http://www.opengis.net/gml/3.2"
    }

    # Root <fes:Filter>
    filter_elem = ET.Element(ET.QName(namespaces["fes"], "Filter"), nsmap=namespaces)

    # Wrap all intersections inside <fes:Or>
    or_elem = ET.SubElement(filter_elem, ET.QName(namespaces["fes"], "Or"))

    for poslist in poslists:
        # <fes:Intersects>
        intersects_elem = ET.SubElement(or_elem, ET.QName(namespaces["fes"], "Intersects"))

        # <fes:ValueReference>
        value_ref_elem = ET.SubElement(intersects_elem, ET.QName(namespaces["fes"], "ValueReference"))
        value_ref_elem.text = layer_geometry.strip()

        # <gml:Polygon>
        polygon_elem = ET.SubElement(
            intersects_elem,
            ET.QName(namespaces["gml"], "Polygon"),
            attrib={"srsName": "urn:ogc:def:crs:EPSG::4326"}
        )

        # <gml:exterior>
        exterior_elem = ET.SubElement(polygon_elem, ET.QName(namespaces["gml"], "exterior"))

        # <gml:LinearRing>
        linearRing_elem = ET.SubElement(exterior_elem, ET.QName(namespaces["gml"], "LinearRing"))

        # <gml:posList>
        posList_elem = ET.SubElement(linearRing_elem, ET.QName(namespaces["gml"], "posList"))
        posList_elem.text = poslist.strip()

    # Convert to XML string
    xml_filter = ET.tostring(filter_elem, encoding="utf-8", xml_declaration=True).decode("utf-8")

    return xml_filter


#================================================================================================================
# Creating a function to construct the "data" parameter of the POST request
#================================================================================================================

''' The function constructs the final xml to be used in the POST request. It integrates the output of the function "creating xml_filter". '''
def data_to_post(geodataframe, layer_name, layer_geometry):
      
    # Defining namespaces
    ns = {
        "wfs": "http://www.opengis.net/wfs/2.0",
        "fes": "http://www.opengis.net/fes/2.0",
        "gml": "http://www.opengis.net/gml/3.2",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance"
        }
    for prefix, uri in ns.items(): # Registering namespaces so the prefixes appear correctly in the output
        ET.register_namespace(prefix, uri)

    # Root element <wfs:GetFeature>
    get_feature_elem = ET.Element(
        ET.QName(ns["wfs"], "GetFeature"),
        {
            "service": "WFS",
            "version": "2.0.0",
            ET.QName(ns["xsi"], "schemaLocation"):
                "http://www.opengis.net/wfs/2.0 "
                "http://schemas.opengis.net/wfs/2.0/wfs.xsd"
        }
    )

    # Add <wfs:Query> element with attributes and the xml_filter
    query_elem = ET.SubElement(
        get_feature_elem,
        ET.QName(ns["wfs"], "Query"),
        {
            "typeNames": layer_name,
            "srsName": "EPSG:4326"
        }
    )

    xml_filter = creating_xml_filter(layer_geometry, geodataframe) # Retrieving the filter
    xml_filter = ET.fromstring (xml_filter)
    query_elem.append(xml_filter) # Appending the filter to the query xml
    
    # Generating the POST data xml
    data = ET.tostring(get_feature_elem, encoding="utf-8", xml_declaration=True).decode("utf-8")
    return data
