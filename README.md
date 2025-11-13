# Music Class Fee Tracker

A Python GUI application built with PySide6 to automate fee calculation and categorization for music class students from bank statement CSV files.

## Features

### 🎯 Core Features

✨ **Dynamic Category Management**
- Add, edit, and delete categories with custom fees through GUI
- Categories automatically saved to `fee_categories.json` and persist across sessions
- Support for both fixed-fee and variable-amount categories
- Automatic recategorization when categories change
- Duplicate detection for category names and fee amounts
- Real-time validation and error handling

👥 **Student Name Management**
- Complete CRUD operations for student mappings
- **Add Students**: One-by-one through dialog or bulk import via CSV/Excel
- **Search Students**: Real-time filtering by short name or full name
- **Edit Students**: Modify both short names and full names with duplicate checking
- **Delete Students**: Remove students with confirmation dialog
- **Import/Export**: CSV and Excel support for bulk operations
- **Fuzzy Matching**: 4-strategy name matching (exact, case-insensitive, space-removed, combined)
- Student mappings stored in `student_name_mappings.json`
- Auto-creates template file on fresh install with examples
- Sample CSV template included for easy bulk imports

✏️ **Transaction Management**
- **Edit Transactions**: Modify date, name, amount, and category for any transaction
- **Delete Transactions**: Remove unwanted transactions with confirmation
- **Duplicate Transactions**: Create copies for recurring payments
- **Bulk Operations**: Select multiple transactions for batch editing or deletion
- **Auto-save**: Changes automatically saved to JSON file for persistence
- **Re-process**: Automatically recategorize all transactions after student list updates

📊 **Advanced Search & Display**
- **Collapsible Search Panel**: Toggle on/off to save screen space
- **Multi-field Search**: Search by Name, Amount, Category, Description, or All fields
- **Real-time Filtering**: Instant results with debouncing (150ms) for performance
- **Result Counter**: Shows number of matching transactions
- **Color-coded Display**: Category-based color coding in table view
- **Checkbox Selection**: Select individual transactions for bulk operations
- **Sortable Columns**: Click headers to sort by any column

💾 **Import/Export Capabilities**
- **CSV Import**: Upload bank statements from CSV files
- **Excel Import**: Support for .xls and .xlsx bank statements
- **Student Import**: Bulk import student names from CSV/Excel
- **Student Export**: Export student list to Excel with formatting
- **Summary Export**: Detailed reports organized by category
- **Auto-save State**: Transaction edits automatically saved and restored

🎨 **User Interface**
- **Modern Design**: Clean, professional interface with Qt6 styling
- **Collapsible Panels**: Search and Selection tools can be hidden
- **Responsive Layout**: Adapts to different screen sizes
- **Visual Feedback**: Success/error messages, loading indicators, auto-save notifications
- **Keyboard Shortcuts**: Quick access to common operations
- **Alternating Row Colors**: Better readability in tables

## Installation

### Prerequisites

1. **Check Python Installation:**
   ```bash
   python3 --version
   ```
   Make sure Python 3.7+ is installed on your system.

### Installing Dependencies

The application requires:
- **PySide6** (>=6.6.0) - Qt6 framework for Python
- **OpenPyXL** (>=3.1.0) - Excel file support (.xlsx)

#### Method 1: Using Virtual Environment (Recommended)

If you encounter an "externally-managed-environment" error when installing packages, use a virtual environment:

1. **Navigate to the project directory:**
   ```bash
   cd path/to/fee-automate
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment:**
   ```bash
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application:**
   ```bash
   python fee_tracker.py
   ```

**Note:** Always activate the virtual environment before running the application:
```bash
source venv/bin/activate  # Then run your scripts
```

#### Method 2: Direct Installation

If you don't encounter the externally-managed-environment error:

```bash
pip install -r requirements.txt
```

Or install packages individually:
```bash
pip install PySide6 openpyxl
```

#### Method 3: Alternative Solutions

If you're still having issues, try one of these alternatives:

**Option A - User Installation:**
```bash
pip3 install --user PySide6
```

**Option B - Using pipx (for application installation):**
```bash
brew install pipx  # On macOS
pipx install PySide6
```

**Option C - Homebrew (macOS only):**
```bash
brew install python-tk  # If available
```

### Troubleshooting Installation Issues

**Problem:** `error: externally-managed-environment`
**Solution:** Use Method 1 (Virtual Environment) above - this is the recommended approach.

**Problem:** `python: command not found`
**Solution:** Use `python3` instead of `python` on macOS/Linux systems.

**Problem:** `pip: command not found`
**Solution:** Use `pip3` instead of `pip`, or install pip: `python3 -m ensurepip --upgrade`

