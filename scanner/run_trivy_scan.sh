#!/bin/bash
set +e   # ✅ CHANGED: allow script to continue on Trivy failure

IMAGE_NAME="llm-api"
REPORT_DIR="reports"
REPORT_FILE="$REPORT_DIR/trivy-report.json"

echo "🔍 Running Trivy container scan on $IMAGE_NAME..."

mkdir -p "$REPORT_DIR"

trivy image \
  --severity HIGH,CRITICAL \
  --format json \
  --output "$REPORT_FILE" \
  "$IMAGE_NAME"

SCAN_EXIT_CODE=$?

if [ $SCAN_EXIT_CODE -ne 0 ]; then
  echo "❌ Trivy found HIGH or CRITICAL vulnerabilities!"
  echo "📄 Report saved to $REPORT_FILE"
  exit 1
fi

echo "✅ Trivy scan passed (no HIGH/CRITICAL vulns)"
echo "📄 Report saved to $REPORT_FILE"

