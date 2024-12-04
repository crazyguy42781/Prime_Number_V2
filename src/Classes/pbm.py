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
import os
import json
from datetime import datetime

# Third-Party Imports

# Local Imports

# Constants
BITS_IN_2_32 = 2**32
BLOCK_BATCH_SIZE = 256  # Total number of blocks to cover up to 2^40
JSON_DIR = "Database/json_blocks"  # Directory to store JSON files


def main() -> None:
    # this is used for testing and imports in other parts of the program.
    # Step 1: Create blank blocks
    manager = PrimeBlockManager(total_blocks=16)
    manager.create_blank_blocks()

    # Step 2: Verify the created files
    blocks = manager.list_blocks()
    print(f"Created {len(blocks)} block files: ")
    print(blocks[:5])  # Print the first 5 block filenames for verification

    return


class PrimeBlockManager:
    def __init__(self, block_size=BITS_IN_2_32, total_blocks=BLOCK_BATCH_SIZE) -> None:
        self.block_size = block_size
        self.total_blocks = total_blocks
        self.init_directory()

    @staticmethod
    def init_directory() -> None:
        """Ensure the JSON directory exists."""
        if not os.path.exists(JSON_DIR):
            os.makedirs(JSON_DIR)
        return

    def create_blank_blocks(self) -> None:
        """Create 256 blank JSON files with appropriate filenames."""
        for i in range(self.total_blocks):
            block_filename = f"2_32-{str(i).zfill(4)}.json"

            blank_block = {
                "file_version": "1.0",
                "base": 174,
                "conversion_type": "prime gaps",
                "chain": {
                    "previous_file": f"2_32-{str(i - 1).zfill(4)}.json" if i > 0 else "Genesis",
                    "current_file": f"2_32-{str(i).zfill(4)}.json" if i < self.total_blocks - 1 else None,
                    "next_file": f"2_32-{str(i + 1).zfill(4)}.json" if i < self.total_blocks - 1 else None,
                },
                "metadata": {
                    "start_prime": i * self.block_size,
                    "end_prime": ((i + 1) * self.block_size) - 1,
                    "array_start_value": None,
                    "array_end_value": None,
                    "last_prime": None,
                    "trailing_zeros": None,
                    "total_primes": None,
                    "total_gaps": None,
                    "max_gap": None,
                    "start_max_gap_location": None,
                    "end_max_gap_location": None,
                    "min_gap": None,
                    "average_gap": None,
                    "encoded_data_size": None,
                    "compression_size": None,
                    "sha256_hash": None,
                    "bit_array_size": self.block_size,
                },
                "system_info": {
                    "generator": "PrimeEncoder v2.0",
                    "creation_date": datetime.now().isoformat(),
                    "author": "Prime Saver",
                    "notes": "This is for saving the primes up to as far as space "
                             "will allow.",
                },
                "data": {
                    "structure": {
                        "chunk_size": 8_388_608,
                        "chunk_count": 512,
                    },
                    "encoded_data": ""
                }
            }

            file_path = os.path.join(JSON_DIR, block_filename)
            with open(file_path, "w") as f:
                json.dump(blank_block, f, indent=4)

        print(f"Created {self.total_blocks} blank blocks in {JSON_DIR}.")

        return

    @staticmethod
    def list_blocks() -> list:
        """List all block files in the directory."""
        return sorted([f for f in os.listdir(JSON_DIR) if f.endswith(".json") and
                       "2_32" in f])

    @staticmethod
    def load_block(filename) -> json:
        """Load a block by filename."""
        with open(os.path.join(JSON_DIR, filename), "r") as f:
            return json.load(f)


if __name__ == '__main__':
    main()
