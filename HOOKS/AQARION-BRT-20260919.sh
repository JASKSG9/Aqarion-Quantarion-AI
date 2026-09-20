#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

repo_dir="$(git rev-parse --show-toplevel)"
cd "$repo_dir"

echo "AQARION pre-push: running verification"
./verify.sh

echo "AQARION pre-push: verification passed"
