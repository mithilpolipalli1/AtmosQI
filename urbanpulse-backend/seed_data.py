import requests

cities = ["Hyderabad", "Delhi", "Mumbai", "Bengaluru", "Chennai", "Kolkata"]

for c in cities:
    w = requests.post(f"http://127.0.0.1:8000/ingest/weather/{c}")
    a = requests.post(f"http://127.0.0.1:8000/ingest/air-quality/{c}")
    print(f"{c}: Weather={w.status_code}, AQI={a.status_code}")

print("Done! All cities ingested.")
