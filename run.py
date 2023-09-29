import os
import subprocess

if not os.path.exists(".env"):
    # Create a virtual environment
    subprocess.run(["python3", "-m", "venv", ".env"])
    subprocess.run(["source", ".env/bin/activate"], shell=True)
    subprocess.run(["pip", "install", "-r", "requirements.txt"])
else:
    subprocess.run(["source", ".env/bin/activate"], shell=True)

print("Virtual environment activated")

# Assuming url_extractor.py and scrapy.py are in the same directory as this script
subprocess.run(["python", "url_extractor.py", "input.xlsx"])
subprocess.run(["python", "scrapy.py", "google_urls.txt"])