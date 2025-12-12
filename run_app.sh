#!/usr/bin/env bash
# Quick start script for Linux/macOS
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run digital_transformation_query_app.py

