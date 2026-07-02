
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

from modules.database import (
    initialize_database,
    save_log,
    get_dashboard_stats,
    get_recent_logs
)
from modules.log_parser import parse_log

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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

        logs = parse_log(filepath)

        for log in logs:
            save_log(log)

        stats = get_dashboard_stats()

        return render_template(
            "upload.html",
            logs=logs,
            filename=filename,
            stats=stats
        )

    return render_template("upload.html")


if __name__ == "__main__":
    app.run(debug=True)
