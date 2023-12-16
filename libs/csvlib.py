
import csv
import os
import shutil
from datetime import datetime


def write_to_csv(file_info_list, csv_file):
    """
    Write file information to a CSV file.
    """
    with open(csv_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Path', 'Last Modification Time'])

        for file_path, mod_time in file_info_list:
            csv_writer.writerow([file_path, mod_time])


def create_empty_csv(csv_file):
    """
    Check if a CSV file exists and create an empty file if it doesn't.
    """
    if not os.path.exists(csv_file):
        with open(csv_file, 'w', newline='') as csvfile:
            # Create an empty CSV file with a header
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([])

        print(f"Empty CSV file created: {csv_file}")
    else:
        print(f"CSV file already exists: {csv_file}")


def read_csv(csv_file):
    """
    Read data from a CSV file and return it as a list of tuples.
    """
    data = []
    with open(csv_file, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  # Skip header
        for row in csv_reader:
            path = row[0]
            mod_time = int(row[1])
            data.append((path, mod_time))
    return data