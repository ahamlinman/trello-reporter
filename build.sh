#!/usr/bin/env bash

set -e

print_header () {
  printf "\e[1;35m%s\e[0m\n" "$@"
}

print_info () {
  printf "\e[34m%s\e[0m\n" "$@"
}

print_header "Starting creation of Lambda deployment package"

mkdir lambda-package-root && cd lambda-package-root

print_info "Copying files from root"
cp ../*.py .

print_info "Installing dependencies using pip"
pip install -r ../requirements.txt -t .

print_info "Creating ZIP package"
zip -r ../lambda-package.zip ./*

print_info "Removing temporary build root"
cd ..
rm -r lambda-package-root

print_header "Done!"
