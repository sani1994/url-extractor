#!/bin/bash

if [ ! -d ".env" ]
then
  python3 -m venv .env
  source .env/bin/activate
  pip install -r requirements.txt
else
  source .env/bin/activate
fi
echo "Virtual environment activated"
python url_extractor.py input.xlsx
python scrapy.py google_urls.txt
