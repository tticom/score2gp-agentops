#!/bin/sh
set -eu

case "${1:-}" in
  *Username*) printf '%s\n' x-access-token ;;
  *)
    if [ -n "${GH_TOKEN:-}" ]; then printf '%s\n' "$GH_TOKEN";
    else tr -d '\r\n' < /run/secrets/github-token; fi ;;
esac
