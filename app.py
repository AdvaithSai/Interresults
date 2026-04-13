"""
app.py  –  TGBIE Marks Fetcher Web Interface
Run:  python app.py
Open: http://localhost:5000
"""

import io, json, os, queue, re, sys, threading, time, traceback, uuid
from pathlib import Path

from flask import Flask, Response, jsonify, render_template, request, send_file, stream_with_context
import pandas as pd

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50 MB

ROLL_RE = re.compile(r"\b\d{10}\b")
BASE_DIR = Path(__file__).parent

# ── active tasks: task_id -> {queue, output_path, status, exam_year} ──────────
tasks: dict = {}


# ─────────────────────────────────────────────────────────────────────────────
#  ROLL-NUMBER EXTRACTION
# ─────────────────────────────────────────────────────────────────────────────

def _rolls_from_text(text: str) -> set:
    return set(ROLL_RE.findall(text))


def extract_from_file(stream, filename: str) -> tuple[list, str | None]:
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    rolls: set = set()
    warning = None

    try:
        raw = stream.read()

        if ext == "csv":
            text = raw.decode("utf-8", errors="replace")
            rolls = _rolls_from_text(text)

        elif ext in ("xlsx", "xls"):
            xl = pd.ExcelFile(io.BytesIO(raw))
            for sheet in xl.sheet_names:
                df = pd.read_excel(xl, sheet_name=sheet, dtype=str, header=None)
                rolls |= _rolls_from_text(df.to_csv(index=False, header=False))

        elif ext == "txt":
            rolls = _rolls_from_text(raw.decode("utf-8", errors="replace"))

        elif ext in ("jpg", "jpeg", "png"):
            try:
                from PIL import Image
                import pytesseract
                
                # Configure tesseract executable path for Windows
                tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
                if os.path.exists(tesseract_path):
                    pytesseract.pytesseract.tesseract_cmd = tesseract_path
                    
                img = Image.open(io.BytesIO(raw))
                rolls = _rolls_from_text(pytesseract.image_to_string(img))
            except ImportError:
                warning = "OCR unavailable — install pytesseract + pillow"
            except Exception as e:
                warning = f"OCR error: {e}"

        elif ext == "pdf":
            try:
                import pdfplumber
                with pdfplumber.open(io.BytesIO(raw)) as pdf:
                    for page in pdf.pages:
                        rolls |= _rolls_from_text(page.extract_text() or "")
            except ImportError:
                warning = "PDF support unavailable — install pdfplumber"
            except Exception as e:
                warning = f"PDF error: {e}"

        else:
            warning = f"Unsupported file type: .{ext}"

    except Exception as e:
        warning = f"Error reading file: {e}"

    return sorted(rolls), warning


# ─────────────────────────────────────────────────────────────────────────────
#  SCRAPER RUNNER  (background thread)
# ─────────────────────────────────────────────────────────────────────────────

def _emit(q: queue.Queue, msg_type: str, **kwargs):
    q.put(json.dumps({"type": msg_type, **kwargs}))


def run_scraper_task(task_id, roll_numbers, exam_year, results_year, category, exam_type, output_path):
    q = tasks[task_id]["queue"]

    try:
        sys.path.insert(0, str(BASE_DIR))
        import config as cfg
        import scraper

        # Patch config with user's choices
        cfg.EXAM_YEAR    = exam_year
        cfg.RESULTS_YEAR = results_year
        cfg.CATEGORY     = category
        cfg.EXAM_TYPE    = exam_type

        total = len(roll_numbers)
        _emit(q, "log", msg=f"🚀 Starting — {total} roll numbers | {exam_year} | {results_year}")
        _emit(q, "log", msg=f"   Category: {category}  |  Exam Type: {exam_type}")

        driver = scraper.setup_driver()
        _emit(q, "log", msg="🌐 Browser launched, connecting to TGBIE portal…")

        data, failed = [], []

        try:
            for i, ht in enumerate(roll_numbers, 1):
                _emit(q, "progress", current=i, total=total, msg=f"Fetching [{i}/{total}]: {ht}")
                result = scraper.fetch_one(driver, ht, exam_year=exam_year)
                if result:
                    result["_exam_year"] = exam_year
                    data.append(result)
                    _emit(q, "log",
                          msg=f"  ✅  {ht}  →  {result.get('Name','?'):<25}  Total: {result.get('Grand_Total','?')}")
                else:
                    failed.append(ht)
                    _emit(q, "log", msg=f"  ❌  {ht}  →  No result found")
                if i < total:
                    time.sleep(1)
        finally:
            driver.quit()
            _emit(q, "log", msg="🔒 Browser closed.")

        if data:
            scraper.save_excel(data, str(output_path))
            _emit(q, "log", msg=f"")
            _emit(q, "log", msg=f"📊 Excel saved — {len(data)}/{total} students.")
            if failed:
                sample = ", ".join(failed[:10]) + ("…" if len(failed) > 10 else "")
                _emit(q, "log", msg=f"⚠️  {len(failed)} failed: {sample}")
            tasks[task_id]["status"] = "done"
            _emit(q, "done", msg=f"Done! {len(data)} students fetched.", failed=failed, count=len(data))
        else:
            _emit(q, "error", msg="No data extracted. Check roll numbers and try again.")

    except Exception as e:
        _emit(q, "error", msg=f"Fatal error: {e}", trace=traceback.format_exc())


