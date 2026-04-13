# ─────────────────────────────────────────────────────────────────────────────
# config.py  –  Telangana Board of Intermediate Education (TGBIE) Mark Fetcher
# Website: https://tgbienew.cgg.gov.in/ResultMemorandum.do
# ─────────────────────────────────────────────────────────────────────────────

# ── Website ───────────────────────────────────────────────────────────────────
WEBSITE_URL = "https://tgbienew.cgg.gov.in/ResultMemorandum.do"

# ── Exam Settings ─────────────────────────────────────────────────────────────
# Results Year — must match an option in the dropdown
# Available options on the site: 2025, 2024, 2023, 2022, 2021, 2020
RESULTS_YEAR = "2026"

# Year of study — "First Year" or "Second Year"
#   First Year  → radio id="year1", value="1"
#   Second Year → radio id="year2", value="2"
EXAM_YEAR = "Second Year"   # change to "First Year" if needed

# Category — "General", "Vocational", "General Bridge Course", "Vocational Bridge Course"
CATEGORY = "General"

# Examination Type — "IPE" or "IPASE"
EXAM_TYPE = "IPE"

# ── Roll Numbers — 2nd Year ───────────────────────────────────────────────────
# These will be fetched with "Second Year" radio selected
ROLL_NUMBERS = [
    "2658266175",
    "2658266182",
    "2658266192",
    # ── add more 2nd year hall ticket numbers below ──
]

# ── Roll Numbers — 1st Year ───────────────────────────────────────────────────
# These will be fetched with "First Year" radio selected
FIRST_YEAR_ROLL_NUMBERS = [
    "2658161888",
    "2658161929",
    "2658162206",
    "2658162467",
    "2658162501",
    "2658162773",
    "2658162906",
    "2658162953",
    "2658163226",
    "2658163268",
    "2658163545",
    "2658163561",
    "2658163570",
    "2658163588",
    "2658163707",
    "2658163717",
    "2658163734",
    "2658163786",
    "2658163805",
    "2658163813",
    "2658163903",
    "2658163920",
    "2658163933",
    "2658163950",
    "2658163963",
    "2658163978",
    "2658163991",
    "2658164216",
    "2658164233",
    "2658164249",
    "2658164261",
    "2658164275",
    "2658164293",
    "2658164303",
    "2658164323",
    "2658164334",
    "2658164350",
    "2658164359",
    "2658164685",
    "2658164702",
    "2658164743",
    "2658164754",
    "2658164782",
    "2658164900",
    "2658164915",
    "2658164924",
    "2658164939",
    "2658164955",
    "2658164968",
    "2658164977",
    "2658164991",
    "2658165005",
    "2658165015",
    "2658165605",
    "2658165919",
    "2658165980",
    "2658166133",
    "2658166162",
    "2658166195",
    "2658166226",
    "2658167053",
    "2658167258",
    "2658167305",
    "2658167350",
    "2658167684",
    "2658167727",
    "2658168009",
    "2658168100",
    "2658168144",
    "2658168799",
    "2658168835",
    "2658168875",
    "2658169027",
    "2658169494",
    "2658169533",
    "2658169574",
    "2658169673",
    "2658170023",
    "2658170060",
    "2658170259",
    "2658170298",
    "2658170553",
    "2658170781",
    "2658170792",
    "2658170811",
    "2658170822",
    "2658170839",
    "2658170852",
    "2658170870",
    "2658170878",
    "2658171198",
    "2658171472",
    "2658161966",
    "2658162010",
    "2658162354",
    "2658162995",
    "2658163031",
    "2658163321",
    "2658163630",
    "2658163646",
    "2658163660",
    "2658163677",
    "2658163688",
    "2658164376",
    "2658164389",
    "2658164423",
    "2658164431",
    "2658164480",
    "2658164490",
    "2658164604",
    "2658164718",
    "2658164728",
    "2658165034",
    "2658165047",
    "2658165060",
    "2658165072",
    "2658165084",
    "2658165099",
    "2658165364",
    "2658165377",
    "2658165416",
    "2658165430",
    "2658165875",
    "2658166255",
    "2658166286",
    "2658167112",
    "2658167157",
    "2658167635",
    "2658168198",
    "2658168289",
    "2658168721",
    "2658168760",
    "2658169108",
    "2658169154",
    "2658169615",
    "2658169981",
    "2658170347",
    "2658170590",
    "2658170607",
    "2658170621",
    "2658170739",
    "2658170750",
    "2658171418",
    "2658162232"
]

# ── Output ────────────────────────────────────────────────────────────────────
OUTPUT_FILE            = "marksheet_2nd_year.xlsx"   # 2nd year results
FIRST_YEAR_OUTPUT_FILE = "marksheet_1st_year.xlsx"   # 1st year results

# Seconds to wait after clicking "Get Memo" for the result to appear
PAGE_LOAD_WAIT = 5

# ─────────────────────────────────────────────────────────────────────────────
# EXACT SELECTORS (discovered by live inspection — do NOT change unless the
# website structure changes)
# ─────────────────────────────────────────────────────────────────────────────

# Form element IDs
RESULTS_YEAR_ID   = "pass_year"       # <select id="pass_year"> — Results Year dropdown
YEAR_RADIO_YEAR1  = "year1"           # <input type="radio" id="year1"> First Year
YEAR_RADIO_YEAR2  = "year2"           # <input type="radio" id="year2"> Second Year
CATEGORY_GENERAL  = "categoryG"       # <input type="radio" id="categoryG"> General
CATEGORY_VOCA     = "categoryV"       # <input type="radio" id="categoryV"> Vocational
EXAM_TYPE_IPE_ID  = "month"           # <input type="radio" id="month" value="1"> IPE
HALL_TICKET_ID    = "hallticket_no"   # <input type="text" id="hallticket_no">
SUBMIT_XPATH      = "//input[@type='button' and @value='Get Memo']"  # type=button (not submit!)

# Exam type radio: name="property(month)"  IPE=value "3"  /  IPASE=value "6"
# (Both share id="month" — selected by name+value XPath in scraper.py)

# Result page — marks table structure (YEAR × SUBJECT grid)
# The table has headers: YEAR | SUBJECT | ENGLISH(THEORY/PRAC) | SANSKRIT | MATHS A | MATHS B | PHYSICS | CHEMISTRY
# Grand Total is displayed as plain text near a label "GRAND TOTAL:"
GRAND_TOTAL_XPATH = "//*[contains(text(),'GRAND TOTAL:')]/following-sibling::*[1] | " \
                    "//*[contains(text(),'GRAND TOTAL:')]"
RESULT_GRADE_XPATH = "//*[contains(text(),'RESULT:')]/following-sibling::*[1] | " \
                     "//*[contains(text(),'RESULT')]"
