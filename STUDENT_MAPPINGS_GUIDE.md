# Student Name Mappings Guide

## Overview
Student name mappings map short names from bank statements to full student names. You can manage these mappings through the application's **Student Manager** UI or by editing the JSON file directly.

## Managing Students via Application UI (Recommended) ✨

### Opening the Student Manager
1. Launch the Fee Tracker application
2. Click **"👥 Manage Students"** button in the top toolbar
3. The Student Manager dialog will open showing all current student mappings

### Features Available:

#### 1. **Import from CSV** 📁
- Click **"Import from CSV"** button
- Select a CSV file with 2 columns:
  - Column 1: Short Name (from bank statement)
  - Column 2: Full Student Name
- The app will show how many students were added/updated
- See `sample_student_names.csv` for example format

**CSV Format:**
```csv
Short Name,Full Student Name
SUNDARAP,Dhanalakshmi V
MEENAKAI,Meena Kailash
NEWSTUDENT,New Student Full Name
```

#### 2. **Import from Excel** 📊
- Click **"Import from Excel"** button  
- Select an Excel file (.xlsx or .xls)
- First row can be headers (will be auto-detected)
- Same 2-column format as CSV

#### 3. **Export to Excel** 💾
- Click **"Export to Excel"** to create a backup
- Creates a timestamped Excel file with all current mappings
- Perfect for sharing or editing in Excel then re-importing

#### 4. **Edit Inline** ✏️
- Click on any Full Student Name to edit directly in the table
- Changes are saved when you click **"Save Changes"**

#### 5. **Delete Mappings** 🗑️
- Click the Delete button next to any student
- Confirmation dialog will appear before deleting

#### 6. **Auto Re-process Transactions**
- After saving changes, if you have loaded transactions:
- App will ask if you want to re-apply new mappings to existing transactions
- Choose "Yes" to update all student names in current transactions

## Managing Students via JSON File (Advanced)

### File Location
`student_name_mappings.json` (in the same folder as the application)

### File Format
```json
{
  "mappings": {
    "SHORT_NAME": "Full Student Name",
    "ANOTHER_NAME": "Another Full Name"
  },
  "_comment": "Student name mappings for the Music Class Fee Tracker. Add new students here as they join."
}
```

### Manual Editing
1. Open `student_name_mappings.json` in any text editor
2. Add new mappings in the `"mappings"` section:
   ```json
   "SHORTNAME": "Full Student Name",
   ```
3. Save the file
4. Changes will be loaded next time the application starts

## Workflow for Adding New Students Each Month

### Recommended Workflow:

1. **At Month End:**
   - Open Student Manager (👥 Manage Students)
   - Click "Export to Excel"
   - This creates a backup of current students

2. **When New Students Join:**
   - Add new students to the Excel file you exported
   - OR create a small CSV with just the new students

3. **Import Updated List:**
   - Click "Import from Excel" (or CSV)
   - Select your updated file
   - App will show "Added: X new students"

4. **Re-process Transactions (if needed):**
   - If you've already loaded this month's CSV, say "Yes" to re-process
   - All student names will be updated automatically

5. **Save Changes:**
   - Click "Save Changes" button
   - Mappings are now permanently saved!

### Alternative: Quick Add Individual Students
- Edit any name directly in the table
- Click Save Changes
- Done!

## Matching Logic

The system uses smart matching with 4 strategies (in order):

1. **Exact match**: `"SUNDARA P"` matches `"SUNDARA P"`
2. **Case-insensitive**: `"sundara p"` matches `"SUNDARA P"`  
3. **Space-removed**: `"SUNDARA P"` matches `"SUNDARAP"` ✅
4. **Space-removed + case-insensitive**: `"sundara p"` matches `"SUNDARAP"`

This means you can add mappings with or without spaces, and it will still work!

## Sample File

Use `sample_student_names.csv` as a template:
```csv
Short Name,Full Student Name
SUNDARAP,Dhanalakshmi V
MEENAKAI,Meena Kailash
MRSVNJ,V N Jayanthi
NEWSTUDENT,New Student Full Name
```

## Tips for Success

✅ **Use the UI** - Easier and safer than manual JSON editing
✅ **Export regularly** - Keep backups before making big changes  
✅ **Import incrementally** - Add new students without losing existing ones
✅ **Re-process when needed** - Update transaction names after importing
✅ **Check the count** - "Total Students" shows how many mappings you have

## Troubleshooting

### Import not working?
- Check CSV/Excel has exactly 2 columns
- First row can be headers (like "Short Name, Full Name")
- Make sure file encoding is UTF-8

### Student name not being recognized?
1. Check the exact short name in the bank statement CSV
2. Add that exact short name to your student list
3. OR use a space-removed version (e.g., "SUNDARAP" for "SUNDARA P")
4. Import the updated list and re-process transactions

### Changes not saving?
- Make sure you click "Save Changes" button
- Check for error messages in the dialog
- Try exporting first to verify your changes

### Need to start fresh?
1. Export to Excel (backup your current list)
2. Delete unwanted students one by one
3. Save changes
4. OR manually edit `student_name_mappings.json`

## Benefits of This System

🎯 **No Code Changes Required** - Non-technical users can manage students
📊 **Excel Integration** - Work in familiar tools
🔄 **Incremental Updates** - Add new students without losing existing ones  
💾 **Auto-save** - Changes persist across sessions
🔍 **Smart Matching** - Handles spaces and case variations automatically
🔁 **Re-processing** - Update existing transactions with new names

## Support

If you encounter issues:
1. Check this guide first
2. Try exporting to verify your current data
3. Look for error messages in the application
4. Keep backups before making major changes!
