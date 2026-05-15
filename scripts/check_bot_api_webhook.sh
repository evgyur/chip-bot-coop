#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: $0 '<TELEGRAM_BOT_TOKEN>'" >&2
  echo "Do not paste real tokens into chat logs or public issues." >&2
  exit 2
fi

token="$1"
if [[ "$token" == *"<"* || "$token" == *">"* || -z "$token" ]]; then
  echo "Provide a real token only in your private terminal, never in a public repo." >&2
  exit 2
fi

curl -fsS "https://api.telegram.org/bot${token}/getWebhookInfo"
echo
