# Centrala University — Pharmaceutical Data Management Tool

## Overview
A secure, interactive tool developed for Centrala University's 
School of Medicine to safely search, download, validate, and 
store pharmaceutical trial data from a partner FTP server.

## Features
- FTP connection management using the Singleton design pattern
- Seven-gate CSV validation pipeline
- CLI and GUI user interfaces
- Automated test data generation
- External API integration for error log GUID generation
- Comprehensive error logging

## Requirements
- Python 3.8 or higher
- No external packages required
- Internet connection required for UUID API (fallback available)

## Running the Application

### CLI Interface
python3 cli.py

### GUI Interface
python3 gui.py

### Run All Tests
python3 -m unittest discover -v

### Generate Test Data
python3 generate_test_data.py