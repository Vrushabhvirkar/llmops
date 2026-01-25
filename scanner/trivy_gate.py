import json
import sys
from pathlib import Path

REPORT_FILE = Path("reports/trivy-report.json")

if not REPORT_FILE.exists():
    print("❌ Trivy report not found.")
    sys.exit(1)

with open(REPORT_FILE) as f:
    data = json.load(f)

vulns = []

for result in data.get("Results", []):
    for v in result.get("Vulnerabilities", []) or []:
        if v["Severity"] in ["HIGH", "CRITICAL"]:
            vulns.append(v)

if vulns:
    print("❌ TRIVY SECURITY GATE FAILED\n")
    for v in vulns[:10]:
        print(f"{v['Severity']} | {v['PkgName']} | {v['VulnerabilityID']}")
    print(f"\nTotal HIGH/CRITICAL vulns: {len(vulns)}")
    sys.exit(1)

print("✅ TRIVY SECURITY GATE PASSED")
sys.exit(0)

