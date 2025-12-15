""" 
The logic is the following. 
Using a random point from a municipality, we find the corresponding "zonage urbain" from IGN Géoservices WFS.
The "zonage urbain" information comes with the necessary information about the PLU/PLUi in place should one exists.
The PLU/PLUi information will be used to find and download the entire archive from Geoportail de l'urbanisme (GPU).
"""

#==========================
# Libraries
#==========================
import xml.etree.ElementTree as ET


#============================================================================================================================
# Constructing a xml_filter
#============================================================================================================================
def creating_xml_filter(layer_geometry, latitude, longitude):
    
    # Defining namespaces
    namespaces = {
        "fes": "http://www.opengis.net/fes/2.0",
        "gml": "http://www.opengis.net/gml/3.2"
    }

    # Creating the root element <fes:Filter> with namespaces
    filter_elem = ET.Element(ET.QName(namespaces["fes"], "Filter"), nsmap=namespaces)

    # Creating <fes:Intersects> as a child of <fes:Filter>
    intersects_elem = ET.SubElement(filter_elem, ET.QName(namespaces["fes"], "Intersects"))

    # Adding <fes:ValueReference> inside <fes:Intersects>
    value_ref_elem = ET.SubElement(intersects_elem, ET.QName(namespaces["fes"], "ValueReference"))
    value_ref_elem.text = layer_geometry  # set the text content

    # Adding <gml:Point> with srsName attribute
    point_elem = ET.SubElement(intersects_elem, ET.QName(namespaces["gml"], "Point"), 
                            attrib={"srsName": "urn:ogc:def:crs:EPSG::4326"})

    # Adding <gml:pos> inside <gml:Point>
    pos_elem = ET.SubElement(point_elem, ET.QName(namespaces["gml"], "pos"))
    pos_elem.text = f"{latitude} {longitude}"

    # Converting the tree to a string
    xml_filter = ET.tostring(filter_elem, encoding="unicode")
    return xml_filter

#======================================================================================================
# Creating a function to construct the "data" parameter of the POST request
#======================================================================================================

def urban_data_to_post(layer_name, layer_geometry, latitude, longitude):
    
    ''' The function constructs the final xml to be used in the POST request. It integrates the output of the function "creating xml_filter". '''
    
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

    xml_filter = creating_xml_filter(layer_geometry, latitude, longitude) # Retrieving the filter
    xml_filter = ET.fromstring (xml_filter)
    query_elem.append(xml_filter)
    
    # Generating the POST data xml
    data = ET.tostring(get_feature_elem, encoding="utf-8", xml_declaration=True).decode("utf-8")
    return data
