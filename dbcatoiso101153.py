import sys
import os
import glob
#import xml.dom.minidom
from lxml import etree as ET

def convert_xml_file(source, xslt_file, dest_dir):
    source_tree = ET.parse(source)
    xsl_tree = ET.parse(xslt_file)
    transform = ET.XSLT(xsl_tree)
    result = transform(source_tree)
    txt = ET.tostring(result, pretty_print=True)

    id = source_tree.xpath("/metadata/mdFileID")[0].text.strip("{}")
    output_path = os.path.join(dest_dir, "{}.xml".format(id)) 

    with open(output_path, "w") as out_file:
        out_file.write(txt.decode())

def convert_xml_dir(dir_path, xslt, dest_dir):
    for file_path in glob.glob(dir_path):
        convert_xml_file(file_path, xslt, dest_dir)

if __name__ == "__main__":
    #convert_xml_file("input/dbca/apiary-dbca.xml", "dbcatoiso191153.xslt", "output/dbca")
    convert_xml_dir("input/dbca/*.xml", "dbcatoiso191153.xslt", "output/dbca")


