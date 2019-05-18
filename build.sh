#!/usr/bin/env bash
# shellcheck disable=SC1091

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

print_info "Creating production virtualenv"
python3 -m venv lambda-package-venv

print_info "Installing into production virtualenv"
(. lambda-package-venv/bin/activate; poetry install --no-dev)

print_info "Copying core files into build root"
mkdir lambda-package-root
cp ./*.py lambda-package-root/

print_info "Installing dependencies into build root"
pip install -r <(. lambda-package-venv/bin/activate; pip freeze) -t lambda-package-root/

print_info "Creating ZIP package"
(cd lambda-package-root && zip -r ../"$OUT_FILE" ./*)

print_info "Removing temporary build files"
rm -rf lambda-package-root lambda-package-venv

print_header "Done!"
