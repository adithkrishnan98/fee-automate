# 📂 Category Management System

## Overview
The Music Class Fee Tracker now includes a complete category management system that allows you to:
- ✅ Add new fee categories
- ✅ Edit existing categories  
- ✅ Delete categories
- ✅ Persist categories between app sessions
- ✅ Auto-recategorize transactions when categories change

## How It Works

### 1. **Accessing Category Management**
- **Menu Bar**: Go to `Categories → Manage Categories`
- **Keyboard**: Use the menu bar navigation

### 2. **Adding New Categories**
1. Open the Category Manager
2. Enter a **Category Name** (e.g., "Piano Lessons")
3. Set the **Fixed Amount** (e.g., ₹600) or set to 0 for variable amounts
4. Click **"Add Category"**

### 3. **Editing Categories**
1. Select a category from the list
2. Modify the name or amount
3. Click **"Update Category"**

### 4. **Deleting Categories**
1. Select a category from the list
2. Click **"Delete"** 
3. Confirm the deletion

### 5. **Category Types**

#### Fixed Amount Categories (💰)
- **Purpose**: For classes with consistent fees
- **Example**: "Violin Lessons (₹500)"
- **Auto-categorization**: Transactions matching the exact amount are automatically categorized

#### Variable Amount Categories (📊)  
- **Purpose**: For donations, variable payments, etc.
- **Example**: "Donations (Variable Amount)"
- **Auto-categorization**: Transactions that don't match any fixed amount go here

## Data Persistence

### Storage Location
Categories are stored in: `fee_categories.json`

### Sample File Structure
```json
{
  "categories": [
    {
      "name": "Namasankeerthanam",
      "fee": 502.0
    },
    {
      "name": "Shloka Class", 
      "fee": 503.0
    },
    {
      "name": "Donations",
      "fee": null
    }
  ]
}
```

### Backup & Recovery
- **Automatic Backup**: The app creates the JSON file if it doesn't exist
- **Manual Backup**: Copy `fee_categories.json` to save your categories
- **Recovery**: Replace the JSON file to restore categories

## Auto-Recategorization

When you modify categories, the app automatically:
1. **Rebuilds** the category structure
2. **Re-categorizes** all existing transactions
3. **Updates** the display with new categories
4. **Preserves** your transaction data

## Best Practices

### 1. **Category Naming**
- Use clear, descriptive names
- Be consistent with naming conventions
- Examples: "Piano Lessons", "Guitar Class", "Music Theory"

### 2. **Amount Setting**
- Set **exact amounts** for regular class fees
- Use **0 or null** for variable amounts (donations, special payments)
- Review amounts periodically for fee changes

### 3. **Category Organization**
- Keep the number of categories manageable (5-10 is ideal)
- Group similar activities under broader categories
- Use consistent fee structures

### 4. **Data Management**
- **Regular Backups**: Export your `fee_categories.json` file periodically
- **Testing**: Test category changes with sample data first
- **Documentation**: Keep notes on what each category represents

## Workflow Example

### First-Time Setup
1. Start the application
2. Go to `Categories → Manage Categories`
3. Add your specific music classes:
   - "Piano Lessons" → ₹600
   - "Guitar Classes" → ₹550  
   - "Music Theory" → ₹400
   - "Donations" → ₹0 (variable)
4. Save and close

### Adding New Classes Mid-Year
1. Go to `Categories → Manage Categories`
2. Add "Violin Lessons" → ₹650
3. Save - existing transactions remain unchanged
4. New violin transactions will auto-categorize

### Fee Changes
1. Edit the existing category amount
2. Click "Update Category"  
3. All transactions will re-categorize automatically
4. Review the results

## Troubleshooting

### Categories Not Saving
- Check file permissions in the application directory
- Ensure `fee_categories.json` is not read-only
- Try running as administrator if needed

### Transactions Not Re-categorizing  
- Use `Categories → Refresh Categories` 
- Check if amounts match exactly
- Verify category configuration

### Missing Categories After Restart
- Check if `fee_categories.json` exists
- Verify file is not corrupted (valid JSON format)
- Restore from backup if needed

## Technical Details

### File Format
- **Format**: JSON
- **Encoding**: UTF-8
- **Location**: Same directory as application
- **Auto-creation**: Yes, with default categories

### Category Matching Logic
1. **Exact Match**: Transaction amount = category fee → Auto-assign
2. **No Match**: Transaction goes to first variable amount category
3. **Fallback**: "Uncategorized" if no variable category exists

### Performance
- Categories load on startup
- Changes save immediately
- Re-categorization is instant for normal dataset sizes
- Optimized for 100s-1000s of transactions

---

**💡 Tip**: Start with a few basic categories and expand as needed. The system is designed to grow with your requirements!