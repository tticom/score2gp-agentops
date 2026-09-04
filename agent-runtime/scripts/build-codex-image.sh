#!/usr/bin/env bash
set -euo pipefail

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)
runtime_dir=$(CDPATH= cd -- "$script_dir/.." && pwd -P)
image_tag=${SCORE2GP_CODEX_IMAGE:-score2gp-codex:local}

command -v docker >/dev/null 2>&1 || { echo "error: docker is required" >&2; exit 69; }
docker info >/dev/null
docker build --pull --tag "$image_tag" --file "$runtime_dir/codex.Dockerfile" "$runtime_dir"
docker run --rm --entrypoint codex "$image_tag" --version
echo "ready: $image_tag"
