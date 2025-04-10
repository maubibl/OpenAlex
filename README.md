# OpenAlex

This repository contains two Python scripts, `importOpenAlex.py` and `transOA.py`, designed to fetch, process, and convert OpenAlex records into DiVA MODS XML suitable for import to DiVA.

## Features

- Fetches records from the [OpenAlex API](https://openalex.org/) using a list of OpenAlex IDs.
- Converts JSON records into XML format compliant with the MODS schema.
- Adds classification data to the XML using the Swepub Classify API.

## Files

### `importOpenAlex.py`
This script:
1. Fetches records from the OpenAlex API based on a predefined list of OpenAlex IDs.
2. Saves the fetched records as a JSON file.
3. Calls `transOA.py` to convert the JSON data into DiVA MODS.
4. Adds classification data to the XML using the Swepub Classify API.

### `transOA.py`
This script:
1. Converts a list of JSON records into a single DIVA MODS XML file with a `<modsCollection>` root element.
