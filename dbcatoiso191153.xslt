<?xml version="1.0"?>
<!-- 
    Converts metadata from the DBCA schema to ISO 19115-3:2018.
    Basic template from https://github.com/metadata101/iso19115-3.2018/blob/master/src/main/plugin/iso19115-3.2018/templates/geodata.xml
    Conversion makes the following assumptions:
        1. The DBCA data is 2D so the output uses 0 for minimum and maximum values for the vertical extent.
        2. If the DBCA data omits a demoninator value for the equivalent scale then the output will use a value of 0.
-->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xmlns:cit="http://standards.iso.org/iso/19115/-3/cit/2.0"
                xmlns:gex="http://standards.iso.org/iso/19115/-3/gex/1.0"
                xmlns:lan="http://standards.iso.org/iso/19115/-3/lan/1.0"
                xmlns:mcc="http://standards.iso.org/iso/19115/-3/mcc/1.0"
                xmlns:mco="http://standards.iso.org/iso/19115/-3/mco/1.0"
                xmlns:mdb="http://standards.iso.org/iso/19115/-3/mdb/2.0"
                xmlns:mmi="http://standards.iso.org/iso/19115/-3/mmi/1.0"
                xmlns:mrd="http://standards.iso.org/iso/19115/-3/mrd/1.0"
                xmlns:mri="http://standards.iso.org/iso/19115/-3/mri/1.0"
                xmlns:mrl="http://standards.iso.org/iso/19115/-3/mrl/2.0"
                xmlns:mrs="http://standards.iso.org/iso/19115/-3/mrs/1.0"
                xmlns:mrc="http://standards.iso.org/iso/19115/-3/mrc/2.0"
                xmlns:gco="http://standards.iso.org/iso/19115/-3/gco/1.0"
                xmlns:cat="http://standards.iso.org/iso/19115/-3/cat/1.0"
                xmlns:gfc="http://standards.iso.org/iso/19110/gfc/1.1"
                xmlns:gml="http://www.opengis.net/gml/3.2"
                xsi:schemaLocation="http://standards.iso.org/iso/19115/-3/mdb/2.0 http://standards.iso.org/iso/19115/-3/mdb/2.0/mdb.xsd http://standards.iso.org/iso/19110/gfc/1.1 https://standards.iso.org/iso/19110/gfc/1.1/featureCatalogue.xsd http://standards.iso.org/iso/19115/-3/cit/2.0 https://standards.iso.org/iso/19115/-3/cit/2.0/citation.xsd http://standards.iso.org/iso/19115/-3/gex/1.0 https://standards.iso.org/iso/19115/-3/gex/1.0/extent.xsd http://standards.iso.org/iso/19115/-3/mcc/1.0 https://standards.iso.org/iso/19115/-3/mcc/1.0/mcc.xsd http://standards.iso.org/iso/19115/-3/mmi/1.0 https://standards.iso.org/iso/19115/-3/mmi/1.0/maintenance.xsd http://standards.iso.org/iso/19115/-3/mri/1.0 https://standards.iso.org/iso/19115/-3/mri/1.0/identification.xsd http://standards.iso.org/iso/19115/-3/gco/1.0 https://standards.iso.org/iso/19115/-3/gco/1.0/baseTypes2014.xsd "
                version="1.0"
                >
    <xsl:template match="/">
        <mdb:MD_Metadata>
            <mdb:metadataIdentifier>
                <mcc:MD_Identifier>
                    <mcc:code>
                        <gco:CharacterString><xsl:value-of select="translate(/metadata/mdFileID,'{}', '')"/></gco:CharacterString>
                    </mcc:code>
                    <mcc:codeSpace>
                        <gco:CharacterString>urn:uuid</gco:CharacterString>
                    </mcc:codeSpace>
                </mcc:MD_Identifier>
            </mdb:metadataIdentifier>
            <xsl:choose>
                <xsl:when test="/metadata/dataIdInfo/idCitation/citRespPartyx">
                    <xsl:for-each select="/metadata/dataIdInfo/idCitation/citRespParty">
                        <mdb:contact>
                            <cit:CI_Responsibility>
                            <cit:role>
                                <cit:CI_RoleCode codeList="http://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#CI_RoleCode" codeListValue="author"/>
                            </cit:role>
                            <cit:party>
                                <cit:CI_Individual>
                                <cit:name>
                                    <gco:CharacterString><xsl:value-of select="rpIndName"/></gco:CharacterString>
                                </cit:name>
                                <cit:contactInfo>
                                    <cit:CI_Contact>
                                    <cit:address>
                                        <cit:CI_Address>
                                        <cit:electronicMailAddress>
                                            <gco:CharacterString><xsl:value-of select="rpCntInfo/cntAddress/eMailAdd"/></gco:CharacterString>
                                        </cit:electronicMailAddress>
                                        </cit:CI_Address>
                                    </cit:address>
                                    </cit:CI_Contact>
                                </cit:contactInfo>
                                </cit:CI_Individual>
                            </cit:party>
                            </cit:CI_Responsibility>
                        </mdb:contact>
                    </xsl:for-each>
                </xsl:when>
                <xsl:otherwise>
                    <mdb:contact gco:nilReason="missing">
                    </mdb:contact>
                </xsl:otherwise>
            </xsl:choose>
            <mdb:dateInfo>
                <cit:CI_Date>
                    <xsl:choose>
                        <xsl:when test="/metadata/dataIdInfo/idCitation/date/pubDate">
                            <cit:date>
                                <gco:DateTime><xsl:value-of select="/metadata/dataIdInfo/idCitation/date/pubDate"/></gco:DateTime>
                            </cit:date>
                        </xsl:when>
                        <xsl:otherwise>
                            <cit:date gco:nilReason="missing"/>
                        </xsl:otherwise>
                    </xsl:choose>
                    <cit:dateType>
                        <cit:CI_DateTypeCode codeList="http://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#CI_DateTypeCode" codeListValue="publication"/>
                    </cit:dateType>
                </cit:CI_Date>
            </mdb:dateInfo>
            <mdb:dateInfo>
                <cit:CI_Date>
                    <xsl:choose>
                        <xsl:when test="/metadata/dataIdInfo/idCitation/date/reviseDate">
                            <cit:date>
                                <gco:DateTime><xsl:value-of select="/metadata/dataIdInfo/idCitation/date/reviseDate"/></gco:DateTime>
                            </cit:date>
                        </xsl:when>
                        <xsl:otherwise>
                            <cit:date gco:nilReason="missing"/>
                        </xsl:otherwise>
                    </xsl:choose>
                <cit:dateType>
                        <cit:CI_DateTypeCode codeList="http://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#CI_DateTypeCode" codeListValue="lastUpdate"/>
                    </cit:dateType>
                </cit:CI_Date>
            </mdb:dateInfo>
            <mdb:identificationInfo>
                <mri:MD_DataIdentification>
                    <mri:citation>
                        <cit:CI_Citation>
                            <xsl:choose>
                                <xsl:when test="/metadata/dataIdInfo/idCitation/resTitle">
                                    <cit:title>
                                        <gco:CharacterString><xsl:value-of select="/metadata/dataIdInfo/idCitation/resTitle"/></gco:CharacterString>
                                    </cit:title>
                                </xsl:when>
                                <xsl:otherwise>
                                    <cit:title gco:nilReason="missing"/>
                                </xsl:otherwise>
                            </xsl:choose>
                            <xsl:choose>
                                <xsl:when test="/metadata/dataIdInfo/idCitation/resAltTitle">
                                    <cit:alternateTitle>
                                        <gco:CharacterString><xsl:value-of select="/metadata/dataIdInfo/idCitation/resAltTitle"/></gco:CharacterString>
                                    </cit:alternateTitle>
                                </xsl:when>
                                <xsl:otherwise>
                                    <cit:alternateTitle gco:nilReason="missing"/>
                                </xsl:otherwise>
                            </xsl:choose>
                        </cit:CI_Citation>
                    </mri:citation>
                    <xsl:choose>
                        <xsl:when test="/metadata/dataIdInfo/idAbs">
                            <mri:abstract>
                                <gco:CharacterString><xsl:value-of select="/metadata/dataIdInfo/idAbs"/></gco:CharacterString>
                            </mri:abstract>
                        </xsl:when>
                        <xsl:otherwise>
                            <mri:abstract gco:nilReason="missing"/>
                        </xsl:otherwise>
                    </xsl:choose>
                    <xsl:choose>
                        <xsl:when test="/metadata/dataIdInfo/idCredit">
                            <mri:credit>
                                <gco:CharacterString><xsl:value-of select="/metadata/dataIdInfo/idCredit"/></gco:CharacterString>
                            </mri:credit>
                        </xsl:when>
                        <xsl:otherwise>
                            <mri:credit gco:nilReason="missing"/>
                        </xsl:otherwise>
                    </xsl:choose>
                    <mri:resourceMaintenance>
                        <mmi:MD_MaintenanceInformation>
                            <xsl:choose>
                                <xsl:when test="/metadata/dataIdInfo/resMaint/maintFreq/MaintFreqCd/@value[. = '001']">
                                    <mmi:maintenanceAndUpdateFrequency>
                                        <mmi:MD_MaintenanceFrequencyCode codeList="http://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#MD_MaintenanceFrequencyCode" codeListValue="continual"/>
                                    </mmi:maintenanceAndUpdateFrequency>
                                </xsl:when>
                                <xsl:when test="/metadata/dataIdInfo/resMaint/maintFreq/MaintFreqCd/@value[. = '002']">
                                    <mmi:maintenanceAndUpdateFrequency>
                                        <mmi:MD_MaintenanceFrequencyCode codeList="http://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#MD_MaintenanceFrequencyCode" codeListValue="daily"/>
                                    </mmi:maintenanceAndUpdateFrequency>
                                </xsl:when>
                                <xsl:when test="/metadata/dataIdInfo/resMaint/maintFreq/MaintFreqCd/@value[. = '003']">
                                    <mmi:maintenanceAndUpdateFrequency>
                                        <mmi:MD_MaintenanceFrequencyCode codeList="http://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#MD_MaintenanceFrequencyCode" codeListValue="weekly"/>
                                    </mmi:maintenanceAndUpdateFrequency>
                                </xsl:when>
                                <xsl:when test="/metadata/dataIdInfo/resMaint/maintFreq/MaintFreqCd/@value[. = '004']">
                                    <mmi:maintenanceAndUpdateFrequency>
                                        <mmi:MD_MaintenanceFrequencyCode codeList="http://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#MD_MaintenanceFrequencyCode" codeListValue="fortnightly"/>
                                    </mmi:maintenanceAndUpdateFrequency>
                                </xsl:when>
                                <xsl:when test="/metadata/dataIdInfo/resMaint/maintFreq/MaintFreqCd/@value[. = '005']">
                                    <mmi:maintenanceAndUpdateFrequency>
                                        <mmi:MD_MaintenanceFrequencyCode codeList="http://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#MD_MaintenanceFrequencyCode" codeListValue="monthly"/>
                                    </mmi:maintenanceAndUpdateFrequency>
                                </xsl:when>
                                <xsl:when test="/metadata/dataIdInfo/resMaint/maintFreq/MaintFreqCd/@value[. = '006']">
                                    <mmi:maintenanceAndUpdateFrequency>
                                        <mmi:MD_MaintenanceFrequencyCode codeList="http://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#MD_MaintenanceFrequencyCode" codeListValue="quarterly"/>
                                    </mmi:maintenanceAndUpdateFrequency>
                                </xsl:when>
                                <xsl:when test="/metadata/dataIdInfo/resMaint/maintFreq/MaintFreqCd/@value[. = '007']">
                                    <mmi:maintenanceAndUpdateFrequency>
                                        <mmi:MD_MaintenanceFrequencyCode codeList="http://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#MD_MaintenanceFrequencyCode" codeListValue="biannually"/>
                                    </mmi:maintenanceAndUpdateFrequency>
                                </xsl:when>
                                <xsl:when test="/metadata/dataIdInfo/resMaint/maintFreq/MaintFreqCd/@value[. = '008']">
                                    <mmi:maintenanceAndUpdateFrequency>
                                        <mmi:MD_MaintenanceFrequencyCode codeList="http://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#MD_MaintenanceFrequencyCode" codeListValue="annually"/>
                                    </mmi:maintenanceAndUpdateFrequency>
                                </xsl:when>
                                <xsl:when test="/metadata/dataIdInfo/resMaint/maintFreq/MaintFreqCd/@value[. = '009']">
                                    <mmi:maintenanceAndUpdateFrequency>
                                        <mmi:MD_MaintenanceFrequencyCode codeList="http://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#MD_MaintenanceFrequencyCode" codeListValue="asNeeded"/>
                                    </mmi:maintenanceAndUpdateFrequency>
                                </xsl:when>
                                <xsl:when test="/metadata/dataIdInfo/resMaint/maintFreq/MaintFreqCd/@value[. = '010']">
                                    <mmi:maintenanceAndUpdateFrequency>
                                        <mmi:MD_MaintenanceFrequencyCode codeList="http://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#MD_MaintenanceFrequencyCode" codeListValue="irregular"/>
                                    </mmi:maintenanceAndUpdateFrequency>
                                </xsl:when>
                                <xsl:when test="/metadata/dataIdInfo/resMaint/maintFreq/MaintFreqCd/@value[. = '011']">
                                    <mmi:maintenanceAndUpdateFrequency>
                                        <mmi:MD_MaintenanceFrequencyCode codeList="http://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#MD_MaintenanceFrequencyCode" codeListValue="notPlanned"/>
                                    </mmi:maintenanceAndUpdateFrequency>
                                </xsl:when>
                                <xsl:when test="/metadata/dataIdInfo/resMaint/maintFreq/MaintFreqCd/@value[. = '012']">
                                    <mmi:maintenanceAndUpdateFrequency>
                                        <mmi:MD_MaintenanceFrequencyCode codeList="http://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#MD_MaintenanceFrequencyCode" codeListValue="unknown"/>
                                    </mmi:maintenanceAndUpdateFrequency>
                                </xsl:when>
                                <xsl:otherwise>
                                    <mmi:maintenanceAndUpdateFrequency gco:nilReason="missing"/>
                                </xsl:otherwise>
                            </xsl:choose>
                        </mmi:MD_MaintenanceInformation>
                    </mri:resourceMaintenance>
                    <xsl:choose>
                        <xsl:when test="/metadata/dataIdInfo/searchKeys/keyword">
                            <mri:descriptiveKeywords>
                                <mri:MD_Keywords>
                                    <xsl:for-each select="/metadata/dataIdInfo/searchKeys/keyword">
                                        <mri:keyword>
                                            <gco:CharacterString><xsl:value-of select="."/></gco:CharacterString>
                                        </mri:keyword>
                                    </xsl:for-each>
                                </mri:MD_Keywords>
                            </mri:descriptiveKeywords>
                        </xsl:when>
                        <xsl:otherwise>
                            <mri:descriptiveKeywords gco:nilReason="missing"/>
                        </xsl:otherwise>
                    </xsl:choose>
                </mri:MD_DataIdentification>
            </mdb:identificationInfo>
        </mdb:MD_Metadata>
    </xsl:template>
</xsl:stylesheet>