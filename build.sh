#!/usr/bin/env bash

set -euo pipefail

print_header () {
  printf '\e[1;35m%s\e[0m\n' "$@"
}

print_info () {
  printf '\e[34m%s\e[0m\n' "$@"
}

OUT_FILE="lambda-package.zip"

print_header "Starting creation of Lambda deployment package"

if [ -f "$OUT_FILE" ]; then
  print_info "Cleaning up old package"
  rm "$OUT_FILE"
fi

mkdir lambda-package-root && cd lambda-package-root

print_info "Copying files from root"
cp ../*.py .

print_info "Installing dependencies using pip"
pip install -r <(cd .. && poetry run pip freeze) -t .

print_info "Creating ZIP package"
zip -r ../"$OUT_FILE" ./*

print_info "Removing temporary build root"
cd ..
rm -r lambda-package-root

print_header "Done!"
