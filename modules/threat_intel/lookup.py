import ipaddress


class ThreatIntelLookup:
    def __init__(self):
        self.known_benign_ips = {
            "8.8.8.8",
            "1.1.1.1",
            "9.9.9.9"
        }

    def lookup(self, iocs):
        results = []

        for ioc in iocs:
            reputation = "Unknown"
            confidence = 50

            try:
                ip = ipaddress.ip_address(ioc)

                if ip.is_private:
                    reputation = "Internal Network"
                    confidence = 100

                elif ioc in self.known_benign_ips:
                    reputation = "Known Benign"
                    confidence = 95

                else:
                    reputation = "Suspicious"
                    confidence = 80

            except ValueError:
                if "." in ioc:
                    reputation = "Domain"
                    confidence = 75

            results.append({
                "ioc": ioc,
                "reputation": reputation,
                "confidence": confidence
            })

        return results
