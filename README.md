# MARKS AUTOMATION PROJECT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📁 Project Structure

```
marks_automation/
│
├── config.py       ← ✏️  EDIT THIS FIRST  (URL, roll numbers, selectors)
├── inspector.py    ← 🔍  Run to auto-detect website structure
├── scraper.py      ← 🚀  Main automation script
└── README.md       ← 📖  This file
```

---

## ✅ QUICK START (3 Steps)

### Step 1 — Edit `config.py`

Open `config.py` and fill in:
- `WEBSITE_URL` — paste the result website URL
- `EXAM_YEAR`   — e.g. `"Second Year"`
- `ROLL_NUMBERS` — your list of roll numbers

### Step 2 — Run the Inspector (optional but recommended)

```
python inspector.py
```

This opens Chrome, lets you navigate to the form page, then **automatically
detects** the correct element IDs and XPaths. Copy those into `config.py`.

### Step 3 — Run the Scraper

```
python scraper.py
```

When done, `marksheet_output.xlsx` will be created in this folder.

---

## 📊 Output

The Excel file will have nicely formatted columns:

| Roll No | Maths | Physics | Chemistry | English | Total |
|---------|-------|---------|-----------|---------|-------|
| 2658266175 | 85 | 78 | 82 | 90 | 335 |

---

## ⚠️ Common Problems & Fixes

| Problem | Fix |
|---------|-----|
| Chrome doesn't open | Run `inspector.py` — it auto-downloads the right ChromeDriver |
| "Element not found" | Run `inspector.py` to get correct IDs/XPaths, update `config.py` |
| Page loads slowly | Increase `PAGE_LOAD_WAIT` in `config.py` (e.g., `10`) |
| Year not being selected | Check `YEAR_DROPDOWN_ID` and `EXAM_YEAR` text in `config.py` |
| Some roll numbers fail | They'll be saved to `failed_rolls.txt` — add them back to `ROLL_NUMBERS` and re-run |

---

## 🔧 All Config Options (config.py)

```python
WEBSITE_URL       = "https://..."   # Result website URL
EXAM_YEAR         = "Second Year"   # Text of year option
ROLL_NUMBERS      = [...]           # List of roll number strings
OUTPUT_FILE       = "marksheet_output.xlsx"
PAGE_LOAD_WAIT    = 5               # Seconds to wait for result page

# Advanced (from inspector.py output)
YEAR_DROPDOWN_ID  = "year"
ROLL_INPUT_ID     = "rollno"
SUBMIT_BUTTON_ID  = "submit"
SUBJECT_COL_XPATH = "//table//tr/td[1]"
MARKS_COL_XPATH   = "//table//tr/td[2]"
TOTAL_XPATH       = ""              # Leave blank for auto-detection
```

---

## 🧠 How It Works

```
For each roll number
  ├── Open website
  ├── Select exam year
  ├── Enter roll number
  ├── Click Submit
  ├── Wait for page to load
  ├── Extract subject names + marks from table
  ├── Extract total marks
  └── Store in memory

After all rolls done:
  └── Save everything to marksheet_output.xlsx  (with styled header)
```

---

*Built with Python · Selenium · pandas · openpyxl · webdriver-manager*
