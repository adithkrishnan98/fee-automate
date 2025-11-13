"""
Student Name Mapping System
Maps short names from bank statements to full student names
Student mappings are now stored in 'student_name_mappings.json'
Edit the JSON file to add new students
"""

import json
from pathlib import Path

# Global variable to hold mappings (loaded from JSON)
STUDENT_NAME_MAPPINGS = {}

def load_student_mappings():
    """
    Load student name mappings from JSON file
    Creates an empty template file if it doesn't exist
    
    Returns:
        dict: Student name mappings
    """
    json_file = Path(__file__).parent / 'student_name_mappings.json'
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('mappings', {})
    except FileNotFoundError:
        # Create empty template file on first run
        print(f"Info: {json_file} not found. Creating empty template file.")
        template_data = {
            "mappings": {},
            "_comment": "Student name mappings for the Music Class Fee Tracker.",
            "_instructions": "Add student mappings in the format: 'SHORTNAME': 'Full Student Name'",
            "_example": {
                "JOHN D": "John Doe",
                "MARY S": "Mary Smith"
            }
        }
        try:
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(template_data, f, indent=2, ensure_ascii=False)
            print(f"Created template file: {json_file}")
        except Exception as create_error:
            print(f"Warning: Could not create template file: {create_error}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Warning: Error parsing {json_file}: {e}. Using empty mappings.")
        return {}
    except Exception as e:
        print(f"Warning: Error loading student mappings: {e}. Using empty mappings.")
        return {}

def save_student_mappings(mappings):
    """
    Save student name mappings to JSON file
    
    Args:
        mappings (dict): Student name mappings to save
        
    Returns:
        bool: True if saved successfully
    """
    json_file = Path(__file__).parent / 'student_name_mappings.json'
    
    try:
        data = {
            "mappings": mappings,
            "_comment": "Student name mappings for the Music Class Fee Tracker. Add new students here as they join."
        }
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving student mappings: {e}")
        return False

# Load mappings on module import
STUDENT_NAME_MAPPINGS = load_student_mappings()


def get_full_name(short_name):
    """
    Get full name from short name mapping
    Returns the short name (formatted) if no mapping found
    
    Matching strategies (in order):
    1. Exact match
    2. Case-insensitive match
    3. Space-removed match (e.g., "SUNDARA P" -> "SUNDARAP")
    4. Space-removed case-insensitive match
    """
    # Remove extra spaces
    short_name = " ".join(short_name.split())
    
    # Strategy 1: Try exact match
    if short_name in STUDENT_NAME_MAPPINGS:
        return STUDENT_NAME_MAPPINGS[short_name]
    
    # Strategy 2: Try case-insensitive match
    for key, value in STUDENT_NAME_MAPPINGS.items():
        if key.lower() == short_name.lower():
            return value
    
    # Strategy 3: Try space-removed match
    # Remove all spaces and try matching
    short_name_no_space = short_name.replace(" ", "")
    for key, value in STUDENT_NAME_MAPPINGS.items():
        if key.replace(" ", "") == short_name_no_space:
            return value
    
    # Strategy 4: Try space-removed case-insensitive match
    for key, value in STUDENT_NAME_MAPPINGS.items():
        if key.replace(" ", "").lower() == short_name_no_space.lower():
            return value
    
    # If no match, return formatted short name
    return f"{short_name.title()}"


def add_mapping(short_name, full_name):
    """
    Add a new student name mapping and save to JSON file
    
    Args:
        short_name (str): Short name from bank statement
        full_name (str): Full student name
        
    Returns:
        bool: True if added successfully
    """
    short_name = " ".join(short_name.split())
    STUDENT_NAME_MAPPINGS[short_name] = full_name
    return save_student_mappings(STUDENT_NAME_MAPPINGS)


def get_all_mappings():
    """
    Get all current mappings
    
    Returns:
        dict: Dictionary of all student name mappings
    """
    return STUDENT_NAME_MAPPINGS.copy()


def get_unmapped_names(transactions):
    """
    Find short names that don't have mappings yet
    
    Args:
        transactions (list): List of transaction dictionaries
        
    Returns:
        set: Set of unmapped short names
    """
    unmapped = set()
    for transaction in transactions:
        short_name = transaction.get('name', '')
        if short_name and short_name not in STUDENT_NAME_MAPPINGS:
            unmapped.add(short_name)
    return unmapped
