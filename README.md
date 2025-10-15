# Credit Card Statement Parser

A Flask-based web application that extracts structured data from credit card statement PDFs.
![Preview](https://github.com/Tejaswi410/Credit-Card-Statement-parser/blob/main/Screenshot%202025-10-14%20221806.png)

## Features

- 🏦 Supports 5 major Indian banks: HDFC, ICICI, AXIS, KOTAK, and SBI
- 🔄 Updated to replace IDFC First Bank and Syndicate Bank with Axis Bank and SBI
- 📄 Extracts key data points:
  - Cardholder Name
  - Card Number (masked)
  - Statement Date
  - Payment Due Date
  - Total Amount Due
  - Minimum Amount Due
  - Credit Limit
  - Transaction History
- 🎨 Clean, responsive Bootstrap UI
- 📱 Mobile-friendly design
- 🔒 Secure file handling (files are deleted after processing)
- ⚡ Fast parsing with instant results
- 📊 JSON export functionality

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Steps

1. Clone or download the project files

2. Create a virtual environment (recommended):
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

```
credit-card-parser/
│
├── app.py                 # Flask application and routes
├── parser.py              # PDF parsing logic and field extraction
├── requirements.txt       # Python dependencies
├── README.md             # This file
│
├── templates/
│   └── index.html        # Web interface
│
├── credit card statements/  # Sample credit card statements for testing
│   ├── hdfc-statement.pdf
│
└── uploads/              # Temporary file storage (auto-created)
```

## Usage

1. Start the Flask server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Upload a credit card statement PDF:
   - Click the upload zone or drag and drop a PDF file
   - Click "Parse Statement"
   - View extracted information instantly

4. Results include:
   - Detected bank provider
   - Confidence score
   - All extracted fields (name, card details, dates, amounts, transactions)
   - Raw JSON data (with copy functionality)

## How It Works

### Parser Logic (`parser.py`)

1. **Text Extraction**: Uses `pdfplumber` to extract text from PDFs
2. **Provider Detection**: Identifies the bank based on text patterns
3. **Field Extraction**: Uses regex patterns to extract specific fields:
   - **Cardholder Name**: Matches patterns like "Dear [NAME]", "Cardholder: [NAME]", or concatenated names
   - **Card Number**: Finds masked card numbers (XXXX XXXX XXXX 1234, 1234XXXXXXXX5678)
   - **Statement Date**: Extracts statement generation dates
   - **Payment Due Date**: Finds payment deadline dates
   - **Amount Due**: Locates total and minimum amount due with currency symbols
   - **Credit Limit**: Extracts available credit limit information
   - **Transactions**: Parses transaction history with dates, descriptions, and amounts

### Supported Patterns

The parser handles various date and amount formats:
- Dates: `DD/MM/YYYY`, `DD-MM-YYYY`, `Month DD, YYYY`
- Amounts: `Rs. 1,234.00`, `INR 1234`, `₹1,234`
- Card numbers: `XXXX XXXX XXXX 1234`, `************1234`


## Troubleshooting

### Issue: "Could not extract text from PDF"
- **Solution**: The PDF might be image-based. Consider adding OCR support with `pytesseract`

### Issue: Fields showing "Not Found"
- **Solution**: The statement format might be different. Add more regex patterns in `parser.py`

### Issue: Port 5000 already in use
- **Solution**: Change port in `app.py`:
  ```python
  app.run(debug=True, port=5001)
  ```

## Testing

Test with sample statements from:
- HDFC Bank
- ICICI Bank
- AXIS Bank
- KOTAK Mahindra Bank
- SBI Cards

## Limitations

- Only supports text-based PDFs (not scanned images)
- Requires consistent statement formats
- May need pattern updates for new statement layouts


## License

This project is for educational purposes. Ensure compliance with data privacy regulations when handling financial documents.

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review regex patterns in `parser.py`
3. Test with different statement formats

---
