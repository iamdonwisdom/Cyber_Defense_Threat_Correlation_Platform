import re


class DetectionEngine:
    """
    Detection Engine v1.0

    Detects suspicious activity from log entries.
    """

    def __init__(self):
        self.alerts = []

    def analyze_log(self, log_entry):
        """
        Analyze a single log entry.
        """

        entry = log_entry.upper()

        if "FAILED LOGIN" in entry:
            self.alerts.append({
                "severity": "High",
                "type": "Failed Login",
                "message": log_entry
            })

        if "BRUTE" in entry:
            self.alerts.append({
                "severity": "Critical",
                "type": "Brute Force",
                "message": log_entry
            })

        if "ERROR" in entry:
            self.alerts.append({
                "severity": "Medium",
                "type": "System Error",
                "message": log_entry
            })

    def analyze_logs(self, logs):
        """
        Analyze multiple log entries.
        """

        self.alerts = []

        for log in logs:
            self.analyze_log(log)

        return self.alerts
