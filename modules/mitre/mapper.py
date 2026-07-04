class MITREMapper:

    def map_alerts(self, alerts):

        mappings = []

        technique_map = {
            "Failed Login": (
                "T1110",
                "Brute Force",
                "Credential Access"
            ),
            "Brute Force": (
                "T1110",
                "Brute Force",
                "Credential Access"
            ),
            "System Error": (
                "T1499",
                "Endpoint Denial of Service",
                "Impact"
            ),
            "PowerShell": (
                "T1059.001",
                "PowerShell",
                "Execution"
            ),
            "Credential Dumping": (
                "T1003",
                "OS Credential Dumping",
                "Credential Access"
            )
        }

        for alert in alerts:

            alert_type = alert.get("type")

            if alert_type in technique_map:

                technique = technique_map[alert_type]

                mappings.append({
                    "alert": alert_type,
                    "technique_id": technique[0],
                    "technique": technique[1],
                    "tactic": technique[2]
                })

        return mappings
