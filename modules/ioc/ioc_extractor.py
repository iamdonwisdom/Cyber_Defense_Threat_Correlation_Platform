import re

class IOCExtractor:

    def extract(self, logs):
        iocs = []

        ip_pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
        domain_pattern = r"\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b"
        hash_pattern = r"\b[a-fA-F0-9]{32,64}\b"

        for log in logs:

            for ip in re.findall(ip_pattern, log):
                iocs.append({
                    "type": "IP Address",
                    "value": ip
                })

            for domain in re.findall(domain_pattern, log):
                iocs.append({
                    "type": "Domain",
                    "value": domain
                })

            for h in re.findall(hash_pattern, log):
                iocs.append({
                    "type": "Hash",
                    "value": h
                })


