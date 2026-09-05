#!/usr/bin/env bash
set -euo pipefail

command -v gcloud >/dev/null 2>&1 || {
  echo "error: gcloud is required" >&2
  exit 69
}

# Run this only on the persistent WSL host. Disposable workers must never
# receive the Google refresh credentials used to read Secret Manager.
gcloud auth login "$@"

config_dir=$(gcloud info --format='value(config.paths.global_config_dir)')
if [ -n "$config_dir" ] && [ -d "$config_dir" ]; then
  find "$config_dir" -type d -exec chmod go-rwx {} +
  find "$config_dir" -type f -exec chmod go-rwx {} +
fi

echo "gcloud credentials stored locally in $config_dir with user-only permissions."
