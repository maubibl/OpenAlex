import requests
import json
import subprocess
import xml.etree.ElementTree as ET
import datetime  # Import datetime for date formatting

# List of OpenAlex IDs to fetch
openalex_ids = []
doi = ["10.1145/3770501.3770517","10.1177/14639491251399202","10.1140/epjd/s10053-025-01105-8"]

def fetch_openalex_records(openalex_ids, dois, output_file):
    """
    Fetch records from OpenAlex API using both OpenAlex IDs and DOIs, and save them to a file.

    Args:
        openalex_ids (list): List of OpenAlex IDs to fetch.
        dois (list): List of DOIs to fetch.
        output_file (str): Path to the output file where the response will be saved.
    """
    headers = {
        "User-Agent": "mailto=aron.lindhagen@mau.se"
    }
    
    all_records = []  # List to store all fetched records

    try:
        # Fetch by OpenAlex IDs
        for openalex_id in openalex_ids:
            url = f"https://api.openalex.org/works/{openalex_id}"
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            record = response.json()
            all_records.append(record)
        
        # Fetch by DOIs
        for doi in dois:
            url = f"https://api.openalex.org/works/https://doi.org/{doi}"
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            record = response.json()
            all_records.append(record)

        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(all_records, file, indent=4)
        
        print(f"Records successfully fetched and saved to {output_file}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching records: {e}")

def fetch_xlink_href(abstract, title):
    """
    Fetch classification from Swepub Classify API.
    Args:
        abstract (str): Concatenated abstract terms.
        title (str): Title of the record.
    Returns:
        str: Classification code (e.g., "10205").
    """
    url = "https://bibliometri.swepub.kb.se/api/v1/classify"
    headers = {
        "Content-Type": "application/json"
    }
    
    # First attempt with level 5
    data = {
        "abstract": abstract,
        "keywords": "",
        "classes": 1,
        "level": 5,
        "title": title
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        result = response.json()
        if 'suggestions' in result and len(result['suggestions']) > 0:
            best_suggestion = max(result['suggestions'], key=lambda x: x['_score'])
            return best_suggestion['code']
    
    # Second attempt with level 3 if no suggestions found in the first attempt
    data["level"] = 3
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        result = response.json()
        if 'suggestions' in result and len(result['suggestions']) > 0:
            best_suggestion = max(result['suggestions'], key=lambda x: x['_score'])
            return best_suggestion['code']
    
    raise Exception("No suggestions found in API response")

def add_classification_to_xml(json_data_list, xml_file):
    """
    Add classification to each record in the XML based on Swepub Classify API.
    Args:
        json_data_list (list): List of JSON records.
        xml_file (str): Path to the XML file to modify.
    """
    # Define namespaces
    namespaces = {
        "": "http://www.loc.gov/mods/v3",  # Default namespace
        "xlink": "http://www.w3.org/1999/xlink"  # xlink namespace
    }
    for prefix, uri in namespaces.items():
        ET.register_namespace(prefix, uri)  # Register namespaces

    # Parse the existing XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Iterate over JSON records and corresponding <mods> elements
    for json_data, mods in zip(json_data_list, root.findall("{http://www.loc.gov/mods/v3}mods")):
        # Skip if no "abstract_inverted_index" exists
        abstract_inverted_index = json_data.get("abstract_inverted_index", None)
        if not abstract_inverted_index:
            continue
        
        # Concatenate all terms in "abstract_inverted_index" to form the abstract
        abstract = " ".join(abstract_inverted_index.keys())
        title = json_data.get("title", "")
        
        try:
            # Fetch classification code from Swepub Classify API
            classification_code = fetch_xlink_href(abstract, title)
            
            # Add <subject> element to the XML
            ET.SubElement(mods, "subject", {
                "lang": "eng",
                "authority": "hsv",
                "{http://www.w3.org/1999/xlink}href": classification_code  # Use xlink namespace
            })
        except Exception as e:
            print(f"Error fetching classification for title '{title}': {e}")
    
    # Save the updated XML file
    tree.write(xml_file, encoding="utf-8", xml_declaration=True)
    print(f"Updated XML file saved to {xml_file}")

if __name__ == "__main__":
    # Output file path
    output_file = "openalex_records.json"
    
    # Fetch and save records
    fetch_openalex_records(openalex_ids, doi, output_file)
    
    # Generate today's date in YYMMDD format
    today_date = datetime.datetime.now().strftime("%y%m%d")
    xml_file = f"openalex{today_date}.xml"  # Output XML file with today's date
    
    # Call transOA.py to convert JSON to XML
    try:
        subprocess.run(["python3", "transOA.py", output_file, xml_file], check=True)
        print(f"XML file successfully created by transOA.py: {xml_file}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running transOA.py: {e}")
    
    # Add classification to the XML
    try:
        with open(output_file, "r", encoding="utf-8") as file:
            json_data_list = json.load(file)
        add_classification_to_xml(json_data_list, xml_file)
    except Exception as e:
        print(f"An error occurred while adding classifications to the XML: {e}")