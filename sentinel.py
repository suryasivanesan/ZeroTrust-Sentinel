import nmap
import requests
import json
import datetime
import os
from cryptography.fernet import Fernet

# =====================================================================
# 1. CRYPTOGRAPHIC DATA PROTECTION LAYER (ZERO-TRUST COMPLIANCE)
# =====================================================================
# Automatically handles generation or secure loading of local symmetric keys
KEY_FILE = "secret.key"

if not os.path.exists(KEY_FILE):
    # Generate a cryptographically secure 128-bit key for local AES authentication
    system_key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_out:
        key_out.write(system_key)
else:
    with open(KEY_FILE, "rb") as key_in:
        system_key = key_in.read()

cipher_engine = Fernet(system_key)

# =====================================================================
# 2. RUNTIME CONFIGURATION SETTINGS
# =====================================================================
# PASTE YOUR COPIED DISCORD WEBHOOK CHANNEL STRING URL HERE:
DISCORD_WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL_HERE"

# Local host target configuration (Use 127.0.0.1 or your local router gateway for testing)
TARGET_IP = "127.0.0.1" 

# Reference dictionaries mapping legacy or high-risk administrative entry vectors
RISKY_PORTS_BASELINE = {
    21: "FTP (Plaintext credential leakage risk)",
    22: "SSH (Brute-force baseline entry exposure risk)",
    23: "Telnet (Highly Vulnerable - Missing baseline payload encryption)",
    80: "HTTP (Unencrypted plaintext traffic transmission profile)",
    445: "SMB (Risk of EternalBlue exploitation / unauthorized lateral movement)"
}

# =====================================================================
# 3. CORE INFRASTRUCTURE PIPELINE ENGINES
# =====================================================================
def execute_network_scan(target_host):
    """Initializes the underlying Nmap engine to discover open network ports."""
    print(f"[*] [ZeroTrust-Sentinel] Initializing automated scanning framework on: {target_host}")
    scanner = nmap.PortScanner()
    
    try:
        # Performs an optimized service-version detection TCP scan across common structural ports
        scanner.scan(target_host, '1-1024', arguments='-sV')
        return scanner[target_host]
    except Exception as error_msg:
        print(f"[-] Scan Engine Execution Failure: {error_msg}")
        return None

def process_and_secure_findings(raw_scan_data):
    """Analyzes open discovery data, writes encrypted log files, and routes active triage alerts."""
    if not raw_scan_data or 'tcp' not in raw_scan_data:
        print("[-] Scanning phase finished: No active TCP protocol endpoints detected.")
        return

    identified_threats = []
    log_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Iterate over discovered TCP network sockets
    for port_num, configuration in raw_scan_data['tcp'].items():
        if configuration['state'] == 'open':
            service_name = configuration['name']
            detected_version = f"{configuration['product']} {configuration['version']}".strip()
            
            if not detected_version:
                detected_version = "Unknown version specification"

            # Profile exposures against the internal risk matrix
            if port_num in RISKY_PORTS_BASELINE:
                threat_severity = "🔴 HIGH RISK"
                mitigation_remedy = RISKY_PORTS_BASELINE[port_num]
            else:
                threat_severity = "🟡 MEDIUM RISK"
                mitigation_remedy = "Standard operating network point. Restrict access via local firewall profiles."

            threat_incident = {
                "port": port_num,
                "service": service_name,
                "version": detected_version,
                "severity": threat_severity,
                "mitigation": mitigation_remedy
            }
            identified_threats.append(threat_incident)

    # 1. GENERATE SECURE CRYPTOGRAPHICALLY OBFUSCATED SYSTEM AUDIT TRAIL
    audit_payload = {
        "scan_time": log_timestamp,
        "target_node": TARGET_IP,
        "vulnerabilities_logged": identified_threats
    }
    
    serialized_json = json.dumps(audit_payload, indent=4)
    # Encrypt raw text telemetry metrics to enforce data integrity locally
    encrypted_payload = cipher_engine.encrypt(serialized_json.encode())

    with open("security_audit_logs.enc", "ab") as safe_log_output:
        safe_log_output.write(encrypted_payload + b"\n")
    print("[+] Zero-Trust Defense: Local audit trial written successfully (Symmetrically Encrypted via AES).")

    # 2. DISPATCH REAL-TIME ALERTS TO SOC CHANNEL IF EXPOSURES EXIST
    if identified_threats:
        dispatch_webhook_alert(identified_threats)
    else:
        print("[+] Scanning completed successfully: Perimeter meets clean structural security standards.")

def dispatch_webhook_alert(vulnerabilities):
    """Transmits real-time markdown-enriched operational telemetry directly to the SOC monitoring endpoint."""
    if DISCORD_WEBHOOK_URL == "YOUR_DISCORD_WEBHOOK_URL_HERE":
        print("[-] Alert Pipeline Idle: Webhook endpoint parameter remains unconfigured.")
        return

    ui_embed_fields = []
    for issue in vulnerabilities:
        ui_embed_fields.append({
            "name": f"Port {issue['port']} ({issue['service']}) — {issue['severity']}",
            "value": f"**Detected Footprint:** `{issue['version']}`\n**Remediation Mapping:** {issue['mitigation']}",
            "inline": False
        })

    # Construct rich messaging format for professional interface mapping
    rich_alert_payload = {
        "username": "ZeroTrust-Sentinel Incident Engine",
        "embeds": [{
            "title": "🚨 DISCOVERED PERIMETER VULNERABILITY EXPOSURE 🚨",
            "description": f"Real-time network analysis engine flagged active exposures on host: **{TARGET_IP}**",
            "color": 15158332,  # Enterprise Hex Code Red
            "fields": ui_embed_fields,
            "footer": {"text": "ZeroTrust-Sentinel • Real-Time Automated Infrastructure Defense System"}
        }]
    }

    try:
        http_response = requests.post(DISCORD_WEBHOOK_URL, json=rich_alert_payload)
        if http_response.status_code == 204:
            print("[+] Real-time operational notification dispatched to telemetry center.")
        else:
            print(f"[-] Webhook communication error encountered: Code {http_response.status_code}")
    except Exception as connection_error:
        print(f"[-] Alert pipeline networking exception: {connection_error}")

# =====================================================================
# 4. RUNTIME SYSTEM EXECUTION TRIGGER
# =====================================================================
if __name__ == "__main__":
    scan_output = execute_network_scan(TARGET_IP)
    if scan_output:
        process_and_secure_findings(scan_output)