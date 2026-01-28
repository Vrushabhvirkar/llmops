#!/bin/bash
set -e

STATUS="$1"        # success / failure
MESSAGE="$2"

if [ -z "$SLACK_WEBHOOK_URL" ]; then
  echo "⚠️ SLACK_WEBHOOK_URL not set, skipping Slack notification"
  exit 0
fi

COLOR="good"
EMOJI="✅"

if [ "$STATUS" = "failure" ]; then
  COLOR="danger"
  EMOJI="❌"
fi

PAYLOAD=$(jq -n \
  --arg text "$EMOJI *LLM Security Pipeline $STATUS*\n$MESSAGE\n🔗 $GITHUB_SERVER_URL/$GITHUB_REPOSITORY/actions/runs/$GITHUB_RUN_ID" \
  '{
    attachments: [
      {
        color: "'$COLOR'",
        text: $text
      }
    ]
  }'
)

curl -s -X POST \
  -H 'Content-Type: application/json' \
  --data "$PAYLOAD" \
  "$SLACK_WEBHOOK_URL"
