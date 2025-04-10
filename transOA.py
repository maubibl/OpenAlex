import json
import xml.etree.ElementTree as ET
import sys
import datetime

def json_to_xml(json_data_list, output_file):
    """
    Convert a list of JSON records to a single XML file with a <modsCollection> root.

    Args:
        json_data_list (list): List of JSON records to convert.
        output_file (str): The path to the output XML file.
    """
   # Define namespaces
    namespaces = {
        "": "http://www.loc.gov/mods/v3",  # Default namespace
        "xlink": "http://www.w3.org/1999/xlink",  # xlink namespace
        "xsi": "http://www.w3.org/2001/XMLSchema-instance"  # xsi namespace
    }
    for prefix, uri in namespaces.items():
        ET.register_namespace(prefix, uri)  # Register namespaces

        # Create the <modsCollection> element with the default namespace
    mods_collection = ET.Element("modsCollection", {
            "xmlns": namespaces[""],  # Default namespace
            "xmlns:xlink": namespaces["xlink"],  # xlink namespace
            "xmlns:xsi": namespaces["xsi"]  # xsi namespace
        })

    # Define a mapping from ISO 639-1 (two-letter) to ISO 639-2/B (three-letter) language codes
    language_code_mapping = {
        "en": "eng",
        "sv": "swe",
        "da": "dan",
        "de": "ger",
        "fr": "fre",
        "es": "spa",
        "it": "ita",
        "zh": "chi",
        "ru": "rus",
        "ja": "jpn",
        "no": "nor",
        "nl": "dut",
        "pt": "por",
        "fi": "fin",
        # Add more mappings as needed
    }

    # Mapping of ISO 3166-1 alpha-2 country codes to country names
    country_code_mapping = {
        "US": "United States",
        "SE": "Sweden",
        "GB": "United Kingdom",
        "DE": "Germany",
        "FR": "France",
        "IT": "Italy",
        "ES": "Spain",
        "CN": "China",
        "JP": "Japan",
        "IN": "India",
        "BR": "Brazil",
        "RU": "Russia",
        "ZA": "South Africa",
        "DK": "Denmark",
        "NO": "Norway",
        "FI": "Finland",
        "NL": "Netherlands",
        "PT": "Portugal",
        "AU": "Australia",
        "CA": "Canada",
        "KR": "South Korea",
        "MX": "Mexico",
        "TR": "Turkey",
        "PL": "Poland",
        "BE": "Belgium",
        "AT": "Austria",
        "CH": "Switzerland",
        "IE": "Ireland",
        "NZ": "New Zealand",
        "HR": "Croatia",
        "CZ": "Czech Republic",
        "HU": "Hungary",
        "CL": "Chile",
        "JO": "Jordan",
        "UA": "Ukraine",
        "GR": "Greece",
        "EE": "Estonia",
        "SA": "Saudi Arabia",
        "MY": "Malaysia",
        "ET": "Ethiopia",
        "SG": "Singapore",
        "BD": "Bangladesh",
        "IR": "Iran"
        # Add more mappings as needed
    }

    # Iterate over each JSON record and create a <mods> element for each
    for json_data in json_data_list:
        mods = ET.SubElement(mods_collection, "mods", {
            "version": "3.7",
            "xsi:schemaLocation": "http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-7.xsd",
        })

        # Add genre elements based on type_crossref
        type_crossref = json_data.get("type_crossref", "")

        if type_crossref == "journal-article":
            ET.SubElement(mods, "genre", {"authority": "diva", "type": "contentTypeCode"}).text = "refereed"
            ET.SubElement(mods, "genre", {"authority": "diva", "type": "publicationTypeCode"}).text = "article"
            ET.SubElement(mods, "genre", {"authority": "svep", "type": "publicationType"}).text = "art"
            ET.SubElement(mods, "genre", {"authority": "diva", "type": "publicationType", "lang": "eng"}).text = "Article in journal"
            ET.SubElement(mods, "genre", {"authority": "kev", "type": "publicationType", "lang": "eng"}).text = "article"
        elif type_crossref == "proceedings-article":
            ET.SubElement(mods, "genre", {"authority": "diva", "type": "contentTypeCode"}).text = "refereed"
            ET.SubElement(mods, "genre", {"authority": "diva", "type": "publicationTypeCode"}).text = "conferencePaper"
            ET.SubElement(mods, "genre", {"authority": "svep", "type": "publicationType"}).text = "kon"
            ET.SubElement(mods, "genre", {"authority": "diva", "type": "publicationType", "lang": "eng"}).text = "Conference paper"
            ET.SubElement(mods, "genre", {"authority": "kev", "type": "publicationType", "lang": "eng"}).text = "proceeding"
            ET.SubElement(mods, "genre", {"authority": "diva", "type": "publicationSubTypeCode"}).text = "publishedPaper"
        elif type_crossref in ["book-chapter", "book-part"]:
            ET.SubElement(mods, "genre", {"authority": "diva", "type": "contentTypeCode"}).text = "science"
            ET.SubElement(mods, "genre", {"authority": "diva", "type": "publicationTypeCode"}).text = "chapter"
            ET.SubElement(mods, "genre", {"authority": "svep", "type": "publicationType"}).text = "kap"
            ET.SubElement(mods, "genre", {"authority": "diva", "type": "publicationType", "lang": "eng"}).text = "Chapter in book"
            ET.SubElement(mods, "genre", {"authority": "kev", "type": "publicationType", "lang": "eng"}).text = "bookitem"
        elif type_crossref in ["book", "monograph", "book-set"]:
            ET.SubElement(mods, "genre", {"authority": "diva", "type": "contentTypeCode"}).text = "science"
            ET.SubElement(mods, "genre", {"authority": "diva", "type": "publicationTypeCode"}).text = "book"
            ET.SubElement(mods, "genre", {"authority": "svep", "type": "publicationType"}).text = "bok"
            ET.SubElement(mods, "genre", {"authority": "diva", "type": "publicationType", "lang": "eng"}).text = "Book"
            ET.SubElement(mods, "genre", {"authority": "kev", "type": "publicationType", "lang": "eng"}).text = "book"
        elif type_crossref == "report":
            ET.SubElement(mods, "genre", {"authority": "diva", "type": "contentTypeCode"}).text = "science"
            ET.SubElement(mods, "genre", {"authority": "diva", "type": "publicationTypeCode"}).text = "report"
            ET.SubElement(mods, "genre", {"authority": "svep", "type": "publicationType"}).text = "rap"
            ET.SubElement(mods, "genre", {"authority": "diva", "type": "publicationType", "lang": "eng"}).text = "Report"
            ET.SubElement(mods, "genre", {"authority": "kev", "type": "publicationType", "lang": "eng"}).text = "book"
        elif type_crossref == "edited-book":
            ET.SubElement(mods, "genre", {"authority": "diva", "type": "contentTypeCode"}).text = "science"
            ET.SubElement(mods, "genre", {"authority": "diva", "type": "publicationTypeCode"}).text = "collection"
            ET.SubElement(mods, "genre", {"authority": "svep", "type": "publicationType"}).text = "sam"
            ET.SubElement(mods, "genre", {"authority": "diva", "type": "publicationType", "lang": "eng"}).text = "Collection (editor)"
            ET.SubElement(mods, "genre", {"authority": "kev", "type": "publicationType", "lang": "eng"}).text = "book"
        elif type_crossref == "posted-content":
            ET.SubElement(mods, "genre", {"authority": "diva", "type": "contentTypeCode"}).text = "science"
            ET.SubElement(mods, "genre", {"authority": "diva", "type": "publicationTypeCode"}).text = "manuscript"
            ET.SubElement(mods, "genre", {"authority": "svep", "type": "publicationType"}).text = "vet"
            ET.SubElement(mods, "genre", {"authority": "diva", "type": "publicationType", "lang": "eng"}).text = "Manuscript (preprint)"
            ET.SubElement(mods, "genre", {"authority": "kev", "type": "publicationType", "lang": "eng"}).text = "preprint"
        else:
            ET.SubElement(mods, "genre", {"authority": "diva", "type": "contentTypeCode"}).text = "science"
            ET.SubElement(mods, "genre", {"authority": "diva", "type": "publicationTypeCode"}).text = "vet"
            ET.SubElement(mods, "genre", {"authority": "svep", "type": "publicationType"}).text = "ovr"
            ET.SubElement(mods, "genre", {"authority": "diva", "type": "publicationType", "lang": "eng"}).text = "Other"

        # Add author information
        authorships = json_data.get("authorships", [])

        for authorship in authorships:
            author = authorship.get("author", {})
            institutions = authorship.get("institutions", [])
            display_name = author.get("display_name", "")
            orcid = author.get("orcid", None)

            # Split the display_name into family and given names
            name_parts = display_name.split()
            family_name = name_parts[-1] if name_parts else ""
            given_name = " ".join(name_parts[:-1]) if len(name_parts) > 1 else ""

            # Create the <name> element
            name_elem = ET.SubElement(mods, "name", {"type": "personal"})
            ET.SubElement(name_elem, "namePart", {"type": "family"}).text = family_name
            ET.SubElement(name_elem, "namePart", {"type": "given"}).text = given_name

            # Add the <role> element
            if type_crossref == "edited-book":
                role_elem = ET.SubElement(name_elem, "role")
                ET.SubElement(role_elem, "roleTerm", {"type": "code", "authority": "marcrelator"}).text = "edt"
            else:
                role_elem = ET.SubElement(name_elem, "role")
                ET.SubElement(role_elem, "roleTerm", {"type": "code", "authority": "marcrelator"}).text = "aut"

            # Add the <affiliation> element
            affiliations = []
            for institution in institutions:
                display_name = institution.get("display_name", "")
                country_code = institution.get("country_code", "")
                country_name = country_code_mapping.get(country_code)

                if not country_name:
                    # Print an error message if the country code is not found
                    print(f"Error: Country code '{country_code}' not found in country_code_mapping.")
                    country_name = country_code  # Fallback to using the country code itself
                 
                if display_name:
                    affiliations.append(f"{display_name}, {country_name}")

            ET.SubElement(name_elem, "affiliation").text = "; ".join(affiliations)

            # Add the <description> element if ORCID is present
            if orcid:
                orcid_value = orcid.replace("https://orcid.org/", "")
                ET.SubElement(name_elem, "description").text = f"orcid.org={orcid_value}"
        # Add Language
        language_field = json_data.get("language", "")
        if isinstance(language_field, dict):
            # Extract the "lang" value if the language field is a dictionary
            language = language_field.get("lang", "")
        else:
            # Use the language field directly if it's a string
            language = language_field

        # Map the two-letter language code to the three-letter code
        language_term = language_code_mapping.get(language, "und")  # Default to "und" (undefined) if not found
        
        # Add title information
        title = json_data.get("title", "")
        if ":" in title:
            # Split the title into main title and subtitle
            main_title, sub_title = map(str.strip, title.split(":", 1))
            # Remove trailing periods
            main_title = main_title.rstrip(".")
            sub_title = sub_title.rstrip(".")  # Remove trailing periods
            
            # Create <titleInfo> with <title> and <subTitle>
            title_info_elem = ET.SubElement(mods, "titleInfo", {"lang": language_term})
            ET.SubElement(title_info_elem, "title").text = main_title
            ET.SubElement(title_info_elem, "subTitle").text = sub_title
        else:
            # Remove trailing period and create <titleInfo> with only <title>
            title = title.rstrip(".")
            title_info_elem = ET.SubElement(mods, "titleInfo", {"lang": language_term})
            ET.SubElement(title_info_elem, "title").text = title
        
        # Create the <language> element
        language_elem = ET.SubElement(mods, "language")
        ET.SubElement(language_elem, "languageTerm", {"type": "code", "authority": "iso639-2b"}).text = language_term

        # Extract the publisher information from "host_organization_name"
        primary_location = json_data.get("primary_location", {})
        source = primary_location.get("source", None)  # Explicitly check if source is None

        # Only proceed if source is not None
        if source:
            publisher = source.get("host_organization_name", None)

            # Create the <originInfo> element
            origin_info_elem = ET.SubElement(mods, "originInfo")
            ET.SubElement(origin_info_elem, "dateIssued").text = str(json_data.get("publication_year", ""))

            # Add the <publisher> element only if "host_organization_name" is not None
            if publisher:
                ET.SubElement(origin_info_elem, "publisher").text = publisher
        else:
            # Create the <originInfo> element without a publisher
            origin_info_elem = ET.SubElement(mods, "originInfo")
            ET.SubElement(origin_info_elem, "dateIssued").text = str(json_data.get("publication_year", ""))

        # Create the <physicalDescription> element
        physical_description_elem = ET.SubElement(mods, "physicalDescription")
        ET.SubElement(physical_description_elem, "form", {"authority": "marcform"}).text = "electronic"

        # Create <identifier type=doi> element
        doi = json_data.get("doi", "")
        if doi and doi.lower() != "none":  # Check if DOI exists and is not "none"
            doi_value = doi.replace("https://doi.org/", "")
            ET.SubElement(mods, "identifier", {"type": "doi"}).text = doi_value

        # Create <identifier type=pmid> element
        pmid = json_data.get("ids", {}).get("pmid", "")
        if pmid and pmid.lower() != "none":  # Check if PMID exists and is not "none"
            pmid_value = pmid.replace("https://pubmed.ncbi.nlm.nih.gov/", "")
            ET.SubElement(mods, "identifier", {"type": "pmid"}).text = pmid_value

        # Initialize issn with a default value
        issn = None

        # Check if "source" exists
        primary_location = json_data.get("primary_location", {})
        source = primary_location.get("source", None)

        # Only proceed if "source" is not None
        if source:
            issn = source.get("issn_l", None)  # Explicitly check for None
            if issn and isinstance(issn, str):  # Ensure issn is not None and is a string
                ET.SubElement(mods, "identifier", {"type": "issn"}).text = issn

        # Add location
        primary_location = json_data.get("primary_location", {})
        
        if not doi:
            # Create <location> with landing_page_url if there is no DOI
            if primary_location.get("is_oa", False) is True:
                location_elem = ET.SubElement(mods, "location")
                ET.SubElement(location_elem, "url", {"displayLabel": "Fulltext", "note": "free"}).text = primary_location.get("landing_page_url", "")
            else:
                location_elem = ET.SubElement(mods, "location")
                ET.SubElement(location_elem, "url", {"displayLabel": "Fulltext"}).text = primary_location.get("landing_page_url", "")

        # Add related item
        related_item_elem = ET.SubElement(mods, "relatedItem", {"type": "host"})

        # Check if "source" and "display_name" exist and are not None
        source = primary_location.get("source", None)
        display_name = source.get("display_name", None) if source else None

        if display_name:
            title_info_elem = ET.SubElement(related_item_elem, "titleInfo")
            ET.SubElement(title_info_elem, "title").text = display_name

        # Use issn in the related item section
        if issn and isinstance(issn, str):
            ET.SubElement(related_item_elem, "identifier", {"type": "issn"}).text = issn

        part_elem = ET.SubElement(related_item_elem, "part")

        # Access the "biblio" object
        biblio = json_data.get("biblio", {})

        # Extract volume, issue, first_page, and last_page from "biblio"
        volume = biblio.get("volume", "")
        if volume:
            detailv_elem = ET.SubElement(part_elem, "detail", {"type": "volume"})
            ET.SubElement(detailv_elem, "number").text = volume

        issue = biblio.get("issue", "")
        if issue:
            detaili_elem = ET.SubElement(part_elem, "detail", {"type": "issue"})
            ET.SubElement(detaili_elem, "number").text = issue

        page_start = biblio.get("first_page", "")
        page_end = biblio.get("last_page", "")
        if page_start or page_end:
            extent_elem = ET.SubElement(part_elem, "extent")
            if page_start:
                ET.SubElement(extent_elem, "start").text = page_start
            if page_end:
                ET.SubElement(extent_elem, "end").text = page_end
       

        if type_crossref == "journal-article" and not biblio.get("volume") and not biblio.get("issue"):
            ET.SubElement(mods, "note", {"type": "publicationStatus", "lang": "eng"}).text = "Epub ahead of print"    
        
    # Write the XML to a file
    tree = ET.ElementTree(mods_collection)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)
    print(f"XML file saved to {output_file}")

if __name__ == "__main__":

    # Check if command-line arguments are provided
    if len(sys.argv) < 3:
        print(f"No input or output file provided. Using default input file 'openalex_records.json' and output file 'openalex.xml'.")
        input_file = "openalex_records.json"  # Default input file
        output_file = f"openalex.xml"  # Default output file with today's date
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]

    # Load the JSON data from the input file
    try:
        with open(input_file, "r", encoding="utf-8") as file:
            json_data = json.load(file)
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        sys.exit(1)

    # Convert JSON to XML
    json_to_xml(json_data, output_file)