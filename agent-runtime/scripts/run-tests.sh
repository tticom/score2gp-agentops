#!/bin/sh
set -eu

runtime_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd -P)
repo_root=$(CDPATH= cd -- "$runtime_dir/.." && pwd -P)
python_bin=$($runtime_dir/scripts/configure-test-env.sh)
if [ "$#" -eq 0 ]; then
  set -- tests
fi
exec "$python_bin" -m pytest "$@"