**Problem:** Permission denied errors
**Solution:** Never use `sudo` with pip. Use virtual environment or `--user` flag instead.

## Usage

### Quick Start

1. **Run the application:**
   ```bash
   python3 fee_tracker.py
   ```

2. **First-Time Setup:**
   - On first run, the app creates `fee_categories.json` and `student_name_mappings.json`
   - Default categories are created automatically
   - Student mappings file includes examples and instructions

### Managing Categories

Click **"⚙️ Manage Categories"** to open the category manager:

- **Add Category**: 
  - Click "➕ Add Category"
  - Enter category name (e.g., "Piano Lessons")
  - Enter fee amount (e.g., 500) or 0 for variable amount
  - Click "Add" to save
  
- **Edit Category**: 
  - Select a category from the list
  - Modify name or fee amount
  - Click "✏️ Update Category"
  
- **Delete Category**: 
  - Select a category from the list
  - Click "🗑️ Delete Category"
  - Confirm deletion

**Notes:**
- Each category must have a unique fee amount (for auto-categorization)
- Only one variable-amount category allowed
- Changes persist across sessions
- Transactions automatically recategorize when categories change

### Managing Students

Click **"👥 Manage Students"** to open the student manager:

- **Add Student (One-by-one)**:
  - Click "➕ Add Student"
  - Enter short name (as it appears in bank statements, e.g., "JOHN D")
  - Enter full student name (e.g., "John Doe")
  - Click "Save"

- **Import Students (Bulk)**:
  - **From CSV**: Click "📁 Import from CSV"
    - Select CSV file with two columns: Short Name, Full Student Name
    - Use `sample_student_names.csv` as a template
  - **From Excel**: Click "📊 Import from Excel"
    - Select .xlsx or .xls file with same format
  
- **Search Students**:
  - Type in the search box to filter by short name or full name
  - Click "✕ Clear" to reset search

- **Edit Student**:
  - Click "✏️ Edit" button next to student name
  - Modify short name or full name
  - Click "Save"

- **Delete Student**:
  - Click "🗑️ Delete" button next to student name
  - Confirm deletion

- **Export Students**:
  - Click "💾 Export to Excel"
  - Choose save location
  - Creates formatted Excel file with all student mappings

**Notes:**
- Changes saved to `student_name_mappings.json`
- App asks if you want to re-process transactions after updating students
- Duplicate short names prevented
- Inline editing also available (click cell and type)

### Processing Transactions

1. **Upload Bank Statement:**
   - Click "📁 Upload CSV File"
   - Select your bank statement CSV file
   - Supports both CSV and Excel formats (.xls, .xlsx)
   
2. **Auto-Categorization:**
   - Transactions automatically categorized by matching fee amounts
   - Student names extracted from UPI descriptions
   - Short names matched to full names using fuzzy logic
   - Unmatched amounts go to variable-amount category

3. **View Results:**
   - All transactions displayed in color-coded table
   - Summary shows counts and totals for each category
   - Scroll through table to see all entries

### Editing Transactions

- **Single Edit**:
  - Click any cell to edit inline (except checkbox and action buttons)
  - OR click "✏️ Edit" button for dialog-based editing
  - Modify date, name, amount, or category
  - Changes auto-save

- **Bulk Operations**:
  - Click "✅ Show Selection Tools" to reveal selection panel
  - Check boxes next to transactions to select
  - Use bulk buttons:
    - **✏️ Edit Selected**: Change category for all selected
    - **📋 Duplicate Selected**: Create copies of selected transactions
    - **🗑️ Delete Selected**: Remove multiple transactions at once
  - Click "☐ Clear Selection" to deselect all

### Searching Transactions

1. Click **"🔍 Show Search"** to expand search panel
2. Select search field:
   - **All**: Search across all fields
   - **Name**: Search by student name
   - **Amount**: Search by transaction amount
   - **Category**: Filter by category
   - **Description**: Search in transaction descriptions
3. Type to filter results in real-time
4. Result count shows number of matching transactions
5. Click **"✕ Clear"** to reset search

### Exporting Data

- **Export Summary**:
  - Click "💾 Export Summary"
  - Choose save location and filename
  - Creates text file with transactions organized by category
  - Includes student names and amounts

- **Export Students**:
  - Open Student Manager ("👥 Manage Students")
  - Click "💾 Export to Excel"
  - Creates formatted Excel file with all student mappings

## Configuration Files

The application uses JSON files for configuration and data storage:

### `fee_categories.json`
Stores all fee categories with their amounts:
```json
{
  "categories": [
    {"name": "Piano Lessons", "fee": 500},
    {"name": "Vocal Class", "fee": 600},
    {"name": "Donations", "fee": null}
  ]
}
```
- **Auto-created** on first run with default categories
- `fee: null` or `fee: 0` indicates variable-amount category
- Edit through GUI or manually edit JSON file

