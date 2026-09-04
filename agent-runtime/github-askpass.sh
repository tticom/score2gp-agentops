#!/bin/sh
set -eu

case "${1:-}" in
  *Username*) printf '%s\n' x-access-token ;;
  *) tr -d '\r\n' < /run/secrets/github-token ;;
esac
