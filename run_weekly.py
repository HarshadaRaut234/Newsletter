import subprocess
import sys

print("Running web_scrapper.py...")
subprocess.run([sys.executable, "web_scrapping.py"], check=True)

print("Running insert.py...")
subprocess.run([sys.executable, "insert.py"], check=True)

print("Running mail_sender.py...")
subprocess.run([sys.executable, "mail_sender.py"], check=True)

print("Weekly newsletter sent successfully.")