# ─────────────────────────────────────────────────────────────────────────────
#  ROUTES
# ─────────────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    import config as cfg
    defaults = {
        "results_year": cfg.RESULTS_YEAR,
        "exam_year":    cfg.EXAM_YEAR,
        "category":     cfg.CATEGORY,
        "exam_type":    cfg.EXAM_TYPE,
    }
    return render_template("index.html", defaults=defaults)


@app.route("/extract", methods=["POST"])
def extract():
    all_rolls: set = set()
    warnings = []

    for f in request.files.getlist("files"):
        if f and f.filename:
            rolls, warn = extract_from_file(f.stream, f.filename)
            all_rolls.update(rolls)
            if warn:
                warnings.append({"file": f.filename, "msg": warn})

    manual = request.form.get("manual", "").strip()
    if manual:
        all_rolls.update(_rolls_from_text(manual))

    return jsonify({"rolls": sorted(all_rolls), "count": len(all_rolls), "warnings": warnings})


@app.route("/run", methods=["POST"])
def run():
    data         = request.get_json()
    roll_numbers = data.get("rolls", [])
    exam_year    = data.get("exam_year", "Second Year")
    results_year = data.get("results_year", "2026")
    category     = data.get("category", "General")
    exam_type    = data.get("exam_type", "IPE")

    if not roll_numbers:
        return jsonify({"error": "No roll numbers provided"}), 400

    task_id     = str(uuid.uuid4())
    output_path = BASE_DIR / f"output_{task_id}.xlsx"

    tasks[task_id] = {
        "queue":       queue.Queue(),
        "output_path": str(output_path),
        "status":      "running",
        "exam_year":   exam_year,
    }

    threading.Thread(
        target=run_scraper_task,
        args=(task_id, roll_numbers, exam_year, results_year, category, exam_type, output_path),
        daemon=True,
    ).start()

    return jsonify({"task_id": task_id})


@app.route("/stream/<task_id>")
def stream(task_id):
    if task_id not in tasks:
        def _err():
            yield f"data: {json.dumps({'type':'error','msg':'Task not found'})}\n\n"
        return Response(stream_with_context(_err()), mimetype="text/event-stream")

    def generate():
        q = tasks[task_id]["queue"]
        while True:
            try:
                msg = q.get(timeout=65)
                yield f"data: {msg}\n\n"
                parsed = json.loads(msg)
                if parsed.get("type") in ("done", "error"):
                    break
            except queue.Empty:
                yield f"data: {json.dumps({'type':'ping'})}\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.route("/download/<task_id>")
def download(task_id):
    if task_id not in tasks:
        return "Task not found", 404
    path = tasks[task_id]["output_path"]
    if not Path(path).exists():
        return "File not ready", 404
    year_label = tasks[task_id].get("exam_year", "results").replace(" ", "_").lower()
    return send_file(
        path,
        as_attachment=True,
        download_name=f"marksheet_{year_label}.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


if __name__ == "__main__":
    app.run(debug=False, port=5000, threaded=True, use_reloader=False)
