# 📚 Bookkeeper CLI

A powerful command-line bookkeeping tool written in Python that helps you manage your financial records efficiently using a local SQLite database.

## ✨ Features

- 📝 Record financial transactions with detailed information
  - Date
  - Amount
  - Category
  - Notes
- 🔄 Smart duplicate detection
  - Prevents duplicate entries based on date, amount, and category
- ✅ Category validation
  - Ensures consistent categorization of transactions
- 📊 Data Export
  - Export all records to Excel format
- 📈 Comprehensive Reporting
  - Generate detailed reports for any date range
  - View transaction listings
  - Category-wise summaries
  - Total amount calculations

## 🛠️ Installation

1. Clone the repository:
```bash
git clone git@github.com:zealchen/bookeeper.git
cd bookkeeper
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 📖 Usage

### 1. Initialize Database
```bash
python main.py.py init-db --db-path my.db
```
> Note: If not specified, the database will be created as `my.db` in the current directory

### 2. Import Records
```bash
python main.py.py import-record \
  --date 2025-06-03 \
  --amount 15.99 \
  --category Food \
  --note "Lunch at restaurant" \
  --db-path my.db
```

#### Available Categories:
- Food
- Transport
- Housing
- Utilities
- Entertainment
- Shopping
- Healthcare
- Education
- Other

### 3. Export Records
```bash
python main.py.py export-records --output my_records.xlsx --db-path my.db
```

### 4. Generate Reports
```bash
python main.py.py report \
  --start 2025-06-01 \
  --end 2025-06-30 \
  --db-path my.db
```

#### Report Contents:
- Detailed transaction table (formatted with PrettyTable)
- Category-wise summaries
- Total amount for the period

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.