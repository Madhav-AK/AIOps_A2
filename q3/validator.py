import csv
import os
import re
import time


def is_valid_email(email):
    pattern = r"[^\s@]+@[^\s@.]+(?:\.[^\s@.]+)+"
    match = re.fullmatch(pattern, email)
    return match is not None


def main():
    job_index = int(os.environ["JOB_COMPLETION_INDEX"])
    shard_number = job_index + 1
    filename = f"user_signup_data_{shard_number}.csv"
    data_dir = os.environ.get("DATA_DIR", "data")
    file_path = f"{data_dir}/{filename}"

    required_fields = ["id", "first name", "email", "phone"]
    total_rows = 0
    invalid_rows = 0

    time.sleep(10)

    with open(file_path, newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            total_rows += 1
            row_is_invalid = False

            for field in required_fields:
                value = row.get(field)
                if value is None:
                    row_is_invalid = True
                elif value.strip() == "":
                    row_is_invalid = True

            email = row.get("email")
            if email is None:
                row_is_invalid = True
            elif not is_valid_email(email):
                row_is_invalid = True

            if row_is_invalid:
                invalid_rows += 1

    pod_name = os.environ.get("POD_NAME", "unknown")
    node_name = os.environ.get("NODE_NAME", "unknown")

    print(f"Pod: {pod_name}", flush=True)
    print(f"Node: {node_name}", flush=True)
    print(f"Job index: {job_index}", flush=True)
    print(f"Shard: {filename}", flush=True)
    print(f"Total rows: {total_rows}", flush=True)
    print(f"Invalid rows: {invalid_rows}", flush=True)


if __name__ == "__main__":
    main()
