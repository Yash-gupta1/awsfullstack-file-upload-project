import ssl
import socket
import datetime
import json

def parse_ssl_handshake_telemetry(hostname, port=443):
    context = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                # Gathering auditable compliance timelines
                expire_date = datetime.datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
                remaining_days = (expire_date - datetime.datetime.utcnow()).days
                
                evidence_payload = {
                    "control_id": "SOC_2_CC_6.7",
                    "telemetry_type": "Encryption-in-transit",
                    "target_host": hostname,
                    "ssl_status": "COMPLIANT" if remaining_days > 30 else "WARNING",
                    "days_to_expiration": remaining_days,
                    "timestamp": datetime.datetime.utcnow().isoformat()
                }
                return json.dumps(evidence_payload)
    except Exception as e:
        return json.dumps({"status": "FAILED", "error": str(e)})

# Mock execution to verify logic
print(parse_ssl_handshake_telemetry("github.com"))
