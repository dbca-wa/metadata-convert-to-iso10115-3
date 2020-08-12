import urllib.request, json
from lxml.builder import ElementMaker
from lxml import etree
from collections import defaultdict
from io import StringIO


misses = {}
hit = {}

def tally (data, name, id):
    if name in data:
        data[name].append(id)
    else:
        data[name] = [data]

def ckan_dataset_to_19115(dataset):
    nsmap={
        "mdb": "http://standards.iso.org/iso/19115/-3/mdb/2.0",
        "gfc": "http://standards.iso.org/iso/19110/gfc/1.1",
        "cit": "http://standards.iso.org/iso/19115/-3/cit/2.0",
        "gex": "http://standards.iso.org/iso/19115/-3/gex/1.0",
        "lan": "http://standards.iso.org/iso/19115/-3/lan/1.0",
        "mcc": "http://standards.iso.org/iso/19115/-3/mcc/1.0",
        "mco": "http://standards.iso.org/iso/19115/-3/mco/1.0",
        "mmi": "http://standards.iso.org/iso/19115/-3/mmi/1.0",
        "mrc": "http://standards.iso.org/iso/19115/-3/mrc/2.0",
        "mrd": "http://standards.iso.org/iso/19115/-3/mrd/1.0",
        "mri": "http://standards.iso.org/iso/19115/-3/mri/1.0",
        "mrl": "http://standards.iso.org/iso/19115/-3/mrl/2.0",
        "mrs": "http://standards.iso.org/iso/19115/-3/mrs/1.0",
        "gco": "http://standards.iso.org/iso/19115/-3/gco/1.0",
        "gml": "http://www.opengis.net/gml/3.2",
        "xlink": "http://www.w3.org/1999/xlink",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance"
    }
    xsdmap = {
        "mdb": "http://standards.iso.org/iso/19115/-3/mdb/2.0/mdb.xsd",
        "gfc": "https://standards.iso.org/iso/19110/gfc/1.1/featureCatalogue.xsd",
        "cit": "https://standards.iso.org/iso/19115/-3/cit/2.0/citation.xsd",
        "gex": "https://standards.iso.org/iso/19115/-3/gex/1.0/extent.xsd",
        "mcc": "https://standards.iso.org/iso/19115/-3/mcc/1.0/mcc.xsd",
        "mmi": "https://standards.iso.org/iso/19115/-3/mmi/1.0/maintenance.xsd",
        "mri": "https://standards.iso.org/iso/19115/-3/mri/1.0/identification.xsd",
        "gco": "https://standards.iso.org/iso/19115/-3/gco/1.0/baseTypes2014.xsd",

        "gml": "https://standards.iso.org/iso/19136/gml.xsd",
        "gml": "http://schemas.opengis.net/gml/3.2.1/gml.xsd",
    }
    schemaLocations = ""
    for shortname in xsdmap.keys():
        if shortname in nsmap:
            schemaLocations += "{} {} ".format(nsmap[shortname], xsdmap[shortname])
    def n(key):
        namespace, key = key.split(":")
        return "{{{}}}{}".format(nsmap[namespace], key)

    def na(key, value):
        return {n(key):value}
    
    def ds(full_key, default=""):
        global misses, hit
        keys = full_key.split(".")
        data = dataset
        while len(keys) > 0:
            key = keys[0]
            if key in dataset:
                data = data[key]
                keys = keys[1:]
            else:
                tally(misses, full_key, dataset["id"])
                return default
        if data == "":
            tally(misses, full_key, dataset["id"])
            return default
        else:
            tally(hit, key, dataset["id"])
            return data

    def pointstrings_to_bounds(pointstrings):
        if len(pointstrings) > 0 and type(pointstrings[0]) is list:
            west = 180
            east = -180
            south = 90
            north = -90
            for substring in pointstrings:
                west1, east1, south1, north1 = pointstrings_to_bounds(substring)
                west = min(west, west1)
                east = max(east, east1)
                south = min(south, south1)
                north = max(north, north1)
            return west, east, south, north
        if len(pointstrings) == 2:
            return pointstrings[0], pointstrings[0], pointstrings[1], pointstrings[1]
        print("should not hit")

    def find_bounds():
        spatial = ds("spatial", None)
        if spatial is None:
            return None
        coords = json.load(StringIO(dataset["spatial"]))["coordinates"]
        return pointstrings_to_bounds(coords)

    def cit_data(value):
        if value is None:
            return E(n("cit:date"), na("gco:nilReason", "missing"))
        else:
            return E(n("cit:date"), 
                E(n("gco:Date"), value)
            )

    def cit_alternateTitle(value):
        if value is None:
            return  E(n("mri:descriptiveKeywords"), na("gco:nilReason", "missing"))
        else:
            return E(n("cit:alternateTitle"),
                E(n("gco:CharacterString"), value)
            )

    def mri_abstract(value):
        if value is None:
            return  E(n("mri:abstract"), na("gco:nilReason", "missing"))
        else:
            return E(n("mri:abstract"),
                E(n("gco:CharacterString"), value)
            )

    def mri_credit(value):
        if value is None:
            return  E(n("mri:credit"), na("gco:nilReason", "missing"))
        else:
            return E(n("mri:credit"),
                E(n("gco:CharacterString"), value)
            )

    def gex_geographicElement():
        bounds = find_bounds()
        if bounds is None:
            return E(n("gex:geographicElement"), na("gco:nilReason", "missing"))
        else:
            (west, east, south, north) = bounds
            return E(n("gex:geographicElement"),
                E(n("gex:EX_GeographicBoundingBox"),
                    E(n("gex:westBoundLongitude"),
                        E(n("gco:Decimal"), str(west)),
                    ),
                    E(n("gex:eastBoundLongitude"),
                        E(n("gco:Decimal"), str(east)),
                    ),
                    E(n("gex:southBoundLatitude"),
                        E(n("gco:Decimal"), str(south)),
                    ),
                    E(n("gex:northBoundLatitude"),
                        E(n("gco:Decimal"), str(north)),
                    ),
                )
            )

    def mmi_maintenanceAndUpdateFrequency(value):
        code_values = ["continual", "daily", "weekly", "fortnightly", "monthly", "quarterly", "biannually", "annually", "asNeeded", "irregular", "notPlanned", "unknown"]
        remap = {
            "infrequent": "irregular",
            "static": "notPlanned",
            "frequent": "continual",
            "yearly": "annually",
        }
        if value in remap:
            value = remap[value]
        if value not in code_values:
            return  E(n("mmi:maintenanceAndUpdateFrequency"), na("gco:nilReason", "missing"))
        else:
            return E(n("mmi:maintenanceAndUpdateFrequency"),
                E(n("mmi:MD_MaintenanceFrequencyCode"), {"codeList":"http://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#MD_MaintenanceFrequencyCode", "codeListValue":value})
            )

    def mri_descriptiveKeywords(values):
        if values is None:
            return  E(n("mri:descriptiveKeywords"), na("gco:nilReason", "missing"))
        else:
            descriptiveKeywords_element = E(n("mri:descriptiveKeywords"))
            keywords_element = E(n("mri:MD_Keywords"))
            for value in values:
                keyword_element = E(n("mri:keyword"),
                    E(n("gco:CharacterString"), value["name"])
                )
                keywords_element.append(keyword_element)
            descriptiveKeywords_element.append(keywords_element)
            return descriptiveKeywords_element

    E = ElementMaker(namespace=nsmap["mdb"], nsmap=nsmap)
    doc = E("MD_Metadata", na("xsi:schemaLocation", schemaLocations),
        E("metadataIdentifier", 
            E(n("mcc:MD_Identifier"),
                E(n("mcc:code"),
                    E(n("gco:CharacterString"), ds("id"))
                ),
                E(n("mcc:codeSpace"),
                    E(n("gco:CharacterString"), "urn:uuid")
                )
            )
        ),

        # E("defaultLocale", E(n("lan:PT_Locale"),
        #     E(n("lan:language"), E(n("lan:LanguageCode"), {"codeList": "codeListLocation#LanguageCode", "codeListValue":"eng"})),
        #     E(n("lan:characterEncoding"), E(n("lan:MD_CharacterSetCode"), {"codeList": "codeListLocation#MD_CharacterSetCode", "codeListValue": "anyValidURI"}))
        # )),
        # E("metadataScope", 
        #     E("MD_MetadataScope", 
        #         E("resourceScope",
        #             E(n("mcc:MD_ScopeCode"), {"codeList":"https://standards.iso.org/iso/19115/-3/mcc/1.0/codelists.xml#MD_ScopeCode", "codeListValue":"dataset"})
        #         ),
        #     )
        # ),

        E("contact", 
            E(n("cit:CI_Responsibility"), 
                E(n("cit:role"), 
                    E(n("cit:CI_RoleCode"), {"codeList":"http://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#CI_RoleCode", "codeListValue":"author"})
                ),
                E(n("cit:party"),
                    E(n("cit:CI_Individual"),
                        E(n("cit:name"),
                            E(n("gco:CharacterString"), ds("author"))
                        ),
                        E(n("cit:contactInfo"),
                            E(n("cit:CI_Contact"),
                                E(n("cit:address"),
                                    E(n("cit:CI_Address"),
                                        E(n("cit:electronicMailAddress"),
                                            E(n("gco:CharacterString"), ds("author_email"))
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            )
        ),

        E("dateInfo",
            E(n("cit:CI_Date"),
                cit_data(ds("published_on", None)),
                E(n("cit:dateType"),
                    E(n("cit:CI_DateTypeCode"), {"codeList":"http://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#CI_DateTypeCode", "codeListValue":"publication"})
                )
            )
        ), 

        E("dateInfo",   
            E(n("cit:CI_Date"),
                cit_data(ds("last_updated_on", None)),
                E(n("cit:dateType"),
                    E(n("cit:CI_DateTypeCode"), {"codeList":"http://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#CI_DateTypeCode", "codeListValue":"lastUpdate"})
                )
            )
        ),

        # E("metadataStandard", 
        #     E(n("cit:CI_Citation"),
        #         E(n("cit:title"),
        #             E(n("gco:CharacterString"), "ISO 19115-3")
        #         )
        #     )
        # ),
        # E("metadataProfile"),
        # E("alternativeMetadataReference"),
        # E("metadataLinkage"),
        # E("spatialRepresentationInfo"),
        # E("referenceSystemInfo"),
        # E("metadataExtensionInfo"),

        E("identificationInfo",
            E(n("mri:MD_DataIdentification"),
                E(n("mri:citation"),
                    E(n("cit:CI_Citation"),
                        E(n("cit:title"),
                            E(n("gco:CharacterString"), ds("title"))
                        ),
                        cit_alternateTitle(ds("name", None)),
                    )
                ),
                mri_abstract(ds("notes", None)),
                mri_credit(ds("organization.title", None)),
                E(n("mri:extent"),
                    E(n("gex:EX_Extent"),
                        gex_geographicElement(),
                    ),
                ),
                E(n("mri:resourceMaintenance"),
                    E(n("mmi:MD_MaintenanceInformation"),
                        mmi_maintenanceAndUpdateFrequency(ds("update_frequency", None)),
                    )
                ),
                mri_descriptiveKeywords(ds("tags", None)),
            )
        )
    )
    return etree.tostring(doc, pretty_print=True, xml_declaration=True, encoding="UTF-8").decode()

def ckan_url_to_dataset(url):
    response_string = urllib.request.urlopen(url).read()#.decode("utf-8")
    return json.loads(response_string).get("result")

def test_single(id="61a8668c-cde0-4693-8946-df7c43cc7596"):
    ds_url = "https://catalogue.data.wa.gov.au/api/3/action/package_show?id={}".format(id)
    dataset = ckan_url_to_dataset(ds_url)
    xml = ckan_dataset_to_19115(dataset)
    with open("output/ckan/{}.xml".format(dataset["id"]), "w", encoding="UTF-8") as out_file:
        out_file.write(xml)

def test_batch(count=10, shuffle=False, offset=0):
    datasets = ckan_url_to_dataset("https://catalogue.data.wa.gov.au/api/3/action/package_list")
    i = offset
    if shuffle:
        import random
        random.shuffle(datasets)
    for name in datasets[offset:(offset + count)]:
        i += 1
        print(i, name)
        try:
            test_single(name)
        except urllib.error.HTTPError as httperror:
            print("Error loading {}: {}".format(name, httperror))

if __name__ == "__main__":
    #test_batch(shuffle=True)
    test_batch(count=4, shuffle=False, offset=0)
    #test_single("commercial-building-disclosure")

    for field in misses:
        print("misses '{}': {}".format(field, len(misses[field])))
