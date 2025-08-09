# GeoLLM - Geographic Coordinate Extraction System

An automated system that uses OpenAI's language models and Google Maps Geocoding API to extract geographic coordinates from flood-related text documents. The system processes Indonesian text documents containing location information and generates precise coordinates for mapping and analysis purposes.

## Project Overview

GeoLLM is designed to process flood-related text documents from Indonesia, extract location information using AI, and convert that information into precise geographic coordinates. The system is specifically tailored for processing yearly flood data and includes comprehensive data validation and cleanup tools.

## Project Structure

```
GeoLLM/
├── main.py                    # Main coordinate extraction script
├── recheck.py                 # Data validation and cleanup utility
├── .env                       # Environment variables (API keys)
├── .gitignore                 # Git ignore file
├── README.md                  # This documentation
├── yearly_result/             # Input directory structure
│   ├── result_2010/
│   │   └── output_banjir/
│   │       ├── 1.txt          # Source text files
│   │       ├── 2.txt
│   │       └── ...
│   ├── result_2011/
│   └── ...
└── venv/                      # Python virtual environment
```

## Setup

### 1. Environment Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd e100-geocoding-extraction
   ```

2. **Set up Python virtual environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # or
   source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**:
   ```bash
   pip install openai python-dotenv requests
   ```

### 2. API Keys Configuration

1. **OpenAI API Key**:
   - Go to https://platform.openai.com/api-keys
   - Create a new API key
   - Copy the key

2. **Google Maps Geocoding API Key**:
   - Go to https://console.developers.google.com/
   - Enable the Geocoding API
   - Create credentials and get your API key

3. **Create `.env` file**:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
   ```

### 3. Input Data Structure

Ensure your input data follows this structure:
```
yearly_result/
├── result_2010/
│   └── output_banjir/
│       ├── 1.txt              # Flood report text files
│       ├── 2.txt
│       └── ...
├── result_2011/
│   └── output_banjir/
│       ├── 1.txt
│       └── ...
└── ...
```

## Main Processing Script (main.py)

### Features

- **AI-Powered Address Extraction**: Uses OpenAI GPT-4.1-mini to extract precise addresses from Indonesian flood reports
- **Geocoding Integration**: Converts extracted addresses to precise coordinates using Google Maps API
- **Batch Processing**: Processes multiple years (2010-2025) automatically
- **Smart Skipping**: Avoids reprocessing files that already have coordinate files
- **Error Handling**: Comprehensive error handling with detailed logging
- **Progress Tracking**: Real-time progress updates and statistics

### AI Prompting Strategy

The system uses a carefully crafted Indonesian prompt to ensure accurate address extraction:

```
"Saya membutuhkan bantuan anda untuk memberikan alamat yang akurat dari 
text yang diberikan di bawah ini:

[TEXT CONTENT]

Berikan langsung jawaban alamat tanpa tambahan kata-kata lain. 
Apabila memungkinkan, berikan alamat dalam format

<kelurahan>%20<kecamatan>%20<kota>%20Indonesia

Bila informasi tidak lengkap, berikan saja alamat yang tersedia. 
Bila terdapat lebih dari satu alamat, berikan satu alamat yang paling relevan. 
Ubah spasi menjadi '%20' untuk format URL."
```

### Model Configuration

- **Primary Model**: GPT-4.1-mini (with web search capabilities)
- **Temperature**: 0.3 (for consistent, focused responses)
- **Purpose**: Optimized for accurate geographic information extraction

### Geocoding Service

- **Provider**: Google Maps Geocoding API
- **Format**: Returns coordinates as "latitude, longitude"
- **Error Handling**: Graceful fallback for failed geocoding requests
- **Rate Limiting**: Built-in request management

### Usage

```bash
python main.py
```

### Output Format

For each processed text file, the system creates a corresponding `*_coordinate.loc` file containing:

```
Address: Kelurahan%20Kemayoran%20Jakarta%20Pusat%20Indonesia
Coordinates: -6.1751, 106.8650
```

## Data Validation Script (recheck.py)

The recheck script provides comprehensive data validation and cleanup utilities for the generated coordinate files.

### Features

1. **Quality Control**: Identifies and handles files with "maaf" (apology) responses
2. **Data Completion**: Appends POST and DATE information from source files
3. **Format Validation**: Ensures all coordinate files have exactly 4 lines
4. **Automatic Fixes**: Repairs files with exactly 6 lines by removing duplicates
5. **File Organization**: Copies files to organized year-based structure

### Interactive Menu Options

1. **Show Sample File**: Preview the format of coordinate files
2. **Process All Coordinate Files**: Main processing for incomplete files
3. **Check 4-Line Requirement**: Validate file format consistency
4. **Fix 6-Line Files**: Automatic repair of duplicate content
5. **Copy to Organized Structure**: Create clean output directory
6. **Exit**: Close the application

### Expected Output Format

Each coordinate file should contain exactly 4 lines:
```
Address: [extracted address]
Coordinates: [latitude, longitude]
POST: [original posting information]
DATE: [date information]
```

### Usage

```bash
python recheck.py
```

Follow the interactive prompts to select validation and cleanup operations.

## Workflow

### 1. Initial Processing
```bash
python main.py
```
- Processes all `.txt` files in `yearly_result/result_*/output_banjir/`
- Extracts addresses using OpenAI API
- Converts addresses to coordinates using Google Maps API
- Creates `*_coordinate.loc` files

### 2. Data Validation
```bash
python recheck.py
```
- Select option 2: "Process all coordinate files"
- Reviews files for quality issues
- Appends missing POST/DATE information
- Handles problematic extractions

### 3. Quality Assurance
```bash
python recheck.py
```
- Select option 3: "Check files for 4-line requirement"
- Identifies format inconsistencies
- Prompts for cleanup decisions

### 4. Final Cleanup
```bash
python recheck.py
```
- Select option 4: "Fix 6-line files" (if needed)
- Select option 5: "Copy to organized structure"

## Error Handling

### Common Issues and Solutions

1. **API Key Errors**:
   - Verify `.env` file exists and contains valid keys
   - Check API key permissions and quotas

2. **"Maaf" Responses**:
   - AI couldn't extract valid address
   - Use recheck.py to identify and handle these files

3. **Geocoding Failures**:
   - Address format may be incorrect
   - API rate limits or network issues
   - Invalid or incomplete addresses

4. **File Format Issues**:
   - Use recheck.py validation tools
   - Check for encoding problems (UTF-8 required)

## Performance Considerations

- **Processing Speed**: ~2-3 seconds per file (including API calls)
- **API Costs**: Moderate OpenAI usage per file
- **Rate Limits**: Respects Google Maps API quotas
- **Batch Size**: Processes years sequentially to manage resources

## Output Statistics

The system provides detailed processing statistics:
- Total files processed
- Success/error rates
- Processing time estimates
- Year-by-year breakdowns

## Contributing

1. Follow the existing code structure
2. Add error handling for new features
3. Update documentation for any changes
4. Test with sample data before full processing

## License

This project is designed for flood data analysis and geographic information extraction purposes.
