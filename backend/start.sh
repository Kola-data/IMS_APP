#!/bin/bash

if [ -d "venv" ]; then
    source venv/bin/activate
    echo "Virtual environment activated."
else
    echo "No virtual environment found. Please set up the virtual environment first."
    exit 1
fi

uvicorn main:app --host 0.0.0.0 --port 8080 --reload