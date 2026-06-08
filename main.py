import subprocess

subprocess.run(["python", "scripts/script1_scrape.py"], check=True)
subprocess.run(["python", "scripts/script2_transform.py"], check=True)
subprocess.run(["python", "scripts/script3_create_db.py"], check=True)
subprocess.run(["python", "scripts/script4_insert_data.py"], check=True)