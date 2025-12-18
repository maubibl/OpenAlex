# OpenAlex to MODS XML Converter

A Python tool for fetching academic records from the OpenAlex API and converting them to MODS (Metadata Object Description Schema) XML format with additional classification data.

## Features

- **Multi-source fetching**: Retrieve records using both OpenAlex IDs and DOIs
- **MODS XML conversion**: Transform JSON data into standardized MODS XML format
- **Author deduplication**: Intelligent handling of duplicate authors while preserving order
- **Funding information**: Include funder information from OpenAlex data
- **Classification integration**: Add subject classifications using the Swepub Classify API
- **Publication type mapping**: Automatic genre classification based on publication types

## Files

### `importOpenAlex.py`
Main script that orchestrates the entire process:
- Fetches records from OpenAlex API
- Converts JSON to XML using `transOA.py`
- Adds classification data to the XML output

### `transOA.py`
Core conversion script that:
- Transforms OpenAlex JSON records to MODS XML format
- Handles author information with deduplication logic
- Maps publication types to appropriate MODS genres
- Includes funding and affiliation data

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/maubibl/OpenAlex.git
   cd OpenAlex
   ```

2. Install required Python packages:
   ```bash
   pip install requests
   ```

## Usage

### Basic Usage

1. **Configure data sources**: Edit the `doi` and `openalex_ids` lists in `importOpenAlex.py`:
   ```python
   doi = ["10.1145/3770501.3770517", "10.1177/14639491251399202"]
   openalex_ids = ["W123456789"]  # Add OpenAlex work IDs if needed
   ```

2. **Run the main script**:
   ```bash
   python3 importOpenAlex.py
   ```

This will:
- Fetch records from OpenAlex API
- Generate `openalex_records.json` with the raw data
- Create `openalexYYMMDD.xml` (dated XML file) in MODS format
- Add classification data to the XML

### Manual Conversion

To convert existing JSON data to XML:
```bash
python3 transOA.py input.json output.xml
```

## Configuration

### Data Sources

- **DOIs**: Add DOI strings to the `doi` list in `importOpenAlex.py`
- **OpenAlex IDs**: Add work IDs to the `openalex_ids` list

### API Settings

The script uses:
- **OpenAlex API**: `https://api.openalex.org/works/`
- **Swepub Classify API**: For adding subject classifications
- **User Agent**: Configured for academic use (`mailto=aron.lindhagen@mau.se`)

## Output Format

### XML Structure

The generated XML follows the MODS schema with:
- `<modsCollection>` root element
- Individual `<mods>` elements for each work
- Author information with deduplication
- Publication metadata (title, date, publisher)
- Subject classifications and genres
- Funding information as `<note type="funder">`

### Author Handling

- **Order preservation**: Maintains original author order from OpenAlex
- **Deduplication**: Removes duplicate authors unless they have conflicting information
- **Conflict resolution**: Keeps both entries when ORCID or affiliation data differs
- **Complete information**: Prioritizes authors with more complete metadata

### File Naming

- JSON output: `openalex_records.json`
- XML output: `openalexYYMMDD.xml` (where YYMMDD is current date)

## Dependencies

- `requests`: For API calls
- `xml.etree.ElementTree`: For XML generation (built-in)
- `json`: For data handling (built-in)
- `datetime`: For date formatting (built-in)
- `subprocess`: For running transOA.py (built-in)

## API Usage

This tool respects API guidelines:
- Includes proper User-Agent header
- Handles rate limiting and errors gracefully
- Processes data locally without storing sensitive information

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is developed for academic research purposes. Please ensure compliance with OpenAlex API terms of service and institutional guidelines.

## Contact

For questions or issues:
- **Maintainer**: Aron Lindhagen
- **Email**: aron.lindhagen@mau.se
- **Institution**: Malmö University Library

## Acknowledgments

- **OpenAlex**: For providing comprehensive academic metadata
- **Swepub**: For classification services
- **MODS Community**: For the metadata standard