#!/bin/bash

# Quick script to run the demo with virtual environment

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run ./setup_venv.sh first"
    exit 1
fi

# Activate venv and run demo
source venv/bin/activate
python demo_queries.py
