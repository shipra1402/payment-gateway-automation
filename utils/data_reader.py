import csv
import os


def read_login_data():
    # Get project root directory
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    # Build correct path
    file_path = os.path.join(BASE_DIR, "test_data", "login_data.csv")

    data = []

    with open(file_path, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append((
                row["username"],
                row["password"],
                row["expected_result"],
                row["test_id"]
            ))

    return data