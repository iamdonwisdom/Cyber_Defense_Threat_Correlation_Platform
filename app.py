from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
import os

from modules.database import (
    initialize_database,
    save_log,
    get_dashboard_stats,
    get_recent_logs
)

from modules.log_parser import parse_log
from modules.detection.detection_engine import DetectionEngine
from modules.ioc.ioc_extractor import IOCExtractor
from modules.threat_intel.lookup import ThreatIntelLookup
from modules.mitre.mapper import MITREMapper
from modules.reports.csv_report import CSVReportGenerator
from modules.reports.pdf_report import PDFReportGenerator

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs("reports", exist_ok=True)

initialize_database()


@app.route("/")
def dashboard():
    stats = get_dashboard_stats()
    logs = get_recent_logs()

    return render_template(
        "dashboard.html",
        stats=stats,
        logs=logs
    )


@app.route("/upload", methods=["GET", "POST"])
def upload_page():

    if request.method == "POST":

        if "logfile" not in request.files:
            return "No file selected."

        file = request.files["logfile"]

        if file.filename == "":
            return "Please choose a file."

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        file.save(filepath)

        # Parse uploaded log file
        logs = parse_log(filepath)

        # Save logs into database
        for log in logs:
            save_log(log)

        # Detection Engine
        detector = DetectionEngine()
        alerts = detector.analyze_logs(logs)

        # IOC Extraction
        extractor = IOCExtractor()
        iocs = extractor.extract(logs)

        # Threat Intelligence
        intel = ThreatIntelLookup()
        threat_results = intel.lookup(iocs)

        # MITRE Mapping
        mitre = MITREMapper()
        mitre_results = mitre.map_alerts(alerts)

        # Generate CSV Report
        csv_generator = CSVReportGenerator()
        csv_report = csv_generator.generate(
            "analysis_report.csv",
            logs,
            alerts,
            iocs,
            mitre_results
        )

        # Generate PDF Report
        pdf_generator = PDFReportGenerator()
        pdf_report = pdf_generator.generate(
            "analysis_report.pdf",
            logs,
            alerts,
            iocs,
            mitre_results
        )

        stats = get_dashboard_stats()

        return render_template(
            "upload.html",
            logs=logs,
            filename=filename,
            stats=stats,
            alerts=alerts,
            iocs=iocs,
            threat_results=threat_results,
            mitre_results=mitre_results,
            csv_report=csv_report,
            pdf_report=pdf_report
        )

    return render_template(
        "upload.html",
        logs=[],
        filename=None,
        stats=get_dashboard_stats(),
        alerts=[],
        iocs=[],
        threat_results=[],
        mitre_results=[],
        csv_report=None,
        pdf_report=None
    )


@app.route("/reports/<path:filename>")
def download_report(filename):
    return send_from_directory("reports", filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
