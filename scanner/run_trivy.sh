#!/bin/bash
set -e

IMAGE_NAME="llm-api:latest"
REPORT_FILE="reports/trivy-report.json"

echo "🛡️ Running Trivy container scan..."

trivy image \
  --severity HIGH,CRITICAL \
  --format json \
  --output "$REPORT_FILE" \
  "$IMAGE_NAME"

echo "📦 Trivy report saved to $REPORT_FILE"