### `student_name_mappings.json`
Maps short names from bank statements to full student names:
```json
{
  "mappings": {
    "JOHN D": "John Doe",
    "MARY S": "Mary Smith"
  },
  "_comment": "Student name mappings for the Music Class Fee Tracker",
  "_instructions": "Add student mappings in the format: 'SHORTNAME': 'Full Student Name'"
}
```
- **Auto-created** on first run with template and examples
- Edit through Student Manager GUI or manually
- Supports fuzzy matching (case-insensitive, space-removed)

### Transaction Auto-save
Edits to transactions are automatically saved to:
- `{original_filename}_edits.json`
- Restores your edits when reopening the same CSV file
- Includes transaction data and timestamps

## Student Name Mapping System

The application features an intelligent fuzzy-matching system for student names:

### Matching Strategies (in order):
1. **Exact Match**: Direct lookup (fastest)
2. **Case-Insensitive**: "john d" matches "JOHN D"
3. **Space-Removed**: "JOHND" matches "JOHN D"
4. **Combined**: "johnd" matches "JOHN D" (case-insensitive + space-removed)

### Example:
Bank statement shows: "SUNDARA P" or "SUNDARAP" or "sundara p"  
All map to: "Dhanalakshmi" (if configured in mappings)

### Fallback Behavior:
If no mapping found, displays formatted short name (e.g., "John D" instead of "JOHND")

### Managing Mappings:

**Through GUI (Recommended):**
- Use Student Manager dialog ("👥 Manage Students" button)
- Add, edit, delete students with visual interface
- Import/export bulk data via CSV or Excel
- Search and filter capabilities

**Manual Editing:**
- Edit `student_name_mappings.json` directly
- Restart application to reload changes
- Useful for advanced users or bulk edits

**Bulk Import:**
- Use provided `sample_student_names.csv` as template
- Two columns: Short Name, Full Student Name
- Import via Student Manager dialog

## CSV/Excel Format Support

The application supports multiple bank statement formats:

### Supported File Types:
- **CSV files** (.csv) - Most common format
- **Excel files** (.xlsx, .xls) - Direct Excel support

### Expected Format:
The application is designed for Canara Bank CSV statements but can work with similar formats containing:
- Transaction Date / Txn Date
- Value Date (optional)
- Cheque/Reference Number
- Description (containing UPI details with student names)
- Branch Code (optional)
- Debit
- Credit (amount)
- Balance

### Flexible Column Headers:
- Supports variations like "Txn Date" or "Transaction Date"
- Handles different bank statement formats
- Custom CSV parser manages quoted fields and special characters

### Automatic Processing:
- Extracts student names from UPI transaction descriptions
- Identifies credit amounts
- Categorizes based on fee amount
- Maps short names to full student names
- Handles special CSV formatting (escaped quotes, etc.)

## Performance & Technical Details

### Performance Optimizations:
- **Search Debouncing**: 150ms delay for smooth real-time filtering
- **Color Caching**: Category colors cached for faster rendering
- **Efficient Rendering**: 60 FPS table updates
- **Smart Updates**: Only affected rows updated on changes
- **Background Processing**: Non-blocking UI during file operations

### Technical Stack:
- **Language**: Python 3.7+
- **Framework**: PySide6 6.6.0+ (Qt6 for Python)
- **Excel Support**: OpenPyXL 3.1.0+
- **Architecture**: MVC-inspired with event-driven design
- **Data Storage**: JSON files for configuration and persistence
- **CSV Parsing**: Custom state-machine parser for robust handling

### Code Statistics:
- **Total Lines**: 2,600+ lines of Python code
- **Main Application**: `fee_tracker.py` (2,857 lines)
- **Student Module**: `student_mappings.py` (168 lines)
- **Classes**: 4 main dialog classes
- **Methods**: 50+ methods across all classes

### Key Components:
1. **FeeTrackerApp**: Main application window
2. **CategoryManagerDialog**: Category CRUD operations
3. **StudentManagerDialog**: Student name management
4. **EditTransactionDialog**: Transaction editing interface

### Data Files:
- `fee_categories.json` - Category definitions
- `student_name_mappings.json` - Student name mappings
- `{filename}_edits.json` - Auto-saved transaction edits
- `sample_student_names.csv` - Import template

## Troubleshooting

### Installation Issues

**Issue**: `error: externally-managed-environment`  
**Solution**: Use virtual environment (see Installation Method 1)

**Issue**: `python: command not found`  
**Solution**: Use `python3` instead of `python` on macOS/Linux

**Issue**: `pip: command not found`  
**Solution**: Use `pip3` or install pip: `python3 -m ensurepip --upgrade`

