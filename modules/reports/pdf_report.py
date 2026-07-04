from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import os


class PDFReportGenerator:

    def generate(self, filename, logs, alerts, iocs, mitre_results):

        os.makedirs("reports", exist_ok=True)

        report_path = os.path.join("reports", filename)

        styles = getSampleStyleSheet()

        doc = SimpleDocTemplate(report_path)

        story = []

        story.append(
            Paragraph(
                "<b>Cyber Defense & Threat Correlation Platform</b>",
                styles["Title"]
            )
        )

        story.append(
            Paragraph(
                "SIEM Analysis Report",
                styles["Heading2"]
            )
        )

        story.append(
            Paragraph(
                "<b>Logs</b>",
                styles["Heading2"]
            )
        )

        for log in logs:
            story.append(
                Paragraph(str(log), styles["BodyText"])
            )

        story.append(
            Paragraph(
                "<b>Detection Alerts</b>",
                styles["Heading2"]
            )
        )

        for alert in alerts:
            story.append(
                Paragraph(
                    f"{alert.get('severity')} - {alert.get('type')} - {alert.get('message')}",
                    styles["BodyText"]
                )
            )

        story.append(
            Paragraph(
                "<b>Indicators of Compromise</b>",
                styles["Heading2"]
            )
        )

        for ioc in iocs:
            story.append(
                Paragraph(
                    f"{ioc.get('type')}: {ioc.get('value')}",
                    styles["BodyText"]
                )
            )

        story.append(
            Paragraph(
                "<b>MITRE ATT&CK Mapping</b>",
                styles["Heading2"]
            )
        )

        for item in mitre_results:
            story.append(
                Paragraph(
                    f"{item.get('alert')} → {item.get('technique_id')} ({item.get('technique')})",
                    styles["BodyText"]
                )
            )

        doc.build(story)

        # Return only the filename
        return filename
