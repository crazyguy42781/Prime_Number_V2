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

# Third-Party Imports

# Local Imports
from Classes.base_converter import BaseConvert
from Classes.pbm import PrimeBlockManager
from Classes.dpm import ProgressManager
from Classes.sieve import SieveProcessor

# Constants
JSON_DIR = "Database/json_blocks"  # Directory to store JSON files


def main() -> None:
    # This is the primary function to start your program.
    # Setting up the classes so they can be passed around instead of being loaded
    # each time in every class and cause a circle error.
    convert = BaseConvert()
    pbm = PrimeBlockManager()
    dpm = ProgressManager(JSON_DIR +"/progress.json")
    sieve = SieveProcessor(bc=convert, pbm=pbm, dpm=dpm)


    return


if __name__ == '__main__':
    main()
