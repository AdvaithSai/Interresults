"""
inspector.py  –  Run this FIRST to automatically detect the website structure.

Usage:
    python inspector.py

It will open your browser, let you navigate to the result page manually,
then print out the correct IDs / XPaths you need to paste into config.py.
"""

import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

try:
    from config import WEBSITE_URL, PAGE_LOAD_WAIT
except ImportError:
    WEBSITE_URL = input("Enter the result website URL: ").strip()
    PAGE_LOAD_WAIT = 4


def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    # Use webdriver-manager so you never need to manually download chromedriver
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def find_inputs(driver):
    """Return all visible input fields and select dropdowns on the page."""
    elements = driver.find_elements(By.XPATH, "//input | //select | //button | //textarea")
    results = []
    for el in elements:
        try:
            tag  = el.tag_name
            el_id   = el.get_attribute("id") or ""
            name    = el.get_attribute("name") or ""
            el_type = el.get_attribute("type") or ""
            placeholder = el.get_attribute("placeholder") or ""
            visible = el.is_displayed()
            if visible:
                results.append({
                    "tag": tag, "id": el_id, "name": name,
                    "type": el_type, "placeholder": placeholder
                })
        except Exception:
            pass
    return results


def find_tables(driver):
    tables = driver.find_elements(By.TAG_NAME, "table")
    info = []
    for i, t in enumerate(tables):
        rows = t.find_elements(By.TAG_NAME, "tr")
        cols = 0
        if rows:
            cols = len(rows[0].find_elements(By.TAG_NAME, "td")) or \
                   len(rows[0].find_elements(By.TAG_NAME, "th"))
        info.append({"index": i, "rows": len(rows), "cols": cols})
    return info


def main():
    print("\n" + "═" * 60)
    print("  MARKS AUTOMATION — WEBSITE INSPECTOR")
    print("═" * 60)
    print(f"\n🌐  Opening: {WEBSITE_URL}")
    print("    Navigate to the RESULT FORM page if it didn't open directly.")
    print("    Press ENTER here once you can see the form with year + roll inputs.\n")

    driver = setup_driver()
    driver.get(WEBSITE_URL)

    input("⏳  Press ENTER when the form page is visible in Chrome ...")

    print("\n🔍  Scanning form elements ...")
    inputs = find_inputs(driver)

    print("\n── FORM ELEMENTS FOUND ──────────────────────────────")
    for el in inputs:
        print(f"  <{el['tag']}> id='{el['id']}'  name='{el['name']}'  "
              f"type='{el['type']}'  placeholder='{el['placeholder']}'")

    print("\n── SUGGESTED CONFIG VALUES ──────────────────────────")
    for el in inputs:
        hint = ""
        combined = (el["id"] + el["name"] + el["placeholder"]).lower()
        if any(k in combined for k in ["roll", "reg", "rno", "regno"]):
            hint = "  ← ROLL NUMBER INPUT"
            print(f"  ROLL_INPUT_ID   = \"{el['id'] or el['name']}\"{hint}")
        if any(k in combined for k in ["year", "class", "sem", "course"]):
            hint = "  ← YEAR / CLASS DROPDOWN"
            print(f"  YEAR_DROPDOWN_ID = \"{el['id'] or el['name']}\"{hint}")
        if el["tag"] == "button" or el["type"] in ("submit", "button"):
            hint = "  ← SUBMIT BUTTON"
            print(f"  SUBMIT_BUTTON_ID = \"{el['id'] or el['name']}\"{hint}")

    print("\n\n📋  Now enter a sample roll number and submit the form manually.")
    input("⏳  Press ENTER once the RESULT/MARKSHEET page is loaded ...")

    print("\n🔍  Scanning result page ...")
    tables = find_tables(driver)
    print("\n── TABLES ON RESULT PAGE ────────────────────────────")
    for t in tables:
        print(f"  Table #{t['index']}: {t['rows']} rows × {t['cols']} cols")

    if tables:
        best = max(tables, key=lambda x: x["rows"])
        ti = best["index"]
        print(f"\n  Best guess: Table #{ti} (most rows)")
        print(f"  SUBJECT_COL_XPATH = \"(//table)[{ti+1}]//tr/td[1]\"")
        print(f"  MARKS_COL_XPATH   = \"(//table)[{ti+1}]//tr/td[2]\"")

    # Try to find total
    try:
        page_text = driver.find_element(By.TAG_NAME, "body").text
        for line in page_text.splitlines():
            if "total" in line.lower():
                print(f"\n  Line containing 'total': \"{line.strip()}\"")
    except Exception:
        pass

    print("\n✅  Copy the values above into config.py and then run:")
    print("    python scraper.py\n")

    input("Press ENTER to close the browser ...")
    driver.quit()


if __name__ == "__main__":
    main()
