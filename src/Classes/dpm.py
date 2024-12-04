"""
Prime Number V2 Program
Copyright (c) 2024 Adam Smith

Open Source Software under the Prime Number V2 Program License (Modified MIT)
For commercial use, contact liversmiles@gmail.com.

Permission is hereby granted, free of charge, to any person obtaining a copy of this 
software and associated documentation files (the "Software"), to deal in the Software 
without restriction, subject to the conditions specified in the license.
"""


# Standard Library Imports
import json
import os
from datetime import datetime

# Third-Party Imports

# Local Imports

# Constants
JSON_DIR = "Database/json_blocks"  # Directory to store JSON files


def main() -> None:
    # this is used for testing and imports in other parts of the program.
    # Initialize Progress Manager
    progress = ProgressManager(JSON_DIR +"/progress.json")
    progress.load_progress()
    if progress.progress_data["file_list"] == {}:
        for each in progress.list_blocks():
            progress.progress_data["file_list"][each] = False
    progress.print_summary()
    progress.save_progress()
    return


class ProgressManager:
    def __init__(self, progress_file):
        self.progress_file = progress_file
        self.file_not_created = False
        self.progress_data = {
            "status": {
                "genesis_completed": False,
                "current_file": None,
                "files_in_progress": [],
                "total_completed_files": 0,
                "timestamp": self.get_timestamp()
            },
            "sieve_metadata": {
                "genesis": {
                    "file_name": "2_32-0000.json",
                    "completed": False,
                    "last_prime_processed": None
                },
                "in_progress": []
            },
            "settings": {
                "max_parallel_files": 3,
                "block_size": 4294967296,
                "base": 174
            },
            "system_info": {
                "generator": "PrimeEncoder v2.0",
                "last_updated": self.get_timestamp(),
                "notes": "Resumes from last checkpoint."
            },
            "file_list": {},
        }

    @staticmethod
    def get_timestamp():
        return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    def save_progress(self):
        self.progress_data["status"]["timestamp"] = self.get_timestamp()
        self.progress_data["system_info"]["last_updated"] = self.get_timestamp()
        with open(self.progress_file, 'w') as file:
            json.dump(self.progress_data, file, indent=4)
        self.file_not_created = True

    def load_progress(self):
        try:
            with open(self.progress_file, 'r') as file:
                self.progress_data = json.load(file)
        except FileNotFoundError:
            print("Progress file not found. Starting fresh.")
            self.save_progress()

    def update_genesis(self, completed, last_prime=None):
        self.progress_data["sieve_metadata"]["genesis"]["completed"] = completed
        self.progress_data["sieve_metadata"]["genesis"][
            "last_prime_processed"] = last_prime
        self.save_progress()

    def add_in_progress_file(self, file_name, start_prime, last_prime=None):
        if len(self.progress_data["status"]["files_in_progress"]) < \
                self.progress_data["settings"]["max_parallel_files"]:
            self.progress_data["sieve_metadata"]["in_progress"].append({
                "file_name": file_name,
                "start_prime": start_prime,
                "last_prime_processed": last_prime
            })
            self.progress_data["status"]["files_in_progress"] = [
                f["file_name"] for f in
                self.progress_data["sieve_metadata"]["in_progress"]
            ]
            self.save_progress()

    def mark_file_complete(self, file_name):
        self.progress_data["sieve_metadata"]["in_progress"] = [
            f for f in self.progress_data["sieve_metadata"]["in_progress"] if
            f["file_name"] != file_name
        ]
        self.progress_data["status"]["files_in_progress"] = [
            f["file_name"] for f in self.progress_data["sieve_metadata"]["in_progress"]
        ]
        self.progress_data["status"]["total_completed_files"] += 1
        self.save_progress()

    def print_summary(self):
        """Prints a summary of the JSON file data."""
        print(json.dumps(self.progress_data, indent=4))

    @staticmethod
    def list_blocks() -> list:
        """List all block files in the directory."""
        return sorted([f for f in os.listdir(JSON_DIR) if f.endswith(".json") and
                       "2_32" in f])


if __name__ == '__main__':
    main()
