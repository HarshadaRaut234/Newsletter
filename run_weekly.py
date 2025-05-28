import subprocess

print("Running web_scrapper.py...")
subprocess.run(["python3", "web_scrapper.py"], check=True)

print("Running insert.py...")
subprocess.run(["python3", "insert.py"], check=True)

print("Running mail_sender.py...")
subprocess.run(["python3", "mail_sender.py"], check=True)

print("Weekly newsletter sent successfully.")
