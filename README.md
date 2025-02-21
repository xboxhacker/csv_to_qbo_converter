# CSV to QBO Converter and Viewer

This Python script provides a graphical user interface (GUI) to convert CSV files to QuickBooks-compatible QBO files and view the contents of QBO files in a human-readable format.

## Features

- **CSV to QBO Conversion**: Convert CSV files containing transaction data into QBO format for import into QuickBooks Desktop.
- **QBO Viewer**: Open and display QBO files in a readable format, showing account details and transaction information.
- **User-Friendly GUI**: Built with tkinter, featuring file selection dialogs and a scrollable text area for viewing.
- **Custom Output Naming**: Allows users to specify the output QBO filename and location.

## Requirements

- Python 3.x
- tkinter (usually included with Python)

No additional libraries are required beyond the Python standard library.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/xboxhacker/csv-to-qbo-converter.git

## Usage
1. Convert CSV to QBO:
- Click "Convert CSV to QBO"
- Select your CSV file in the file dialog
- Choose a name and location for the output QBO file
- Success or error messages will appear accordingly
  
2. View QBO File:
- Click "View QBO File"
- Select a QBO file to open
- View the formatted contents in the text area
- Expected CSV Format

# The CSV file should have the following columns:

- 	`Date` (MM/DD/YYYY format)
- 	`Description` (transaction description)
- 	`Amount` (numeric, can include commas as thousand separators)
- 	`Memo`(optional)
