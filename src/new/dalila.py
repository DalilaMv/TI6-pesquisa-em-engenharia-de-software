import csv
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

CONNECTION_STRING = os.environ["CONNECTION_STRING"]
DB_NAME = os.environ["DB_NAME"]


def get_events(nameWithOwner, start_time, end_time):
    try:
        client = MongoClient(CONNECTION_STRING)
        db = client[DB_NAME]
    except:
        print("Não foi possível conectar-se ao servidor do MongoDB:")

    collection = db[nameWithOwner]
    query = {"created_at": {"gte": start_time,"$lte": end_time}}
    events = collection.find(query)
    return [event for event in events]

def main():
    with open("./csv2_intervalos.csv", "r") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames + ["types"]
        with open("eventos.csv", "w", newline="") as f_out:
            writer = csv.DictWriter(f_out, fieldnames=fieldnames)
            writer.writeheader()
            for row in reader:
                nameWithOwner = row["nameWithOwner"]
                # failed_time = datetime.strptime(row["failed_time"], "%Y-%m-%d %H:%M:%S")
                # success_time = datetime.strptime(row["success_time"], "%Y-%m-%d %H:%M:%S")
                failed_time = datetime.fromisoformat(row["failed_time"])
                success_time = datetime.fromisoformat(row["success_time"])
                types = get_events(nameWithOwner, failed_time, success_time)
                row["types"] = "|".join(types)
                writer.writerow(row)

if __name__ == "__main__":
    main()