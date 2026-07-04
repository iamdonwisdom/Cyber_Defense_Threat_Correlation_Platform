import csv
import os


class CSVReportGenerator:

    def generate(self, filename, logs, alerts, iocs, mitre_results):

        os.makedirs("reports", exist_ok=True)

        report_path = os.path.join("reports", filename)

        with open(report_path, "w", newline="", encoding="utf-8") as csvfile:

            writer = csv.writer(csvfile)

            writer.writerow(["Cyber Defense & Threat Correlation Platform"])
            writer.writerow(["SIEM Analysis Report"])
            writer.writerow([])

            writer.writerow(["Logs"])
            writer.writerow(["Timestamp", "Severity", "Source", "Event"])

            for log in logs:
                writer.writerow([
                    "",
                    "",
                    "Uploaded File",
                    str(log)
                ])

            writer.writerow([])

            writer.writerow(["Detection Alerts"])
            writer.writerow(["Severity", "Type", "Message"])

            for alert in alerts:
                writer.writerow([
                    alert.get("severity", ""),
                    alert.get("type", ""),
                    alert.get("message", "")
                ])

            writer.writerow([])

            writer.writerow(["Indicators of Compromise"])
            writer.writerow(["Type", "Value"])

            for ioc in iocs:
                writer.writerow([
                    ioc.get("type", ""),
                    ioc.get("value", "")
                ])

            writer.writerow([])

            writer.writerow(["MITRE ATT&CK Mapping"])
            writer.writerow(["Alert", "Technique ID", "Technique", "Tactic"])

            for item in mitre_results:
                writer.writerow([
                    item.get("alert", ""),
                    item.get("technique_id", ""),
                    item.get("technique", ""),
                    item.get("tactic", "")
                ])

        # Return only the filename
        return filename
