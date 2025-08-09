import os
import glob
import requests
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def setup_openai_client():
    """Initialize OpenAI client with API key"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY not found in environment variables.")
        print("Please create a .env file with your OpenAI API key:")
        print("OPENAI_API_KEY=your_api_key_here")
        return None
    
    return OpenAI(api_key=api_key)

def chat_with_openai(client, prompt, model="gpt-4.1-mini"):
    """Send a prompt to OpenAI and get response"""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            # max_tokens=1000,
            temperature=0.3,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def get_coordinates_from_api(address):
    """Get coordinates from Google Maps Geocoding API"""
    try:
        # Get Google Maps API key from environment
        google_api_key = os.getenv('GOOGLE_MAPS_API_KEY')
        if not google_api_key:
            return "Error: GOOGLE_MAPS_API_KEY not found in environment variables"
        
        # Format the address for URL
        formatted_address = address.replace(' ', '%20')
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={formatted_address}&key={google_api_key}"
        
        # Make API request
        response = requests.get(url, headers={'User-Agent': 'GeoLLM/1.0'})
        response.raise_for_status()
        
        data = response.json()
        
        # Check if we got results
        if data.get('status') == 'OK' and data.get('results') and len(data['results']) > 0:
            location = data['results'][0]['geometry']['location']
            latitude = location['lat']
            longitude = location['lng']
            return f"{latitude}, {longitude}"
        else:
            return "Error: No coordinates found"
            
    except Exception as e:
        return f"Error: {str(e)}"

def process_text_file(client, file_path, model="gpt-4.1-mini"):
    """Process a single text file and extract coordinates"""
    try:
        # Read the text file
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read().strip()
        
        # Create prompt for address extraction
        prompt = (
            "Saya membutuhkan bantuan anda untuk memberikan alamat yang akurat dari "
            "text yang diberikan di bawah ini:\n\n"
            f"{text}"
            "\n\nBerikan langsung jawaban alamat tanpa tambahan kata-kata lain. "
            "Apabila memungkinkan, berikan alamat dalam format\n\n"
            "<kelurahan>%20<kecamatan>%20<kota>%20Indonesia\n\n"
            "Bila informasi tidak lengkap, berikan saja alamat yang tersedia. "
            "Bila terdapat lebih dari satu alamat, berikan satu alamat yang paling relevan. "
            "Ubah spasi menjadi '%20' untuk format URL.\n\n"
        )
        
        # Get AI response for address
        address_response = chat_with_openai(client, prompt, model)
        
        # Clean up the address response
        address = address_response.strip()
        
        # Get coordinates from API
        coordinates = get_coordinates_from_api(address)
        
        # Return both address and coordinates
        result = f"Address: {address}\nCoordinates: {coordinates}"
        print(result)
        return result
        
    except Exception as e:
        return f"Error processing file {file_path}: {str(e)}"

def main():
    """Process all text files in yearly_result folders"""
    print("OpenAI Coordinate Extraction")
    print("=" * 30)
    
    # Initialize OpenAI client
    client = setup_openai_client()
    if not client:
        return
    
    # Use the specified model with search capabilities
    model = "gpt-4.1-mini"
    print(f"Using model: {model} (with web search capabilities)")
    print()
    
    # Base directory
    base_dir = "yearly_result"
    
    # Process each year from 2010 to 2025
    total_processed = 0
    total_errors = 0
    
    for year in range(2010, 2026):
        year_folder = os.path.join(base_dir, f"result_{year}")
        output_banjir_folder = os.path.join(year_folder, "output_banjir")
        
        if not os.path.exists(output_banjir_folder):
            print(f"Skipping {year} - output_banjir folder not found")
            continue
        
        # Get all txt files in the folder
        txt_files = glob.glob(os.path.join(output_banjir_folder, "*.txt"))
        
        if not txt_files:
            print(f"No txt files found in {year}")
            continue
        
        print(f"Processing {year} - Found {len(txt_files)} files")
        
        for txt_file in txt_files:
            try:
                print("")
                # Get the filename without extension
                filename = os.path.basename(txt_file)
                name_without_ext = os.path.splitext(filename)[0]
                
                # Create coordinate filename
                coordinate_file = os.path.join(output_banjir_folder, f"{name_without_ext}_coordinate.loc")
                
                # Skip if coordinate file already exists
                if os.path.exists(coordinate_file):
                    print(f"  Skipping {filename} - coordinate file already exists")
                    continue
                
                print(f"Processing: {year}-{filename}")
                
                # Process the file
                response = process_text_file(client, txt_file, model)
                
                if "Error" in response:
                    print(f"  Error processing {filename}: {response}")
                    total_errors += 1
                    continue

                # Save the response
                with open(coordinate_file, 'w', encoding='utf-8') as f:
                    f.write(response)
                
                total_processed += 1
                print(f"  Saved: {name_without_ext}_coordinate.loc")
                
            except Exception as e:
                total_errors += 1
                print(f"  Error processing {filename}: {str(e)}")
        
        print(f"Completed {year}\n")
    
    print("=" * 30)
    print(f"Processing complete!")
    print(f"Total files processed: {total_processed}")
    print(f"Total errors: {total_errors}")
    print("Done!")

if __name__ == "__main__":
    main()