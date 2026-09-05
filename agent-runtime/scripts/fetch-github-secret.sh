#!/usr/bin/env bash
set -euo pipefail

output_file=${1:?usage: fetch-github-secret.sh OUTPUT_FILE PROJECT SECRET}
project=${2:?usage: fetch-github-secret.sh OUTPUT_FILE PROJECT SECRET}
secret=${3:?usage: fetch-github-secret.sh OUTPUT_FILE PROJECT SECRET}

command -v gcloud >/dev/null 2>&1 || {
  echo "error: gcloud is required" >&2
  exit 69
}

read_secret() {
  gcloud secrets versions access latest --secret="$secret" --project="$project" \
    | tr -d '\r\n' > "$output_file"
}

if ! read_secret; then
  rm -f "$output_file"
  if [ -t 0 ] && [ -t 1 ] && [ "${SCORE2GP_GCLOUD_AUTO_LOGIN:-1}" = 1 ]; then
    echo "No usable gcloud credentials; starting browser login..." >&2
    "$(dirname "$0")/gcloud-login.sh"
    read_secret
  else
    echo "error: gcloud authentication is required on this WSL host; run:" >&2
    echo "  $(dirname "$0")/gcloud-login.sh" >&2
    exit 77
  fi
fi

chmod 600 "$output_file"
test -s "$output_file" || {
  echo "error: GitHub secret is empty" >&2
  exit 74
}
