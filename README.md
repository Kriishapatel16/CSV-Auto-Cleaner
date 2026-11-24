# CSV Auto Cleaner

### Clean messy data. Keep the good stuff.

**CSV Auto Cleaner** is a privacy-focused web application designed to help users analyze, clean, validate, and transform datasets without manually editing spreadsheets or writing complex data-cleaning scripts.

Built with **Python, Flask, Pandas, and JavaScript**, it provides an interactive workspace where users can upload datasets, explore data-quality insights, apply cleaning operations, review changes, undo operations, and download cleaned files with a PDF report.

---

## ✨ Features

### 📂 Multiple File Formats
Upload and work with different dataset formats:
- CSV (.csv)
- Excel (.xlsx, .xls)
- JSON (.json)
- Tab-separated values (.tsv)

### 📊 Dataset Analysis
Automatically analyze uploaded datasets and display useful information, including:
- Total rows, columns, and cells
- Missing values and their percentages
- Duplicate row statistics
- Numeric, text, and date column counts
- Dataset quality score
- Column-level insights and visualizations

### 🧹 30+ Data Cleaning Operations
Clean and transform datasets through an interactive interface.

Operations cover:
- Missing-value handling
- Duplicate detection and removal
- Text cleaning and formatting
- Date parsing and standardization
- Data validation
- Column and data transformations
- Numeric and formatting operations

### 📈 Interactive Visualizations
Understand your dataset through visual insights:
- Missing values by column
- Column type distribution
- Data completeness
- Missing-value distribution
- Duplicate versus unique records
- Dataset quality score

### ↩️ Undo and Reset
- Undo the latest cleaning operation.
- Reset the working dataset to its original uploaded state.
- Review dataset statistics before and after cleaning.

### 📄 PDF Reports
Generate downloadable PDF reports containing dataset information, cleaning activity, and processing results.

### 🔐 Security and Privacy
- UUID-based temporary processing sessions
- File extension and content validation
- Upload size validation
- Formula-injection protection for downloaded data
- Automatic cleanup of inactive sessions
- Rate limiting
- Security response headers
- Environment-based secret configuration

The application is designed to process datasets in temporary sessions rather than maintaining a permanent user dataset library.

---

## 🖥️ Application Workflow

The application follows a simple workflow:

1. **Upload:** Select or drag and drop a supported dataset.
2. **Analyze:** Automatically inspect the dataset and calculate data-quality statistics.
3. **Explore:** View charts and identify areas that need attention.
4. **Clean:** Select the required cleaning operations.
5. **Process:** Apply the selected operations and review the results.
6. **Undo or Reset:** Reverse the latest change or restore the original dataset.
7. **Download:** Download the cleaned dataset and generate a PDF report.

---

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Backend | Python, Flask |
| Data Processing | Pandas |
| Frontend | HTML5, CSS3, JavaScript |
| Charts | Chart.js |
| Report Generation | ReportLab |
| File Support | OpenPyXL, xlrd |
| Rate Limiting | Flask-Limiter |
| Session Management | Python, UUID, filesystem |
| Background Cleanup | APScheduler |
| Environment Configuration | python-dotenv |

---

## 📁 Project Structure

```text
csv-auto-cleaner/
│
├── app.py
├── config.py
├── requirements.txt
├── .env.example
├── .gitignore
│
├── core/
│   ├── analysis_engine.py
│   ├── content_validator.py
│   ├── file_io.py
│   ├── file_validator.py
│   ├── history_manager.py
│   ├── output_sanitizer.py
│   ├── quality_score.py
│   └── session_manager.py
│
├── operations/
│   ├── missing_values.py
│   ├── duplicates.py
│   ├── text_cleaning.py
│   ├── dates.py
│   ├── formatting.py
│   ├── validation.py
│   ├── transformation.py
│   └── registry.py
│
├── routes/
│   ├── upload.py
│   ├── analyze.py
│   ├── operations.py
│   ├── undo.py
│   ├── reset.py
│   ├── download.py
│   └── report.py
│
├── reporting/
│   └── pdf_generator.py
│
├── workers/
│   └── cleanup_scheduler.py
│
├── static/
│   ├── css/
│   │   └── styles.css
│   └── js/
│       ├── main.js
│       ├── upload.js
│       ├── insights.js
│       ├── workspace.js
│       ├── processing.js
│       └── results.js
│
├── templates/
│   └── index.html
│
└── tests/
    ├── test_app.py
    ├── test_content_validator.py
    └── test_output_sanitizer.py
```

---

## ⚙️ Installation and Setup

Follow these steps to run the project locally.

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/csv-auto-cleaner.git
```

```bash
cd csv-auto-cleaner
```

### 2. Create a virtual environment

**Windows:**

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root.

Use `.env.example` as a reference:

```env
SECRET_KEY=your-new-random-secret-key
COOKIE_SECURE=0
RATELIMIT_STORAGE_URI=memory://
```

Generate a secure secret key:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Keep the actual `.env` file private. Never commit it to GitHub.

For an HTTPS production deployment, configure the secure cookie setting appropriately.

### 5. Run the application

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000
```

---

## 🧪 Testing

The project includes automated tests for application endpoints, file-content validation, and output sanitization.

Install the testing dependency:

```bash
python -m pip install pytest
```

Run the tests:

```bash
python -m pytest -q
```

---

## 🔒 Security and Deployment Notes

CSV Auto Cleaner uses temporary session storage and local filesystem operations for uploaded and processed datasets.

The local application is designed around a persistent server process and session files. Serverless platforms such as Vercel have different filesystem and execution constraints.

**Important:** A production deployment on a serverless platform requires compatible external storage for session datasets, processed files, and history, along with a suitable scheduled-cleanup mechanism. The current filesystem-based workflow should not be considered fully production-ready on Vercel without that adaptation.

Do not upload `.env`, user datasets, session data, or generated runtime files to the repository.

---

## 🚀 Future Improvements

Potential enhancements include:
- External storage integration for reliable cloud sessions
- Improved support for large dataset uploads
- Advanced data profiling and validation
- Additional cleaning and transformation operations
- Automated data-quality recommendations
- Expanded automated test coverage
- Production deployment and monitoring improvements

---

## 🎯 Project Objective

The goal of CSV Auto Cleaner is to make everyday data preparation easier and more accessible.

Instead of spending time manually searching for missing values, removing duplicates, correcting formatting, and validating records, users can work through a single interface that brings together dataset analysis, cleaning operations, and reporting.

---

## 👩‍💻 Author

**Krisha Patel**

Built as a Python and Flask project focused on data processing, web application development, automation, and secure file handling.

---

## 📄 License

This project is currently available for review and learning. A license should be added to the repository before granting others permission to reuse, modify, or distribute the source code.
