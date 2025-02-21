import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import csv
from datetime import datetime

# Create the main window
root = tk.Tk()
root.title("CSV to QBO Converter and Viewer")
root.geometry("600x400")

def open_csv_file():
    """Open file dialog to select CSV and start conversion"""
    input_path = filedialog.askopenfilename(
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        title="Select CSV File to Convert"
    )
    if input_path:
        output_path = filedialog.asksaveasfilename(
            defaultextension=".qbo",
            filetypes=[("QBO files", "*.qbo"), ("All files", "*.*")],
            initialfile="converted_output.qbo",
            title="Save QBO File As"
        )
        if output_path:
            try:
                convert_to_qbo(input_path, output_path)
                messagebox.showinfo("Success", "QBO file has been created successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

def convert_to_qbo(csv_path, output_path):
    """Convert CSV to QBO format"""
    bankid = "123456789"  # Bank routing number
    acctid = "987654321"  # Account number
    
    qbo_content = [
        "OFXHEADER:100",
        "DATA:OFXSGML",
        "VERSION:102",
        "SECURITY:NONE",
        "ENCODING:USASCII",
        "CHARSET:1252",
        "COMPRESSION:NONE",
        "OLDFILEUID:NONE",
        "NEWFILEUID:NONE",
        "<OFX>",
        "<BANKMSGSRSV1>",
        "<STMTTRNRS>",
        "<TRNUID>1001",
        "<STMTRS>",
        "<CURDEF>USD",
        f"<BANKACCTFROM>",
        f"<BANKID>{bankid}",
        f"<ACCTID>{acctid}",
        "<ACCTTYPE>CHECKING",
        "</BANKACCTFROM>",
    ]
    
    with open(csv_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                trans_date = datetime.strptime(row['Date'], '%m/%d/%Y')
                date_str = trans_date.strftime('%Y%m%d')
                amount_str = row['Amount'].replace(',', '')
                amount = float(amount_str)
                trntype = 'DEBIT' if amount < 0 else 'CREDIT'
                fitid = f"{date_str}{abs(hash(row['Description']))}"
                
                qbo_content.extend([
                    "<STMTTRN>",
                    f"<TRNTYPE>{trntype}",
                    f"<DTPOSTED>{date_str}",
                    f"<TRNAMT>{amount}",
                    f"<FITID>{fitid}",
                    f"<NAME>{row['Description']}",
                    f"<MEMO>{row.get('Memo', '')}",
                    "</STMTTRN>",
                ])
            except KeyError as e:
                raise Exception(f"Missing required column: {str(e)}")
            except ValueError as e:
                raise Exception(f"Invalid data format: {str(e)}")
    
    qbo_content.extend([
        "</STMTRS>",
        "</STMTTRNRS>",
        "</BANKMSGSRSV1>",
        "</OFX>",
    ])
    
    with open(output_path, 'w', encoding='utf-8') as qbo_file:
        qbo_file.write('\n'.join(qbo_content))

def view_qbo_file():
    """Open and display QBO file contents"""
    qbo_path = filedialog.askopenfilename(
        filetypes=[("QBO files", "*.qbo"), ("All files", "*.*")],
        title="Select QBO File to View"
    )
    if qbo_path:
        try:
            with open(qbo_path, 'r', encoding='utf-8') as qbo_file:
                lines = qbo_file.readlines()
            
            # Initialize display text
            display_text = "QBO File Contents:\n"
            display_text += f"File: {qbo_path}\n\n"
            
            # Default values
            bank_id = "Unknown"
            acct_id = "Unknown"
            acct_type = "Unknown"
            transactions = []
            current_trans = {}
            in_transaction = False
            
            # Parse the QBO file
            for line in lines:
                line = line.strip()
                if line.startswith("<BANKID>"):
                    bank_id = line[7:]
                elif line.startswith("<ACCTID>"):
                    acct_id = line[7:]
                elif line.startswith("<ACCTTYPE>"):
                    acct_type = line[9:]
                elif line == "<STMTTRN>":
                    in_transaction = True
                    current_trans = {}
                elif line == "</STMTTRN>" and in_transaction:
                    in_transaction = False
                    transactions.append(current_trans)
                elif in_transaction and line.startswith("<") and not line.startswith("</"):
                    tag = line[1:line.index('>')]
                    value = line[line.index('>')+1:]
                    current_trans[tag] = value
            
            # Build display text
            display_text += f"Bank Routing Number: {bank_id}\n"
            display_text += f"Account Number: {acct_id}\n"
            display_text += f"Account Type: {acct_type}\n\n"
            
            if transactions:
                display_text += "Transactions:\n" + "-"*50 + "\n"
                for trans in transactions:
                    date_str = trans.get('DTPOSTED', '')
                    try:
                        date = datetime.strptime(date_str, '%Y%m%d').strftime('%m/%d/%Y')
                    except ValueError:
                        date = "Unknown"
                    
                    amount = float(trans.get('TRNAMT', '0.00'))
                    display_text += (
                        f"Date: {date}\n"
                        f"Type: {trans.get('TRNTYPE', 'Unknown')}\n"
                        f"Amount: ${amount:,.2f}\n"
                        f"Description: {trans.get('NAME', 'Unknown')}\n"
                        f"Memo: {trans.get('MEMO', '')}\n"
                        f"Transaction ID: {trans.get('FITID', 'Unknown')}\n"
                        f"{'-'*50}\n"
                    )
            else:
                display_text += "No transactions found in the QBO file.\n"
            
            # Update text area
            text_area.config(state='normal')  # Enable editing
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, display_text)
            text_area.config(state='disabled')  # Make read-only
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not read QBO file: {str(e)}")

# Create GUI elements
label = tk.Label(root, text="CSV to QBO Converter and Viewer", pady=10)
label.pack()

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

convert_button = tk.Button(button_frame, text="Convert CSV to QBO", command=open_csv_file)
convert_button.pack(side=tk.LEFT, padx=5)

view_button = tk.Button(button_frame, text="View QBO File", command=view_qbo_file)
view_button.pack(side=tk.LEFT, padx=5)

instructions = tk.Label(root, text="Convert: Select a CSV file\nView: Open a QBO file\nCSV format: Date (MM/DD/YYYY), Description, Amount, [Memo]", 
                       justify="center")
instructions.pack(pady=10)

text_area = scrolledtext.ScrolledText(root, width=70, height=15, state='disabled')
text_area.pack(pady=10)

# Start the GUI
root.mainloop()