**Issue**: `No module named 'openpyxl'`  
**Solution**: Install OpenPyXL: `pip install openpyxl`

**Issue**: Permission denied errors  
**Solution**: Never use `sudo` with pip. Use virtual environment or `--user` flag

### Application Issues

**Issue**: Application won't start  
**Solutions**:
- Ensure PySide6 is installed: `pip install PySide6`
- Check Python version: `python3 --version` (requires 3.7+)
- Activate virtual environment if using one

**Issue**: CSV/Excel file won't load  
**Solutions**:
- Verify file format matches expected structure
- Check file isn't corrupted or password-protected
- Try saving Excel file as CSV and importing
- Check console output for specific error messages

**Issue**: Student names not showing correctly  
**Solutions**:
- Open Student Manager and verify mappings exist
- Check short name matches exactly (spaces, case)
- Use fuzzy matching by trying variations
- Add missing student through Student Manager

**Issue**: Categories not saving  
**Solutions**:
- Check file permissions in application directory
- Verify `fee_categories.json` isn't read-only
- Try manually creating the file with empty categories
- Check console for write permission errors

**Issue**: Transactions not auto-saving  
**Solutions**:
- Ensure you've loaded a CSV file first
- Check write permissions in the file's directory
- Look for `{filename}_edits.json` file
- Verify disk space is available

**Issue**: Wrong categorization  
**Solutions**:
- Check category fee amounts match transaction amounts exactly
- Verify you have a variable-amount category for unmatched amounts
- Review Category Manager for duplicate fee amounts
- Edit transactions manually if auto-categorization fails

### Data Issues

**Issue**: Lost student mappings after update  
**Solution**: Check `student_name_mappings.json` file exists and isn't empty

**Issue**: Duplicate students in list  
**Solution**: Use Student Manager to search and delete duplicates

**Issue**: Import fails silently  
**Solutions**:
- Check CSV/Excel file has exactly 2 columns
- Verify no merged cells in Excel files
- Ensure data starts from row 1 or has proper headers
- Check for special characters in names

### Getting Help

If issues persist:
1. Check the console output for error messages
2. Verify all dependencies are installed: `pip list | grep -i "pyside6\|openpyxl"`
3. Try with a fresh virtual environment
4. Review configuration JSON files for syntax errors
5. Test with the sample CSV file provided

## Building macOS Application

The project includes scripts to build a standalone macOS application:

### Prerequisites:
```bash
pip install pyinstaller
```

### Build Steps:

1. **Build the application:**
   ```bash
   chmod +x build_app.sh
   ./build_app.sh
   ```

2. **Create DMG installer (optional):**
   ```bash
   chmod +x create_dmg.sh
   ./create_dmg.sh
   ```

### Output:
- **Application**: `dist/FeeTracker.app`
- **DMG Installer**: `FeeTracker.dmg` (if created)

### Distribution:
The standalone app can be distributed to other macOS users without requiring Python installation.

## File Structure

```
fee-automate/
├── fee_tracker.py              # Main application
├── student_mappings.py         # Student name mapping logic
├── fee_categories.json         # Category definitions (auto-generated)
├── student_name_mappings.json  # Student mappings (auto-generated)
├── sample_student_names.csv    # Import template
├── requirements.txt            # Python dependencies
├── fee_tracker.spec           # PyInstaller configuration
├── build_app.sh               # macOS build script
├── create_dmg.sh              # DMG creation script
├── README.md                  # This file
├── CATEGORY_MANAGEMENT.md     # Category management guide
├── MAPPING_GUIDE.md           # Student mapping guide
└── STUDENT_MAPPINGS_GUIDE.md  # Student manager documentation
```

## Documentation

Additional documentation available:
- **CATEGORY_MANAGEMENT.md** - Detailed category management guide
- **MAPPING_GUIDE.md** - Student name mapping system guide  
- **STUDENT_MAPPINGS_GUIDE.md** - Comprehensive student manager documentation

## License

Free to use and modify for personal and educational purposes.

---

## Recent Updates

### Version 2.0 (November 2025)
- ✅ Complete Student Manager with CRUD operations
- ✅ Search and filter functionality for students
- ✅ CSV/Excel import and export for student lists
- ✅ Fuzzy name matching with 4 strategies
- ✅ Auto-save transaction edits
- ✅ Bulk transaction operations
- ✅ Enhanced search with multi-field filtering
- ✅ Collapsible UI panels
- ✅ Excel file support for bank statements
- ✅ Auto-create template files on fresh install

### Version 1.0
- Initial release with basic categorization
- CSV file parsing
- Category management
- Transaction editing
- Export functionality

---

**Created for music class fee management** 🎵  
**Maintained with ❤️ by the development team**
