# Student Name Mapping Guide

## How to Update Student Names

The `student_mappings.py` file contains a dictionary that maps short names (from bank statements) to full student names.

### Quick Steps:

1. **Find the short name** in the application table
2. **Open** `student_mappings.py` in a text editor
3. **Locate or add** the entry in `STUDENT_NAME_MAPPINGS`
4. **Save** the file
5. **Restart** the application

### Example:

If you see "MEENAKSHI" in the bank statement and want it to show as "Meenakshi Sundaram":

```python
STUDENT_NAME_MAPPINGS = {
    "MEENAKSHI": "Meenakshi Sundaram",
    # ... other entries
}
```

### Format Rules:

- **Key (left side)**: Exact short name as it appears in bank statement (with spaces and capitalization)
- **Value (right side)**: Full name you want to display
- **Syntax**: `"SHORT_NAME": "Full Name",` (don't forget the comma!)

### Tips:

1. **Keep it alphabetical** for easy finding
2. **Use consistent formatting** for full names (e.g., all Title Case)
3. **Test after changes** by uploading a CSV file
4. **Back up** the file before making major changes

### Common Short Names Already Mapped:

The file already includes ~50 common names. Check the list before adding duplicates.

### Adding New Students:

When you see a new short name in the transactions:

1. Note the exact spelling (including spaces)
2. Add a new line in the appropriate alphabetical section:
   ```python
   "NEW SHORT": "New Student Full Name",
   ```
3. Save and restart

### Example Section:

```python
# Names starting with M
"M KALAVAT": "M Kalavathi",
"M USHA": "M Usha Rani",
"Manisha": "Manisha Sharma",
"MEENA KAI": "Meena Kailash",
"MEENAKSHI": "Meenakshi Sundaram",
"Mrs V N J": "Mrs V N Jayalakshmi",
```

### Troubleshooting:

**Name not changing?**
- Check spelling matches exactly (case-sensitive for keys)
- Make sure you saved the file
- Restart the application

**Application won't start?**
- Check for syntax errors (missing quotes, commas)
- Python is very strict about indentation

**Multiple people with same short name?**
- Unfortunately, the current system can't distinguish
- Consider adding more context in the full name
- Example: "Lakshmi R" vs "Lakshmi S"

### Need Help?

The mapping system uses simple Python dictionary syntax. Just follow the pattern of existing entries!
