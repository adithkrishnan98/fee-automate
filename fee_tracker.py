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
    QDialog, QFormLayout, QDialogButtonBox, QDoubleSpinBox, QGridLayout,
    QCheckBox
)
from PySide6.QtCore import Qt, QTimer
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
        
        # Search optimization
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.perform_search)
        self.search_delay = 150  # milliseconds - faster response
        self.color_cache = {}  # Cache for color mappings
        
        # Selection state tracking
        self.selected_transactions = set()  # Track selected transaction IDs
        self._manual_selection_panel_open = False  # Track manual panel state
        self._updating_display = False  # Prevent concurrent updates
        
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
    
    def get_transaction_id(self, transaction):
        """Generate a unique ID for a transaction"""
        return f"{transaction['date']}_{transaction['name']}_{transaction['amount']}_{transaction['reference']}"
        
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
        self.search_input.textChanged.connect(self.on_search_text_changed)
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
        
        # Selection toggle button
        self.selection_toggle_btn = QPushButton("✅ Show Selection Tools")
        self.selection_toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.selection_toggle_btn.clicked.connect(self.toggle_selection_panel)
        main_layout.addWidget(self.selection_toggle_btn)
        
        # Selection Controls Panel
        self.selection_group = QGroupBox("")
        selection_layout = QHBoxLayout()
        
        # Selection controls (Select All button hidden for now)
        
        self.clear_selection_btn = QPushButton("☐ Clear Selection")
        self.clear_selection_btn.setStyleSheet("""
            QPushButton {
                background-color: #757575;
                color: white;
                padding: 8px 15px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #616161;
            }
        """)
        self.clear_selection_btn.clicked.connect(self.clear_selection)
        selection_layout.addWidget(self.clear_selection_btn)
        
        # Separator
        selection_layout.addWidget(QLabel("|"))
        
        # Selection info
        self.selection_label = QLabel("Selected: 0 transactions")
        self.selection_label.setStyleSheet("font-weight: bold; color: #1976D2; padding: 8px;")
        selection_layout.addWidget(self.selection_label)
        
        # Spacer
        selection_layout.addStretch()
        
        # Action buttons
        self.edit_selected_btn = QPushButton("✏️ Edit Selected")
        self.edit_selected_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                padding: 8px 15px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
            QPushButton:disabled {
                background-color: #BDBDBD;
            }
        """)
        self.edit_selected_btn.setEnabled(False)
        self.edit_selected_btn.clicked.connect(self.edit_selected_transactions)
        selection_layout.addWidget(self.edit_selected_btn)
        
        self.delete_selected_btn = QPushButton("🗑️ Delete Selected")
        self.delete_selected_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 8px 15px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
            QPushButton:disabled {
                background-color: #BDBDBD;
            }
        """)
        self.delete_selected_btn.setEnabled(False)
        self.delete_selected_btn.clicked.connect(self.delete_selected_transactions)
        selection_layout.addWidget(self.delete_selected_btn)
        
        self.selection_group.setLayout(selection_layout)
        self.selection_group.setVisible(False)  # Hidden by default
        main_layout.addWidget(self.selection_group)
        
        # Table for displaying categorized data
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "☐", "Date", "Name", "Amount (₹)", "Category", "Description", "Reference"
        ])
        
        # Set table properties
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)             # Checkbox column - Fixed width
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Date
        header.setSectionResizeMode(2, QHeaderView.Stretch)           # Name
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Amount
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Category
        header.setSectionResizeMode(5, QHeaderView.Stretch)           # Description
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # Reference
        
        # Set fixed width for checkbox column (50 pixels should be enough)
        self.table.setColumnWidth(0, 50)
        
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
        # Prevent concurrent updates
        if self._updating_display:
            return
        
        self._updating_display = True
        
        try:
            # Clear color cache to regenerate for any category changes
            self.color_cache.clear()
            
            # Clear selection since row indices will change
            self.selected_transactions.clear()
            self._manual_selection_panel_open = False
            
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
                    
                    # Add checkbox for selection
                    checkbox_widget = QWidget()
                    checkbox_layout = QHBoxLayout(checkbox_widget)
                    checkbox = QCheckBox()
                    transaction_id = self.get_transaction_id(transaction)
                    checkbox.setChecked(transaction_id in self.selected_transactions)
                    checkbox.toggled.connect(lambda checked, tid=transaction_id: self.on_checkbox_toggled(tid, checked))
                    checkbox_layout.addWidget(checkbox)
                    checkbox_layout.setAlignment(Qt.AlignCenter)
                    checkbox_layout.setContentsMargins(0, 0, 0, 0)
                    self.table.setCellWidget(row, 0, checkbox_widget)
                
                    # Add data to cells (shifted by 1 column)
                    self.table.setItem(row, 1, QTableWidgetItem(transaction['date']))
                    self.table.setItem(row, 2, QTableWidgetItem(transaction['name']))
                    
                    amount_item = QTableWidgetItem(f"₹{transaction['amount']:.2f}")
                    amount_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    self.table.setItem(row, 3, amount_item)
                    
                    # Display category without amount
                    display_category = self.get_display_category(transaction['category'])
                    category_item = QTableWidgetItem(display_category)
                    category_item.setBackground(colors[transaction['category']])
                    category_item.setForeground(text_colors[transaction['category']])
                    category_item.setTextAlignment(Qt.AlignCenter)
                    category_item.setFont(QFont("", -1, QFont.Bold))
                    self.table.setItem(row, 4, category_item)
                    
                    desc_item = QTableWidgetItem(transaction['description'][:50] + "..." 
                                                if len(transaction['description']) > 50 
                                                else transaction['description'])
                    self.table.setItem(row, 5, desc_item)
                    
                    self.table.setItem(row, 6, QTableWidgetItem(transaction['reference']))
                    
                    row += 1
        
            # Update summary and selection UI
            self.update_summary()
            self.update_selection_ui()
            
        finally:
            self._updating_display = False
    
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
    
    def on_search_text_changed(self):
        """Handle search text changes with debouncing"""
        self.search_timer.stop()  # Stop any existing timer
        self.search_timer.start(self.search_delay)  # Start new timer
    
    def perform_search(self):
        """Optimized search with caching and efficient filtering"""
        search_term = self.search_input.text().strip().lower()
        search_field = self.search_field_combo.currentText()
        
        if not search_term:
            # If search is empty, show all transactions
            self.update_display()
            self.search_results_label.setText("")
            return
        
        # Cache color mapping to avoid regeneration
        if not self.color_cache:
            self._generate_color_cache()
        
        # Fast filtering using list comprehension
        filtered_transactions = self._filter_transactions_fast(search_term, search_field)
        
        # Efficient table update
        self._update_table_efficiently(filtered_transactions)
        
        # Update search results label
        total = len(self.transactions)
        found = len(filtered_transactions)
        self.search_results_label.setText(f"Found {found} of {total} transactions")
    
    def _generate_color_cache(self):
        """Generate and cache color mappings once"""
        color_palette = [
            (QColor(200, 230, 201), QColor(27, 94, 32)),   # Light green / Dark green
            (QColor(187, 222, 251), QColor(13, 71, 161)),  # Light blue / Dark blue
            (QColor(255, 224, 178), QColor(230, 81, 0)),   # Light orange / Dark orange
            (QColor(248, 187, 208), QColor(136, 14, 79)),  # Light pink / Dark pink
            (QColor(225, 190, 231), QColor(74, 20, 140)),  # Light purple / Dark purple
            (QColor(255, 245, 157), QColor(245, 127, 23)), # Light yellow / Dark yellow
        ]
        
        self.color_cache = {'colors': {}, 'text_colors': {}}
        for idx, category_key in enumerate(self.categorized_data.keys()):
            bg_color, fg_color = color_palette[idx % len(color_palette)]
            self.color_cache['colors'][category_key] = bg_color
            self.color_cache['text_colors'][category_key] = fg_color
    
    def _filter_transactions_fast(self, search_term, search_field):
        """Fast transaction filtering using optimized logic"""
        if search_field == "All":
            return [t for t in self.transactions if (
                search_term in t['name'].lower() or
                search_term in t['category'].lower() or
                search_term in t['description'].lower() or
                search_term in str(t['amount'])
            )]
        elif search_field == "Name":
            return [t for t in self.transactions if search_term in t['name'].lower()]
        elif search_field == "Amount":
            return [t for t in self.transactions if search_term in str(t['amount'])]
        elif search_field == "Category":
            return [t for t in self.transactions if search_term in t['category'].lower()]
        elif search_field == "Description":
            return [t for t in self.transactions if search_term in t['description'].lower()]
        return []
    
    def _update_table_efficiently(self, filtered_transactions):
        """Efficiently update table without recreating widgets unnecessarily"""
        # Clear table contents but preserve structure
        self.table.setRowCount(len(filtered_transactions))
        
        colors = self.color_cache['colors']
        text_colors = self.color_cache['text_colors']
        
        # Batch table updates for better performance
        for row, transaction in enumerate(filtered_transactions):
            # Add checkbox for selection  
            checkbox_widget = QWidget()
            checkbox_layout = QHBoxLayout(checkbox_widget)
            checkbox = QCheckBox()
            transaction_id = self.get_transaction_id(transaction)
            checkbox.setChecked(transaction_id in self.selected_transactions)
            checkbox.toggled.connect(lambda checked, tid=transaction_id: self.on_checkbox_toggled(tid, checked))
            checkbox_layout.addWidget(checkbox)
            checkbox_layout.setAlignment(Qt.AlignCenter)
            checkbox_layout.setContentsMargins(0, 0, 0, 0)
            self.table.setCellWidget(row, 0, checkbox_widget)
            
            # Set basic data (shifted by 1 column)
            self.table.setItem(row, 1, QTableWidgetItem(transaction['date']))
            self.table.setItem(row, 2, QTableWidgetItem(transaction['name']))
            
            # Amount with alignment
            amount_item = QTableWidgetItem(f"₹{transaction['amount']:.2f}")
            amount_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row, 3, amount_item)
            
            # Category with cached colors
            display_category = self.get_display_category(transaction['category'])
            category_item = QTableWidgetItem(display_category)
            category_item.setBackground(colors[transaction['category']])
            category_item.setForeground(text_colors[transaction['category']])
            category_item.setTextAlignment(Qt.AlignCenter)
            category_item.setFont(QFont("", -1, QFont.Bold))
            self.table.setItem(row, 4, category_item)
            
            # Description (truncated)
            desc_text = (transaction['description'][:50] + "..." 
                        if len(transaction['description']) > 50 
                        else transaction['description'])
            self.table.setItem(row, 5, QTableWidgetItem(desc_text))
            
            self.table.setItem(row, 6, QTableWidgetItem(transaction['reference']))
    

    def on_checkbox_toggled(self, transaction_id, checked):
        """Handle checkbox toggle (most reliable signal)"""
        if checked:
            self.selected_transactions.add(transaction_id)
        else:
            self.selected_transactions.discard(transaction_id)
        
        self.update_selection_ui()
        
    def on_checkbox_state_changed(self, checkbox, transaction_id):
        """Handle checkbox state changes (simplified)"""
        is_checked = checkbox.isChecked()
        
        if is_checked:
            self.selected_transactions.add(transaction_id)
        else:
            self.selected_transactions.discard(transaction_id)
        
        self.update_selection_ui()
    
    def on_checkbox_changed(self, transaction_id, transaction, state):
        """Handle checkbox state changes (legacy - keeping for compatibility)"""
        if state == Qt.Checked:
            self.selected_transactions.add(transaction_id)
        else:
            self.selected_transactions.discard(transaction_id)
        
        self.update_selection_ui()
    
    def get_visible_transactions(self):
        """Get currently visible transactions in table order"""
        visible = []
        for row in range(self.table.rowCount()):
            # Get transaction data from table
            name = self.table.item(row, 2).text() if self.table.item(row, 2) else ""
            amount_text = self.table.item(row, 3).text() if self.table.item(row, 3) else ""
            
            # Find matching transaction
            for transaction in self.transactions:
                if (transaction['name'] == name and 
                    f"₹{transaction['amount']:.2f}" == amount_text):
                    visible.append(transaction)
                    break
        return visible
    
    def select_all_transactions(self):
        """Select all visible transactions"""
        visible_transactions = self.get_visible_transactions()
        
        for transaction in visible_transactions:
            transaction_id = self.get_transaction_id(transaction)
            self.selected_transactions.add(transaction_id)
        
        # Update all checkboxes
        for row in range(self.table.rowCount()):
            checkbox_widget = self.table.cellWidget(row, 0)
            if checkbox_widget:
                checkbox = checkbox_widget.findChild(QCheckBox)
                if checkbox:
                    checkbox.setChecked(True)
        
        self.update_selection_ui()
    
    def clear_selection(self):
        """Clear all selections"""
        self.selected_transactions.clear()
        
        # Update all checkboxes
        for row in range(self.table.rowCount()):
            checkbox_widget = self.table.cellWidget(row, 0)
            if checkbox_widget:
                checkbox = checkbox_widget.findChild(QCheckBox)
                if checkbox:
                    checkbox.setChecked(False)
        
        # Reset manual flag when clearing
        self._manual_selection_panel_open = False
        self.update_selection_ui()
    
    def update_selection_ui(self):
        """Update selection-related UI elements"""
        count = len(self.selected_transactions)
        
        self.selection_label.setText(f"Selected: {count} transactions")
        
        # Enable/disable action buttons based on selection
        has_selection = count > 0
        self.edit_selected_btn.setEnabled(has_selection)
        self.delete_selected_btn.setEnabled(has_selection)
        
        # Select all button is hidden for now - no updates needed
        
        # Smart accordion behavior
        self.auto_toggle_selection_panel(has_selection)
    
    def toggle_selection_panel(self):
        """Manually toggle the selection panel visibility"""
        if self.selection_group.isVisible():
            self.hide_selection_panel_manually()
        else:
            self.show_selection_panel_manually()
    
    def auto_toggle_selection_panel(self, has_selection):
        """Automatically show/hide selection panel based on selections"""
        if has_selection and not self.selection_group.isVisible():
            # Auto-show when selections are made
            self.selection_group.setVisible(True)
            self.selection_toggle_btn.setText("❌ Hide Selection Tools")
        elif not has_selection and self.selection_group.isVisible():
            # Auto-hide when no selections, but respect manual override
            if not self._manual_selection_panel_open:
                self.selection_group.setVisible(False)
                self.selection_toggle_btn.setText("✅ Show Selection Tools")
        
        # Reset manual flag when selections exist (user is actively using selection)
        if has_selection:
            self._manual_selection_panel_open = False
    
    def show_selection_panel_manually(self):
        """Show selection panel and mark as manually opened"""
        self._manual_selection_panel_open = True
        self.selection_group.setVisible(True)
        self.selection_toggle_btn.setText("❌ Hide Selection Tools")
    
    def hide_selection_panel_manually(self):
        """Hide selection panel and clear manual flag"""
        self._manual_selection_panel_open = False
        self.selection_group.setVisible(False)
        self.selection_toggle_btn.setText("✅ Show Selection Tools")
    
    def get_selected_transactions(self):
        """Get the actual transaction objects for selected transactions"""
        selected = []
        for transaction in self.transactions:
            transaction_id = self.get_transaction_id(transaction)
            if transaction_id in self.selected_transactions:
                selected.append(transaction)
        return selected
    
    def edit_selected_transactions(self):
        """Edit selected transactions"""
        selected = self.get_selected_transactions()
        if not selected:
            QMessageBox.information(self, "No Selection", "Please select transactions to edit.")
            return
        
        if len(selected) == 1:
            # Edit single transaction
            self.edit_transaction(selected[0])
        else:
            # Bulk edit - show dialog for category change
            self.bulk_edit_transactions(selected)
    
    def bulk_edit_transactions(self, transactions):
        """Show bulk edit dialog for multiple transactions"""
        from PySide6.QtWidgets import QInputDialog
        
        # Get available categories
        categories = list(self.categorized_data.keys())
        
        # Show category selection dialog
        category, ok = QInputDialog.getItem(
            self, 
            "Bulk Edit", 
            f"Change category for {len(transactions)} transactions:",
            categories, 
            0, 
            False
        )
        
        if ok and category:
            # Apply category change to all selected transactions
            for transaction in transactions:
                old_category = transaction['category']
                if old_category != category:
                    # Remove from old category
                    if transaction in self.categorized_data[old_category]:
                        self.categorized_data[old_category].remove(transaction)
                    # Add to new category
                    self.categorized_data[category].append(transaction)
                    # Update transaction
                    transaction['category'] = category
            
            # Refresh display
            self.update_display()
            QMessageBox.information(
                self, 
                "Success", 
                f"Updated {len(transactions)} transactions to {category.split(' (₹')[0]}"
            )
    
    def delete_selected_transactions(self):
        """Delete selected transactions with confirmation"""
        selected = self.get_selected_transactions()
        if not selected:
            QMessageBox.information(self, "No Selection", "Please select transactions to delete.")
            return
        
        # Confirmation dialog
        reply = QMessageBox.question(
            self, 
            "Confirm Deletion", 
            f"Are you sure you want to delete {len(selected)} selected transactions?\n\nThis action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Remove from categorized data and main transactions list
            for transaction in selected:
                # Remove from selection tracking
                transaction_id = self.get_transaction_id(transaction)
                self.selected_transactions.discard(transaction_id)
                
                # Remove from category
                category = transaction['category']
                if transaction in self.categorized_data[category]:
                    self.categorized_data[category].remove(transaction)
                # Remove from main list
                if transaction in self.transactions:
                    self.transactions.remove(transaction)
            
            # Clear selection and refresh display
            self.clear_selection()
            self.update_display()
            
            QMessageBox.information(
                self, 
                "Deleted", 
                f"Successfully deleted {len(selected)} transactions."
            )

    def set_search_delay(self, delay_ms):
        """Adjust search delay (useful for performance tuning)"""
        self.search_delay = delay_ms
    
    def toggle_search(self):
        """Toggle the visibility of the search section"""
        if self.search_group.isVisible():
            # Stop any pending search operations immediately
            self.search_timer.stop()
            
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
        # Stop any pending search operations
        self.search_timer.stop()
        
        # Check if there was actually a search term to clear
        had_search_term = bool(self.search_input.text().strip())
        
        self.search_input.clear()
        self.search_field_combo.setCurrentIndex(0)
        self.search_results_label.setText("")
        
        # Only update display if there was a search active (optimization)
        if had_search_term:
            self.update_display()
    
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
