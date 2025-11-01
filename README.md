# Music Class Fee Tracker

A Python GUI application built with PySide6 to automate fee calculation and categorization for music class students from bank statement CSV files.

## Features

s✨ **Dynamic Category Management**
- Add, edit, and delete categories with custom fees
- Categories automatically saved and persist across sessions
- Support for both fixed-fee and variable-amount categories
- Automatic recategorization when categories change

✏️ **Edit & Delete Transactions**
- Edit button for each transaction row
- Modify amounts and categories on the fly
- Delete unwanted transactions with confirmation
- Automatic recalculation of totals after changes

📊 **Visual Display**
- Color-coded categorization in table view
- Dynamic summary statistics with counts and totals
- Easy-to-read tabular format
- Full student names displayed (mapped from short names)
- Automatically adapts to any number of categories

🔍 **Search Functionality**
- Collapsible search panel
- Search by: Name, Amount, Category, or Description
- Real-time filtering with result counts

👤 **Student Name Mapping**
- Automatic conversion of short names to full names
- Customizable mapping in `student_mappings.py`
- Easy to update and maintain

💾 **Export Functionality**
- Export detailed summary reports to text files
- Organized by category with student names and amounts
- Dynamic export adapts to your categories

## Installation

1. Make sure Python 3.7+ is installed on your system

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or install PySide6 directly:
```bash
pip install PySide6
```

## Usage

1. **Run the application:**
```bash
python fee_tracker.py
```

2. **Manage Categories (New!):**
   - Click "⚙️ Manage Categories" to open the category manager
   - **Add Category**: Click "➕ Add Category", enter name and fee amount
   - **Edit Category**: Select a category, click "✏️ Edit Category"
   - **Delete Category**: Select a category, click "🗑️ Delete Category"
   - Categories are automatically saved and persist across sessions
   - Enter 0 for fee to create a variable-amount category (like Donations)

3. **Upload CSV file:**
   - Click the "📁 Upload CSV File" button
   - Select your bank statement CSV file
   - The application will automatically process and categorize all transactions
   - Transactions are categorized based on matching fee amounts

4. **View Results:**
   - All transactions are displayed in the table with color-coded categories
   - Summary section shows counts and totals for each category
   - Scroll through the table to see all entries
   - Summary dynamically updates based on your categories

5. **Edit or Delete Transactions:**
   - Click "✏️ Edit" on any row to modify amount or category
   - Click "🗑️ Delete" to remove a transaction (with confirmation)
   - Totals automatically recalculate after changes

6. **Search Transactions:**
   - Click "🔍 Show Search" to expand the search panel
   - Select search field (All, Name, Amount, Category, or Description)
   - Type to filter results in real-time
   - Click "✕ Clear" to reset

7. **Export Summary:**
   - Click "💾 Export Summary" to save a detailed report
   - Choose location and filename
   - Report includes all entries organized by category

## Category Management

The application now supports dynamic category management, making it fully scalable for any number of classes or fee structures.

### How Categories Work:

1. **Fixed-Fee Categories**: Enter a specific amount (e.g., ₹502)
   - Transactions matching this exact amount are automatically categorized

2. **Variable-Amount Categories**: Enter 0 as the fee
   - Acts as a catch-all for amounts that don't match any fixed fee
   - Perfect for donations or miscellaneous payments

3. **Category Files**: Categories are stored in `categories.json`
   - Automatically created on first run with default categories
   - Persists across application restarts
   - Can be manually edited if needed

### Default Categories:
- Namasankeerthanam: ₹502
- Shloka Class: ₹503
- Rishabhaa Class: ₹750
- Donations: Variable amount

## Student Name Mapping

The application automatically converts short names from bank statements to full student names using the `student_mappings.py` file.

### Editing Student Names:

1. **Open the mapping file:**
   ```bash
   # Edit with any text editor
   open student_mappings.py
   ```

2. **Update the dictionary:**
   ```python
   STUDENT_NAME_MAPPINGS = {
       "MEENAKSHI": "Meenakshi Sundaram",  # Short name: Full name
       "Mrs V N J": "Mrs V N Jayalakshmi",
       # Add or edit entries here
   }
   ```

3. **Save and restart the application**

The application will automatically use the updated names when processing CSV files.

## CSV Format

The application is designed to work with Canara Bank CSV statements with the following format:
- Transaction Date
- Value Date
- Cheque/Reference Number
- Description (containing UPI details with student names)
- Branch Code
- Debit
- Credit (amount)
- Balance

The application automatically:
- Extracts student names from UPI descriptions
- Maps short names to full student names
- Identifies credit amounts
- Categorizes based on the fee amount
- Displays organized results with full names

## Class Categories

| Class | Fee Amount | Color |
|-------|------------|-------|
| Namasankeerthanam | ₹502 | 🟢 Light Green |
| Shloka Class | ₹503 | 🔵 Light Blue |
| Rishabhaa Class | ₹750 | 🟠 Light Orange |
| Donations | Other amounts | 🔴 Light Pink |

## Screenshots

### Main Window
The main window displays:
- File upload button at the top
- Summary statistics showing count and totals for each batch
- Detailed table with all transactions color-coded by category
- Export button to save summaries

### Features
- **Sortable columns**: Click column headers to sort
- **Alternating row colors**: For better readability
- **Responsive layout**: Adjusts to window size
- **Error handling**: Clear messages for any issues

## Troubleshooting

**Issue**: Application won't start
- **Solution**: Ensure PySide6 is installed: `pip install PySide6`

**Issue**: CSV file won't load
- **Solution**: Make sure the CSV file is in the correct format (Canara Bank statement)

**Issue**: Names not showing correctly
- **Solution**: Edit the `student_mappings.py` file to add or update name mappings

**Issue**: Wrong full name displayed
- **Solution**: Find the short name in `student_mappings.py` and update the corresponding full name

## Technical Details

- **Framework**: PySide6 (Qt for Python)
- **Language**: Python 3.7+
- **CSV Parsing**: Custom parser to handle Canara Bank's special CSV format (with `=""` escaping and quoted fields)
- **Name Mapping**: Automatic lookup system for converting short names to full names
- **GUI**: Modern, user-friendly interface with color coding and collapsible search

## Customization

### Fee Amounts
To modify fee amounts, edit these constants in `fee_tracker.py`:

```python
BATCH_A_FEE = 502  # Namasankeerthanam fee
BATCH_B_FEE = 503  # Shloka Class fee
BATCH_C_FEE = 750  # Rishabhaa Class fee
```

### Student Names
To add or update student names, edit `student_mappings.py`:

```python
BATCH_A_FEE = 502  # Change to your Batch A fee
BATCH_B_FEE = 503  # Change to your Batch B fee
BATCH_C_FEE = 750  # Change to your Batch C fee
```

## License

Free to use and modify for personal and educational purposes.

## Support

For issues or questions, please check:
1. CSV file format matches Canara Bank statements
2. PySide6 is properly installed
3. Python version is 3.7 or higher

---

**Created for music class fee management** 🎵
