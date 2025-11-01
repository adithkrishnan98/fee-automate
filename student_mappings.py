"""
Student Name Mapping System
Maps short names from bank statements to full student names
Edit this file to update student names
"""

# Student name mappings dictionary
# Key: Short name from bank statement
# Value: Full student name
STUDENT_NAME_MAPPINGS = {
    # Names starting with A
    "ANJANA SW": "Anjana Swaminathan",
    "ARUMUGA K": "Shraddha Krishnan",
    
    # Names starting with B
    "BHAGEERAT": "Bhageerathan",
    "BHUPENDRA": "Bhupendran Sridhar",
    "BHUVANA D": "Bhuvana Devendran",
    "B PARVATH": "B Parvathi",
    
    # Names starting with C
    "CHANDRA R": "Chandra Ramesh",
    "CHELLA PU": "Chella Pushpam",
    "CHITHRA": "Chithra S",
    
    # Names starting with D
    "DHARINI  N": "Dharini N",
    
    # Names starting with G
    "GOMATHI Y": "Gomathi Y",
    
    # Names starting with H
    "HEMALATHA": "Hemalatha Ramesh",
    
    # Names starting with I
    "INDRANI  V": "Indrani Venkatesh",
    
    # Names starting with J
    "JAYALAKSH": "Jayalakshmi",
    
    # Names starting with K
    "KASI": "Kasi",
    
    # Names starting with L
    "LAKSHMI R": "Lakshmi R",
    "LALITHA S": "Lalitha S",
    
    # Names starting with M
    "M KALAVAT": "M Kalavathi",
    "M USHA": "M Usha Rani",
    "Manisha": "Manisha Sharma",
    "MEENA KAI": "Meena Kailash",
    "MEENA SAN": "Meena Sankar",
    "MEENAKSHI": "Meenakshi Sundaram",
    "MEERA  RA": "Meera Ramesh",
    "MRS GEETH": "Mrs Geetha Ramachandran",
    "Mrs VANET": "Mrs Vanitha",
    "Mrs V N J": "Mrs Jayanthi Sampath",
    "Mrs N LAL": "Mrs N Lalitha",
    
    # Names starting with P
    "PREMALATH": "Premalatha",
    
    # Names starting with R
    "R CHITRA": "R Chitra",
    "RAJI  CHA": "Raji Chandrasekaran",
    "RAJESWARI": "Rajeswari",
    "RAMARANI": "Ramarani",
    
    # Names starting with S
    "S BHUVANE": "S Bhuvaneshwari",
    "S VENKATA": "S Venkatesh",
    "SHANTHA S": "Shantha S",
    "SHANTHI L": "Shanthi Lakshman",
    "SHARDHA R": "Shardha Rupa",
    "SHOBANA": "Shobana Krishnan",
    "SRINIVASA": "Padmavathy Srinivasan",
    "Ms SRIPRI": "Ms Sripriya",
    "SUDHA  G": "Sudha Gopalakrishnan",
    "SULOCHANA": "Sulochana",
    "SUNDARA P": "Dhanalakshmi V",
    
    # Names starting with U
    "USHA M": "Usha M",
    "USHA MURL": "Usha Murli",
    "V UMA SHA": "V Uma Shankar",
    
    # Additional names (add more as you identify them)
    "Ms LAKSHM": "Ms Lakshmi Devi",
}


def get_full_name(short_name):
    """
    Get full name from short name mapping
    Returns the short name (formatted) if no mapping found
    
    Args:
        short_name (str): Short name from bank statement
        
    Returns:
        str: Full student name or formatted short name
    """
    # Remove extra spaces
    short_name = " ".join(short_name.split())
    
    # Try exact match
    if short_name in STUDENT_NAME_MAPPINGS:
        return STUDENT_NAME_MAPPINGS[short_name]
    
    # Try case-insensitive match
    for key, value in STUDENT_NAME_MAPPINGS.items():
        if key.lower() == short_name.lower():
            return value
    
    # If no match, return formatted short name with [Unknown] marker
    return f"{short_name.title()}"


def add_mapping(short_name, full_name):
    """
    Add a new student name mapping
    
    Args:
        short_name (str): Short name from bank statement
        full_name (str): Full student name
        
    Returns:
        bool: True if added successfully
    """
    short_name = " ".join(short_name.split())
    STUDENT_NAME_MAPPINGS[short_name] = full_name
    return True


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
