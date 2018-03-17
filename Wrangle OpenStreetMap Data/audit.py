import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE_sample = "map.osm"
street_type_re = re.compile(r'\b\S+\.?', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", "Way", "Trail", "Parkway", "Commons", "Circle", "Terrace", "Highway"]

mapping = { "St": "Street",
            "St.": "Street",
            "street": "Street",
            "Ave": "Avenue",
            "Ave.": "Avenue",
            "Blvd": "Boulevard",
            "Blvd.": "Boulevard",
            "Boulavard": "Boulevard",
            "Rd": "Road",
            "Rd.": "Road",
            "RD": "Road",
            "Pl": "Place",
            "Pl.": "Place",
            "PKWY": "Parkway",
            "Pkwy": "Parkway",
            "Ln": "Lane",
            "Ln.": "Lane",
            "Dr": "Drive",
            "Dr.": "Drive"
            }


def audit_street_type(street_types, street_name):
    """audits street type"""
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):

    """returns True if element is street name"""
    return (elem.attrib['k'] == "addr:street" or elem.attrib['k'] == "exit_to")


def audit(osmfile):
    """audits osmfile for street and key type info, and returns street types"""
    osm_file = open(osmfile,encoding="utf8")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types

def is_zip_code(elem):
    return (elem.attrib['k'] == "addr:postcode")

def audit_zip(osmfile):
    osm_file = open(osmfile, encoding="utf8")
    prob_zip = set()
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_zip_code(tag):

                    if len(tag.attrib['v']) != 5:
                        prob_zip.add(tag.attrib['v'])
                    elif tag.attrib['v'][0:2] != '96':
                        prob_zip.add(tag.attrib['v'])
    osm_file.close()
    return prob_zip

print ("Zip codes with possibilty of an error:")
print ("\n")
print (audit_zip(OSMFILE_sample))

street_name = audit(OSMFILE_sample)
pprint.pprint(street_name)

