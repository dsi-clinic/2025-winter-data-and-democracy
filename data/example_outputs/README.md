# Accuracy Test Files

This folder contains manually-checked election data files, Claude-generated election data files, and accuracy test to generate insights on errors and performance of Claude's OCR function.

## Files and Folders

1920pg9

- Contains manually checked and AI generated election data for page 9 of the 1920 election

1922full

- Contains manually ehcekced and AI generated election data for the entire 1922 election

1940full

- Contains manually ehcekced and AI generated election data for the entire 1940 election

1940pg1

- Contains manually checked and AI generated election data for page 1 of the 1940 election

1980pg3

- Contains manually checked and AI generated election data for page 3 of the 1980 election

accuracy_functions.py

- Contains all accuracy score functions to be imported by accuracy_test.ipynb

accuracy_test.ipynb

- Imports all functions from accuracy_functions.py and run tests on each election year

accuracytest.py

- Script to automatically run the accuracy tests in the pipeline
