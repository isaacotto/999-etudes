#!/bin/bash

# Clean project directory of generated files

# Prompt user for confirmation
read -p "Are you sure you want to clean the project directory? This will remove all generated files. (y/n): " confirm

# Remove generated .pdf, .midi, and .txt files as well as score.ly
rm -f *.pdf
rm -f *.midi
rm -f *.txt
rm -f score.ly

# Remove all generated directories beginning with "output-scores"
rm -rf output-scores*

