import urllib.request, json
from lxml.builder import ElementMaker
from lxml import etree
from collections import defaultdict


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
        "gfc": "http://standards.iso.org/iso/19110/gfc/1.1/gfc.xsd",
        "gml": "http://schemas.opengis.net/gml/3.2.1/gml.xsd"
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
    def ds(key, default=""):
        global misses, hit
        if key in dataset:
            tally(hit, key, dataset["id"])
            return dataset[key]
        else:
            tally(misses, key, dataset["id"])
            #print("miss {}/hit {}: {}, {}".format(missing, hit, dataset["id"], key))
            return default

    def cit_data(value):
        if value is None:
            return E(n("cit:date"), na("gco:nilReason", "missing"))
        else:
            return E(n("cit:date"), 
                E(n("gco:Date"), value)
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
                        )
                    )
                ),
                mri_abstract(ds("notes", None)),
                mri_credit(ds("organization.title", None))
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
    test_batch(count=10, shuffle=True, offset=0)
    #test_single("commercial-building-disclosure")

    for field in misses:
        print("misses '{}': {}".format(field, len(misses[field])))


