import os
import glob
import shutil
from urllib.parse import unquote

def process_coordinate_files():
    """
    Iterate through all coordinate files and process them according to requirements:
    1. If address contains "maaf", prompt user to delete
    2. If not, append first 2 lines from corresponding .txt file
    """
    
    # Pattern to find all coordinate files
    pattern = r"yearly_result\result_*\output_banjir\*_coordinate.loc"
    coordinate_files = glob.glob(pattern, recursive=True)
    
    print(f"Found {len(coordinate_files)} coordinate files to process...\n")
    
    for coord_file in coordinate_files:
        try:
            # Read the coordinate file
            with open(coord_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            print(f"Processing: {coord_file}")
            print("=" * 50)
            
            # Check if address contains "maaf"
            if "maaf" in content.lower():
                print("Content of file:")
                print(content)
                print("\nThis file contains 'maaf' in the address.")
                
                while True:
                    user_input = input("Do you want to delete this file? (yes/no): ").lower().strip()
                    if user_input in ['yes', 'y']:
                        try:
                            os.remove(coord_file)
                            print(f"File {coord_file} deleted successfully.\n")
                        except Exception as e:
                            print(f"Error deleting file {coord_file}: {e}\n")
                        break
                    elif user_input in ['no', 'n']:
                        print("File kept.\n")
                        break
                    else:
                        print("Please enter 'yes' or 'no'")
            else:
                # File doesn't contain "maaf", check if it needs POST and DATE lines
                # Read the coordinate file to count lines
                with open(coord_file, 'r', encoding='utf-8') as f:
                    coord_lines = f.readlines()
                
                coord_line_count = len(coord_lines)
                
                # Only append if file has exactly 2 lines (Address and Coordinates only)
                if coord_line_count == 2:
                    # Get the corresponding .txt file
                    base_name = os.path.basename(coord_file).replace('_coordinate.loc', '.txt')
                    txt_file = os.path.join(os.path.dirname(coord_file), base_name)
                    
                    if os.path.exists(txt_file):
                        try:
                            # Read first 2 lines from .txt file
                            with open(txt_file, 'r', encoding='utf-8') as f:
                                lines = f.readlines()
                                first_two_lines = ''.join(lines[:2]).strip()
                            
                            # Append to coordinate file
                            with open(coord_file, 'a', encoding='utf-8') as f:
                                f.write('\n' + first_two_lines)
                            
                            print(f"Appended content from {base_name} to {os.path.basename(coord_file)}")
                            print(f"Added lines:\n{first_two_lines}\n")
                            
                        except Exception as e:
                            print(f"Error processing {txt_file}: {e}\n")
                    else:
                        print(f"Warning: Corresponding .txt file not found: {txt_file}\n")
                else:
                    print(f"Skipped: {os.path.basename(coord_file)} already has {coord_line_count} lines (not 2)\n")
                    
        except Exception as e:
            print(f"Error processing {coord_file}: {e}\n")
        
        print("-" * 50)

def show_sample_file():
    """Show a sample of what the files look like"""
    pattern = r"yearly_result\result_*\output_banjir\*_coordinate.loc"
    coordinate_files = glob.glob(pattern, recursive=True)
    
    if coordinate_files:
        sample_file = coordinate_files[0]
        print(f"Sample coordinate file: {sample_file}")
        try:
            with open(sample_file, 'r', encoding='utf-8') as f:
                content = f.read()
            print("Content:")
            print(content)
            print("-" * 30)
            
            # Show corresponding txt file
            base_name = os.path.basename(sample_file).replace('_coordinate.loc', '.txt')
            txt_file = os.path.join(os.path.dirname(sample_file), base_name)
            if os.path.exists(txt_file):
                print(f"Corresponding txt file: {txt_file}")
                with open(txt_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    first_two_lines = ''.join(lines[:2])
                print("First 2 lines:")
                print(first_two_lines)
        except Exception as e:
            print(f"Error reading sample file: {e}")

def check_file_line_count():
    """
    Check if all coordinate files have exactly 4 lines.
    If not, show content and prompt user to delete.
    """
    pattern = r"yearly_result\result_*\output_banjir\*_coordinate.loc"
    coordinate_files = glob.glob(pattern, recursive=True)
    
    print(f"Checking {len(coordinate_files)} coordinate files for 4-line requirement...\n")
    
    files_with_issues = 0
    
    for coord_file in coordinate_files:
        try:
            # Read the coordinate file
            with open(coord_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            line_count = len(lines)
            
            # Check if file has exactly 4 lines
            if line_count != 4:
                files_with_issues += 1
                print(f"Processing: {coord_file}")
                print("=" * 50)
                print(f"This file has {line_count} lines instead of 4.")
                print("\nFile content:")
                print("-" * 20)
                
                # Show content
                with open(coord_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                print(content)
                print("-" * 20)
                
                while True:
                    user_input = input("Do you want to delete this file? (yes/no): ").lower().strip()
                    if user_input in ['yes', 'y']:
                        try:
                            os.remove(coord_file)
                            print(f"File {coord_file} deleted successfully.\n")
                        except Exception as e:
                            print(f"Error deleting file {coord_file}: {e}\n")
                        break
                    elif user_input in ['no', 'n']:
                        print("File kept.\n")
                        break
                    else:
                        print("Please enter 'yes' or 'no'")
                
                print("-" * 50)
            else:
                print(f"✓ {os.path.basename(coord_file)} - OK (4 lines)")
                
        except Exception as e:
            print(f"Error processing {coord_file}: {e}\n")
    
    print(f"\nSummary: Found {files_with_issues} files with line count issues.")

def fix_six_line_files():
    """
    Find files with exactly 6 lines and automatically remove the last 2 lines.
    """
    pattern = r"yearly_result\result_*\output_banjir\*_coordinate.loc"
    coordinate_files = glob.glob(pattern, recursive=True)
    
    print(f"Checking {len(coordinate_files)} coordinate files for 6-line files to fix...\n")
    
    files_fixed = 0
    
    for coord_file in coordinate_files:
        try:
            # Read the coordinate file
            with open(coord_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            line_count = len(lines)
            
            # Check if file has exactly 6 lines
            if line_count == 6:
                files_fixed += 1
                print(f"Found 6-line file: {coord_file}")
                print("=" * 50)
                
                # Show original content
                print("Original content (6 lines):")
                print("-" * 20)
                for i, line in enumerate(lines, 1):
                    print(f"{i}: {line.rstrip()}")
                print("-" * 20)
                
                # Keep only the first 4 lines
                new_content = ''.join(lines[:4])
                
                # Write back to file
                with open(coord_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print("✓ Removed last 2 lines. New content (4 lines):")
                print("-" * 20)
                for i, line in enumerate(lines[:4], 1):
                    print(f"{i}: {line.rstrip()}")
                print("-" * 20)
                print(f"Fixed: {os.path.basename(coord_file)}\n")
                
            else:
                print(f"Skipped: {os.path.basename(coord_file)} ({line_count} lines)")
                
        except Exception as e:
            print(f"Error processing {coord_file}: {e}\n")
    
    print(f"\nSummary: Fixed {files_fixed} files that had 6 lines.")

def copy_files_to_new_structure():
    """
    Copy all coordinate and text files to a new organized folder structure.
    Structure: root_folder/year/filename.ext
    """
    # Get root folder name from user
    root_folder = input("Enter the root folder name: ").strip()
    
    if not root_folder:
        print("Root folder name cannot be empty.")
        return
    
    # Create the root folder if it doesn't exist
    if not os.path.exists(root_folder):
        try:
            os.makedirs(root_folder)
            print(f"Created root folder: {root_folder}")
        except Exception as e:
            print(f"Error creating root folder: {e}")
            return
    
    # Pattern to find all coordinate files
    pattern = r"yearly_result\result_*\output_banjir\*_coordinate.loc"
    coordinate_files = glob.glob(pattern, recursive=True)
    
    print(f"Found {len(coordinate_files)} coordinate files to copy...\n")
    
    copied_files = 0
    years_created = set()
    
    for coord_file in coordinate_files:
        try:
            # Extract year from the path (e.g., result_2010 -> 2010)
            path_parts = coord_file.replace('\\', '/').split('/')
            year_folder = None
            for part in path_parts:
                if part.startswith('result_'):
                    year_folder = part.replace('result_', '')
                    break
            
            if not year_folder:
                print(f"Warning: Could not extract year from {coord_file}")
                continue
            
            # Create year folder if it doesn't exist
            year_path = os.path.join(root_folder, year_folder)
            if not os.path.exists(year_path):
                os.makedirs(year_path)
                years_created.add(year_folder)
                print(f"Created year folder: {year_folder}")
            
            # Get the base filename (without _coordinate.loc)
            coord_filename = os.path.basename(coord_file)
            base_name = coord_filename.replace('_coordinate.loc', '')
            
            # Copy coordinate file
            coord_dest = os.path.join(year_path, coord_filename)
            shutil.copy2(coord_file, coord_dest)
            
            # Copy corresponding txt file
            txt_file = coord_file.replace('_coordinate.loc', '.txt')
            if os.path.exists(txt_file):
                txt_filename = base_name + '.txt'
                txt_dest = os.path.join(year_path, txt_filename)
                shutil.copy2(txt_file, txt_dest)
                
                print(f"Copied pair: {coord_filename} and {txt_filename} to {year_folder}/")
                copied_files += 1
            else:
                print(f"Warning: Corresponding .txt file not found for {coord_filename}")
                # Still copy the coordinate file
                print(f"Copied: {coord_filename} to {year_folder}/ (no corresponding .txt)")
                copied_files += 1
                
        except Exception as e:
            print(f"Error processing {coord_file}: {e}")
    
    print(f"\nSummary:")
    print(f"- Root folder: {root_folder}")
    print(f"- Years created: {sorted(years_created)}")
    print(f"- File pairs copied: {copied_files}")
    print(f"- Total years: {len(years_created)}")

if __name__ == "__main__":
    print("Coordinate File Processor")
    print("=" * 30)
    
    while True:
        print("\nOptions:")
        print("1. Show sample file")
        print("2. Process all coordinate files")
        print("3. Check files for 4-line requirement")
        print("4. Fix 6-line files (remove last 2 lines)")
        print("5. Copy files to new organized structure")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == '1':
            show_sample_file()
        elif choice == '2':
            process_coordinate_files()
        elif choice == '3':
            check_file_line_count()
        elif choice == '4':
            fix_six_line_files()
        elif choice == '5':
            copy_files_to_new_structure()
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, 5, or 6.")