#!/usr/bin/env python3
"""
Music Class Fee Tracker
A GUI application to categorize and track student fees from bank statements
"""

import sys
import csv
import re
import json
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QFileDialog,
    QLabel, QGroupBox, QHeaderView, QMessageBox, QLineEdit, QComboBox,
    QDialog, QFormLayout, QDialogButtonBox, QDoubleSpinBox, QGridLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor

# Import student name mappings
from student_mappings import get_full_name


class EditTransactionDialog(QDialog):
    """Dialog for editing a transaction"""
    
    def __init__(self, transaction, available_categories, parent=None):
        super().__init__(parent)
        self.transaction = transaction
        self.available_categories = available_categories
        self.setWindowTitle("Edit Transaction")
        self.setModal(True)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the dialog UI"""
        layout = QFormLayout(self)
        
        # Name field (read-only)
        self.name_label = QLabel(self.transaction['name'])
        layout.addRow("Name:", self.name_label)
        
        # Date field (read-only)
        self.date_label = QLabel(self.transaction['date'])
        layout.addRow("Date:", self.date_label)
        
        # Amount field (editable)
        self.amount_spinbox = QDoubleSpinBox()
        self.amount_spinbox.setRange(0, 999999)
        self.amount_spinbox.setDecimals(2)
        self.amount_spinbox.setValue(self.transaction['amount'])
        self.amount_spinbox.setPrefix("₹")
        layout.addRow("Amount:", self.amount_spinbox)
        
        # Category field (editable)
        self.category_combo = QComboBox()
        self.category_combo.addItems(self.available_categories)
        self.category_combo.setCurrentText(self.transaction['category'])
        layout.addRow("Category:", self.category_combo)
        
        # Dialog buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
    
    def get_updated_transaction(self):
        """Return the updated transaction data"""
        return {
            **self.transaction,
            'amount': self.amount_spinbox.value(),
            'category': self.category_combo.currentText()
        }


class FeeTrackerApp(QMainWindow):
    """Main application window for fee tracking"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Music Class Fee Tracker")
        self.setGeometry(100, 100, 1400, 800)
        
        # Load categories from JSON file
        self.categories = self.load_categories()
        
        # Data storage - build categorized_data dynamically
        self.transactions = []
        self.categorized_data = {}
        for cat in self.categories:
            category_key = self.get_category_key(cat['name'], cat['fee'])
            self.categorized_data[category_key] = []
        
        self.init_ui()
    
    def load_categories(self):
        """Load categories from JSON configuration file"""
        config_file = Path(__file__).parent / 'fee_categories.json'
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data['categories']
        except FileNotFoundError:
            # Return default categories if file doesn't exist
            return [
                {"name": "Namasankeerthanam", "fee": 502.0},
                {"name": "Shloka Class", "fee": 503.0},
                {"name": "Rishabhaa Class", "fee": 750.0},
                {"name": "Donations", "fee": None}
            ]
        except Exception as e:
            QMessageBox.warning(self, "Warning", f"Error loading categories: {e}\nUsing defaults.")
            return [
                {"name": "Namasankeerthanam", "fee": 502.0},
                {"name": "Shloka Class", "fee": 503.0},
                {"name": "Rishabhaa Class", "fee": 750.0},
                {"name": "Donations", "fee": None}
            ]
    
    def get_category_key(self, name, fee):
        """Generate a consistent category key for storage"""
        if fee is not None:
            return f"{name} (₹{fee:.0f})"
        else:
            return name
        
    def init_ui(self):
        """Initialize the user interface"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("🎵 Music Class Fee Tracker")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # File selection area
        file_layout = QHBoxLayout()
        self.file_label = QLabel("No file selected")
        self.file_label.setStyleSheet("padding: 10px; background-color: #f0f0f0; border-radius: 5px; color: #212121;")
        file_layout.addWidget(self.file_label, 1)
        
        upload_btn = QPushButton("📁 Upload CSV File")
        upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        upload_btn.clicked.connect(self.upload_file)
        file_layout.addWidget(upload_btn)
        
        main_layout.addLayout(file_layout)
        
        # Summary statistics
        self.summary_group = QGroupBox("Summary")
        self.summary_layout = QGridLayout()
        self.summary_layout.setSpacing(10)
        
        # Create dynamic summary labels based on categories
        self.category_labels = {}
        summary_font = QFont()
        summary_font.setPointSize(11)
        summary_font.setBold(True)
        
        # Calculate how many items per row (let's do 4 per row for good spacing)
        items_per_row = 4
        row = 0
        col = 0
        
        for cat in self.categories:
            category_key = self.get_category_key(cat['name'], cat['fee'])
            label = QLabel(f"{cat['name']}: 0 entries (₹0)")
            label.setFont(summary_font)
            label.setStyleSheet("padding: 10px; background-color: #e3f2fd; border-radius: 5px; color: #1a237e;")
            self.category_labels[category_key] = label
            
            # Add to grid layout
            self.summary_layout.addWidget(label, row, col)
            col += 1
            if col >= items_per_row:
                col = 0
                row += 1
                if row >= 2:  # Maximum 2 rows
                    break
        
        self.summary_group.setLayout(self.summary_layout)
        main_layout.addWidget(self.summary_group)
        
        # Search toggle button
        self.search_toggle_btn = QPushButton("🔍 Show Search")
        self.search_toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: #9C27B0;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #7B1FA2;
            }
        """)
        self.search_toggle_btn.clicked.connect(self.toggle_search)
        main_layout.addWidget(self.search_toggle_btn)
        
        # Search functionality (collapsible)
        self.search_group = QGroupBox("Search Transactions")
        search_layout = QHBoxLayout()
        
        # Search field dropdown
        search_label = QLabel("Search by:")
        search_layout.addWidget(search_label)
        
        self.search_field_combo = QComboBox()
        self.search_field_combo.addItems(["All", "Name", "Amount", "Category", "Description"])
        self.search_field_combo.setStyleSheet("""
            QComboBox {
                padding: 5px;
                border: 2px solid #2196F3;
                border-radius: 5px;
                min-width: 120px;
            }
        """)
        search_layout.addWidget(self.search_field_combo)
        
        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter search term...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #2196F3;
                border-radius: 5px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 2px solid #1976D2;
            }
        """)
        self.search_input.textChanged.connect(self.perform_search)
        search_layout.addWidget(self.search_input, 1)
        
        # Clear search button
        clear_btn = QPushButton("✕ Clear")
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        clear_btn.clicked.connect(self.clear_search)
        search_layout.addWidget(clear_btn)
        
        # Search results label
        self.search_results_label = QLabel("")
        self.search_results_label.setStyleSheet("color: #1976D2; font-weight: bold; padding: 5px;")
        search_layout.addWidget(self.search_results_label)
        
        self.search_group.setLayout(search_layout)
        self.search_group.setVisible(False)  # Hidden by default
        main_layout.addWidget(self.search_group)
        
        # Table for displaying categorized data
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Date", "Name", "Amount (₹)", "Category", "Description", "Reference", "Edit", "Delete"
        ])
        
        # Set table properties
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)
        
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QTableWidget {
                gridline-color: #d0d0d0;
            }
            QTableWidget::item {
                padding: 5px;
            }
        """)
        
        main_layout.addWidget(self.table)
        
        # Total amount section (below table)
        total_layout = QHBoxLayout()
        total_layout.addStretch()
        
        self.total_label = QLabel("Total: ₹0")
        total_font = QFont()
        total_font.setPointSize(14)
        total_font.setBold(True)
        self.total_label.setFont(total_font)
        self.total_label.setStyleSheet("""
            padding: 15px 30px; 
            background-color: #fff9c4; 
            border-radius: 5px; 
            border: 2px solid #fbc02d; 
            color: #f57f17;
        """)
        total_layout.addWidget(self.total_label)
        total_layout.addStretch()
        
        main_layout.addLayout(total_layout)
        
        # Export button
        export_btn = QPushButton("💾 Export Summary")
        export_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)
        export_btn.clicked.connect(self.export_summary)
        main_layout.addWidget(export_btn)
        
    def upload_file(self):
        """Handle file upload and processing"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Bank Statement CSV",
            str(Path.home()),
            "CSV Files (*.csv *.CSV);;All Files (*)"
        )
        
        if file_path:
            try:
                self.process_csv(file_path)
                self.file_label.setText(f"File: {Path(file_path).name}")
                QMessageBox.information(self, "Success", "File processed successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to process file:\n{str(e)}")
    
    def process_csv(self, file_path):
        """Process the CSV file and categorize transactions"""
        self.transactions = []
        # Rebuild categorized_data dynamically from categories
        self.categorized_data = {}
        for cat in self.categories:
            category_key = self.get_category_key(cat['name'], cat['fee'])
            self.categorized_data[category_key] = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        # Find where the transaction data starts
        start_idx = 0
        for i, line in enumerate(lines):
            if 'Txn Date' in line and 'Credit' in line:
                start_idx = i + 1
                break
        
        # Process transactions
        for line in lines[start_idx:]:
            if not line.strip() or line.strip().startswith(','):
                continue
                
            # Parse the CSV line
            parts = self.parse_csv_line(line)
            
            if len(parts) >= 8:
                try:
                    # Extract transaction details
                    txn_date = parts[0].strip().strip('="').strip('"')
                    description = parts[3].strip().strip('="').strip('"')
                    credit = parts[6].strip().strip('="').strip('"').replace(',', '')
                    
                    if not credit or credit == '':
                        continue
                    
                    # Convert credit to float
                    amount = float(credit)
                    
                    # Extract short name from description (format: UPI/CR/xxx/NAME/...)
                    short_name = self.extract_name(description)
                    
                    # Get full name from mapping
                    full_name = get_full_name(short_name)
                    
                    # Categorize based on amount
                    category = self.categorize_transaction(amount)
                    
                    transaction = {
                        'date': txn_date,
                        'name': full_name,  # Use full name
                        'short_name': short_name,  # Keep short name for reference
                        'amount': amount,
                        'category': category,
                        'description': description,
                        'reference': parts[2].strip().strip('="').strip('"')
                    }
                    
                    self.transactions.append(transaction)
                    self.categorized_data[category].append(transaction)
                    
                except (ValueError, IndexError) as e:
                    # Skip invalid lines
                    continue
        
        self.update_display()
    
    def parse_csv_line(self, line):
        """Parse a CSV line handling the special format with = signs"""
        # This CSV uses ="" format for escaping, but also has regular "quoted" fields
        parts = []
        current = ""
        in_quotes = False
        
        i = 0
        while i < len(line):
            char = line[i]
            
            if char == '=' and i + 1 < len(line) and line[i + 1] == '"':
                # Start of a quoted field with ="" format
                i += 2
                field = ""
                while i < len(line):
                    if line[i] == '"' and (i + 1 >= len(line) or line[i + 1] in [',', '\n', '\r']):
                        break
                    field += line[i]
                    i += 1
                parts.append(field)
                i += 1  # Skip the closing quote
                # Skip the comma if present
                if i < len(line) and line[i] == ',':
                    i += 1
            elif char == '"' and not in_quotes:
                # Start of a regular quoted field
                in_quotes = True
                i += 1
            elif char == '"' and in_quotes:
                # End of a regular quoted field
                in_quotes = False
                parts.append(current)
                current = ""
                i += 1
                # Skip the comma if present
                if i < len(line) and line[i] == ',':
                    i += 1
            elif char == ',':
                if not in_quotes:
                    # Field separator (only when not in quotes)
                    parts.append(current)
                    current = ""
                    i += 1
                else:
                    # Comma inside quotes - part of the field value
                    current += char
                    i += 1
            else:
                current += char
                i += 1
        
        # Append the last field if any
        if current or in_quotes:
            parts.append(current)
        
        return parts
    
    def extract_name(self, description):
        """Extract name from UPI description"""
        # Format: UPI/CR/xxxxx/NAME/BANK/...
        parts = description.split('/')
        if len(parts) >= 4:
            name = parts[3].strip()
            # Clean up name
            name = re.sub(r'\s+', ' ', name)
            return name
        return "Unknown"
    
    def categorize_transaction(self, amount):
        """Categorize transaction based on amount using JSON config"""
        # Try to match with a fixed fee category
        for cat in self.categories:
            if cat['fee'] is not None and amount == cat['fee']:
                return self.get_category_key(cat['name'], cat['fee'])
        
        # If no match, use the first category with fee = null (variable amount)
        for cat in self.categories:
            if cat['fee'] is None:
                return self.get_category_key(cat['name'], cat['fee'])
        
        # Fallback (shouldn't happen if Donations exists)
        return "Uncategorized"
    
    def get_display_category(self, category):
        """Get category name without amount for display"""
        # Remove amount in brackets for cleaner display
        if '(₹' in category:
            return category.split(' (₹')[0]
        return category
    
    def update_display(self):
        """Update the table and summary with categorized data"""
        # Clear table
        self.table.setRowCount(0)
        
        # Generate dynamic color mapping for all categories
        color_palette = [
            (QColor(200, 230, 201), QColor(27, 94, 32)),   # Light green / Dark green
            (QColor(187, 222, 251), QColor(13, 71, 161)),  # Light blue / Dark blue
            (QColor(255, 224, 178), QColor(230, 81, 0)),   # Light orange / Dark orange
            (QColor(248, 187, 208), QColor(136, 14, 79)),  # Light pink / Dark pink
            (QColor(225, 190, 231), QColor(74, 20, 140)),  # Light purple / Dark purple
            (QColor(255, 245, 157), QColor(245, 127, 23)), # Light yellow / Dark yellow
        ]
        
        colors = {}
        text_colors = {}
        for idx, category_key in enumerate(self.categorized_data.keys()):
            bg_color, fg_color = color_palette[idx % len(color_palette)]
            colors[category_key] = bg_color
            text_colors[category_key] = fg_color
        
        # Populate table by category (iterate dynamically)
        row = 0
        for category_key in self.categorized_data.keys():
            for transaction in self.categorized_data[category_key]:
                self.table.insertRow(row)
                
                # Add data to cells
                self.table.setItem(row, 0, QTableWidgetItem(transaction['date']))
                self.table.setItem(row, 1, QTableWidgetItem(transaction['name']))
                
                amount_item = QTableWidgetItem(f"₹{transaction['amount']:.2f}")
                amount_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.table.setItem(row, 2, amount_item)
                
                # Display category without amount
                display_category = self.get_display_category(transaction['category'])
                category_item = QTableWidgetItem(display_category)
                category_item.setBackground(colors[transaction['category']])
                category_item.setForeground(text_colors[transaction['category']])
                category_item.setTextAlignment(Qt.AlignCenter)
                category_item.setFont(QFont("", -1, QFont.Bold))
                self.table.setItem(row, 3, category_item)
                
                desc_item = QTableWidgetItem(transaction['description'][:50] + "..." 
                                            if len(transaction['description']) > 50 
                                            else transaction['description'])
                self.table.setItem(row, 4, desc_item)
                
                self.table.setItem(row, 5, QTableWidgetItem(transaction['reference']))
                
                # Add Edit button
                edit_btn = QPushButton("✏️")
                edit_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #FF9800;
                        color: white;
                        padding: 5px 8px;
                        border-radius: 3px;
                        font-weight: bold;
                        font-size: 14px;
                    }
                    QPushButton:hover {
                        background-color: #F57C00;
                    }
                """)
                edit_btn.setToolTip("Edit transaction")
                edit_btn.clicked.connect(lambda checked, t=transaction: self.edit_transaction(t))
                self.table.setCellWidget(row, 6, edit_btn)
                
                # Add Delete button
                delete_btn = QPushButton("🗑️")
                delete_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #f44336;
                        color: white;
                        padding: 5px 8px;
                        border-radius: 3px;
                        font-weight: bold;
                        font-size: 14px;
                    }
                    QPushButton:hover {
                        background-color: #da190b;
                    }
                """)
                delete_btn.setToolTip("Delete transaction")
                delete_btn.clicked.connect(lambda checked, t=transaction: self.delete_transaction(t))
                self.table.setCellWidget(row, 7, delete_btn)
                
                row += 1
        
        # Update summary
        self.update_summary()
    
    def update_summary(self):
        """Update summary statistics dynamically"""
        # Color palette for categories
        colors = ['#c8e6c9', '#bbdefb', '#ffe0b2', '#f8bbd0', '#e1bee7', '#fff9c4']
        text_colors = ['#1b5e20', '#0d47a1', '#e65100', '#880e4f', '#4a148c', '#f57f17']
        
        total_amount = 0
        
        # Update each category label dynamically
        for idx, (category_key, label) in enumerate(self.category_labels.items()):
            count = len(self.categorized_data.get(category_key, []))
            cat_total = sum(t['amount'] for t in self.categorized_data.get(category_key, []))
            total_amount += cat_total
            
            # Get category name (without amount)
            cat_name = category_key.split(' (₹')[0] if '(₹' in category_key else category_key
            
            label.setText(f"{cat_name}: {count} entries (₹{cat_total:.2f})")
            
            # Update colors based on whether there are entries
            bg_color = colors[idx % len(colors)] if count > 0 else '#e3f2fd'
            fg_color = text_colors[idx % len(text_colors)] if count > 0 else '#1a237e'
            
            label.setStyleSheet(
                f"padding: 10px; background-color: {bg_color}; border-radius: 5px; color: {fg_color};"
            )
        
        # Update total
        self.total_label.setText(f"Total: ₹{total_amount:.2f}")
        self.total_label.setStyleSheet(
            "padding: 10px; background-color: #fff9c4; border-radius: 5px; border: 2px solid #fbc02d; color: #f57f17;"
        )
    
    def perform_search(self):
        """Perform search based on selected field and search term"""
        search_term = self.search_input.text().strip().lower()
        search_field = self.search_field_combo.currentText()
        
        if not search_term:
            # If search is empty, show all transactions
            self.update_display()
            self.search_results_label.setText("")
            return
        
        # Clear table
        self.table.setRowCount(0)
        
        # Generate dynamic color mapping for all categories (same as update_display)
        color_palette = [
            (QColor(200, 230, 201), QColor(27, 94, 32)),   # Light green / Dark green
            (QColor(187, 222, 251), QColor(13, 71, 161)),  # Light blue / Dark blue
            (QColor(255, 224, 178), QColor(230, 81, 0)),   # Light orange / Dark orange
            (QColor(248, 187, 208), QColor(136, 14, 79)),  # Light pink / Dark pink
            (QColor(225, 190, 231), QColor(74, 20, 140)),  # Light purple / Dark purple
            (QColor(255, 245, 157), QColor(245, 127, 23)), # Light yellow / Dark yellow
        ]
        
        colors = {}
        text_colors = {}
        for idx, category_key in enumerate(self.categorized_data.keys()):
            bg_color, fg_color = color_palette[idx % len(color_palette)]
            colors[category_key] = bg_color
            text_colors[category_key] = fg_color
        
        # Filter transactions based on search criteria
        filtered_transactions = []
        for transaction in self.transactions:
            match = False
            
            if search_field == "All":
                # Search in all fields
                if (search_term in transaction['name'].lower() or
                    search_term in transaction['category'].lower() or
                    search_term in transaction['description'].lower() or
                    search_term in str(transaction['amount'])):
                    match = True
            elif search_field == "Name":
                if search_term in transaction['name'].lower():
                    match = True
            elif search_field == "Amount":
                # Allow partial amount matching
                if search_term in str(transaction['amount']):
                    match = True
            elif search_field == "Category":
                if search_term in transaction['category'].lower():
                    match = True
            elif search_field == "Description":
                if search_term in transaction['description'].lower():
                    match = True
            
            if match:
                filtered_transactions.append(transaction)
        
        # Display filtered transactions
        row = 0
        for transaction in filtered_transactions:
            self.table.insertRow(row)
            
            # Add data to cells
            self.table.setItem(row, 0, QTableWidgetItem(transaction['date']))
            self.table.setItem(row, 1, QTableWidgetItem(transaction['name']))
            
            amount_item = QTableWidgetItem(f"₹{transaction['amount']:.2f}")
            amount_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row, 2, amount_item)
            
            # Display category without amount
            display_category = self.get_display_category(transaction['category'])
            category_item = QTableWidgetItem(display_category)
            category_item.setBackground(colors[transaction['category']])
            category_item.setForeground(text_colors[transaction['category']])
            category_item.setTextAlignment(Qt.AlignCenter)
            category_item.setFont(QFont("", -1, QFont.Bold))
            self.table.setItem(row, 3, category_item)
            
            desc_item = QTableWidgetItem(transaction['description'][:50] + "..." 
                                        if len(transaction['description']) > 50 
                                        else transaction['description'])
            self.table.setItem(row, 4, desc_item)
            
            self.table.setItem(row, 5, QTableWidgetItem(transaction['reference']))
            
            # Add Edit button
            edit_btn = QPushButton("✏️")
            edit_btn.setStyleSheet("""
                QPushButton {
                    background-color: #FF9800;
                    color: white;
                    padding: 5px 8px;
                    border-radius: 3px;
                    font-weight: bold;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #F57C00;
                }
            """)
            edit_btn.setToolTip("Edit transaction")
            edit_btn.clicked.connect(lambda checked, t=transaction: self.edit_transaction(t))
            self.table.setCellWidget(row, 6, edit_btn)
            
            # Add Delete button
            delete_btn = QPushButton("🗑️")
            delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: #f44336;
                    color: white;
                    padding: 5px 8px;
                    border-radius: 3px;
                    font-weight: bold;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #da190b;
                }
            """)
            delete_btn.setToolTip("Delete transaction")
            delete_btn.clicked.connect(lambda checked, t=transaction: self.delete_transaction(t))
            self.table.setCellWidget(row, 7, delete_btn)
            
            row += 1
        
        # Update search results label
        total = len(self.transactions)
        found = len(filtered_transactions)
        self.search_results_label.setText(f"Found {found} of {total} transactions")
    
    def toggle_search(self):
        """Toggle the visibility of the search section"""
        if self.search_group.isVisible():
            self.search_group.setVisible(False)
            self.search_toggle_btn.setText("🔍 Show Search")
            # Clear search when hiding
            self.clear_search()
        else:
            self.search_group.setVisible(True)
            self.search_toggle_btn.setText("🔍 Hide Search")
            # Focus on search input when showing
            self.search_input.setFocus()
    
    def clear_search(self):
        """Clear search and show all transactions"""
        self.search_input.clear()
        self.search_field_combo.setCurrentIndex(0)
        self.update_display()
        self.search_results_label.setText("")
    
    def edit_transaction(self, transaction):
        """Edit a transaction"""
        # Get list of available categories for the dropdown
        available_categories = list(self.categorized_data.keys())
        dialog = EditTransactionDialog(transaction, available_categories, self)
        if dialog.exec() == QDialog.Accepted:
            # Get updated values
            new_amount = dialog.amount_spinbox.value()
            new_category = dialog.category_combo.currentText()
            old_category = transaction['category']
            
            # Update the transaction object in place (more efficient)
            transaction['amount'] = new_amount
            
            # Only update category if it changed
            if old_category != new_category:
                # Remove from old category
                self.categorized_data[old_category].remove(transaction)
                # Add to new category
                self.categorized_data[new_category].append(transaction)
                # Update category in transaction
                transaction['category'] = new_category
            
            # Refresh display
            self.update_display()
    
    def delete_transaction(self, transaction):
        """Delete a transaction"""
        # Confirm deletion
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete this transaction?\n\n"
            f"Name: {transaction['name']}\n"
            f"Amount: ₹{transaction['amount']:.2f}\n"
            f"Date: {transaction['date']}",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Remove from main transactions list (more efficient)
            self.transactions.remove(transaction)
            
            # Remove from categorized data
            category = transaction['category']
            self.categorized_data[category].remove(transaction)
            
            # Refresh display
            self.update_display()
    
    def export_summary(self):
        """Export summary to a text file"""
        if not self.transactions:
            QMessageBox.warning(self, "No Data", "Please upload a CSV file first.")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Summary",
            str(Path.home() / "fee_summary.txt"),
            "Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("=" * 80 + "\n")
                    f.write("MUSIC CLASS FEE TRACKER - SUMMARY REPORT\n")
                    f.write("=" * 80 + "\n\n")
                    
                    # Export all categories dynamically
                    for category_key in self.categorized_data.keys():
                        transactions = self.categorized_data[category_key]
                        total = sum(t['amount'] for t in transactions)
                        
                        f.write(f"\n{category_key}\n")
                        f.write("-" * 80 + "\n")
                        f.write(f"Total: {len(transactions)} entries | Amount: ₹{total:.2f}\n\n")
                        
                        for t in transactions:
                            f.write(f"  • {t['name']:<25} | ₹{t['amount']:>8.2f} | {t['date']}\n")
                        
                        f.write("\n")
                    
                    total_amount = sum(t['amount'] for t in self.transactions)
                    f.write("=" * 80 + "\n")
                    f.write(f"GRAND TOTAL: ₹{total_amount:.2f}\n")
                    f.write("=" * 80 + "\n")
                
                QMessageBox.information(self, "Success", f"Summary exported to:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export summary:\n{str(e)}")


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    window = FeeTrackerApp()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
