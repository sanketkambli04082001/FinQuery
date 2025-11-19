import os
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

from finquery.analyzer import ReportAnalyzer
from finquery.fetcher import DataFetcher
from finquery.visualizer import DataVisualizer
from finquery.database import DataBaseManager

UPLOAD_FOLDER = 'uploads'
STATIC_CHART_FOLDER = os.path.join("static", "charts")
ALLOWED_EXTENSIONS = {"pdf"}

# How many characters we pass to the AI (same as your main.py)
AI_CHAR_LIMIT = 20000

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_CHART_FOLDER, exist_ok=True)

analyzer = ReportAnalyzer()
fetcher = DataFetcher()
visualizer = DataVisualizer()
db = DataBaseManager()

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    if "pdf_file" not in request.files:
        return redirect(url_for("index"))

    file = request.files["pdf_file"]
    if file.filename == "" or not allowed_file(file.filename):
        return redirect(url_for("index"))

    filename = secure_filename(file.filename)
    save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(save_path)

    # 1) Extract text (full text kept in variable, but we will store a bounded version)
    pdf_text = analyzer.extract_text_from_pdf(save_path) or ""

    # Keep a bounded stored version (so DB doesn't grow huge). Store first + last portions.
    MAX_STORE = 350000
    if len(pdf_text) > MAX_STORE:
        prefix = pdf_text[:175000]
        suffix = pdf_text[-175000:]
        pdf_text_to_store = prefix + "\n\n....(truncated middle)....\n\n" + suffix
    else:
        pdf_text_to_store = pdf_text

    ai_text = pdf_text[:AI_CHAR_LIMIT] + "\n\n" + pdf_text[-3000:]


    try:
        summary = analyzer.summarize_text(ai_text)
    except Exception as e:
        print("Summary AI failed:", e)
        summary = "Summary unavailable (AI error)."


    try:
        company_info = analyzer.get_competitors(ai_text)
        main_ticker = company_info.get("main_ticker", "UNKNOWN")
        competitors = company_info.get("competitors", []) or []
    except Exception as e:
        print("Competitor detection AI failed:", e)
        main_ticker = "UNKNOWN"
        competitors = []

    # 4) Fetch competitor data (simple loop / fetcher helper)
    competitor_rows = []
    if competitors:
        try:
            # use existing fetcher method (should handle per-ticker errors)
            competitor_rows = fetcher.get_competitor_stats(competitors)
        except Exception as e:
            print("get_competitor_stats failed:", e)
            # fallback: try single-company overviews
            competitor_rows = []
            for t in competitors:
                try:
                    info = fetcher.get_company_overview(t)
                    competitor_rows.append({"ticker": t, "info": info})
                except Exception:
                    competitor_rows.append({"ticker": t, "info": None})

    # 5) Extract financial table and create chart (pass limited text to AI)
    chart_filename = ""
    try:
        chart_data = analyzer.extract_financial_table(ai_text) or {}
    except Exception as e:
        print("Table extraction AI failed:", e)
        chart_data = {}

    if chart_data:
        keys = list(chart_data.keys())
        if keys and str(keys[0]).upper().startswith("Q"):
            chart_title = "Quarterly Revenue (Cr)"
        else:
            chart_title = "Annual Revenue (Cr)"

        chart_filename = f"{main_ticker}_revenue_chart.png"
        chart_path = os.path.join(STATIC_CHART_FOLDER, chart_filename)
        try:
            visualizer.create_bar_chart(chart_data, chart_title, chart_path)
        except Exception as e:
            print("Chart creation failed:", e)
            chart_filename = ""

    # 6) Build report dict and save to DB
    report = {
        "ticker": main_ticker,
        "summary": summary,
        "competitors": competitors,
        "competitor_rows": competitor_rows,
        # chart path referenced relative to /static/
        "chart_filename": f"charts/{chart_filename}" if chart_filename else "",
        "pdf_text": pdf_text_to_store
    }

    report_id = db.save_report(report)
    return redirect(url_for("view_report", report_id=report_id))


@app.route("/report/<int:report_id>", methods=["GET", "POST"])
def view_report(report_id):
    rec = db.get_report(report_id)
    if not rec:
        return "Report not found", 404

    qa_answer = ""
    if request.method == "POST":
        question = (request.form.get("question") or "").strip()
        if question:
            full_text = rec.get("pdf_text", "") or ""
            chunk_size = 20000 

            if len(full_text) <= chunk_size * 3:
                tri_text = full_text
            else:
               
                start = full_text[:chunk_size]              
                middle_index = len(full_text) // 2
                middle = full_text[middle_index: middle_index + chunk_size]  
                end = full_text[-chunk_size:]                 

                tri_text = start + "\n\n" + middle + "\n\n" + end

            try:
                qa_answer = analyzer.answer_question(tri_text, question)
            except Exception as e:
                print("QA AI failed:", e)
                qa_answer = "AI answer currently unavailable."


    return render_template("report.html", report=rec, qa_answer=qa_answer)


@app.route("/static/<path:filename>")
def static_files(filename):
    """Serve files in static/ (CSS, charts, etc)."""
    return send_from_directory("static", filename)


if __name__ == "__main__":
    # disable reloader to avoid duplicate model calls in dev
    app.run(debug=True, use_reloader=False, port=5000)
