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
import sys
import json

# Third-Party Imports
from bitarray import bitarray

# Local Imports
from base_converter import BaseConvert

# Setting max string digigs
sys.set_int_max_str_digits(1_000_000_000)


def main() -> None:
    # this is used for testing and imports in other parts of the program.
    sieve = SieveProcessor(limit=10)
    sieve.print_data()
    sieve.reset_array()

    return


class SieveProcessor:
    def __init__(self, limit=1_000_000, bc=None, pbm=None, dpm=None) -> None:
        # setting up necessary imports from main.py
        self.bc = bc  # Base Converter
        self.pbm = pbm  # Prime Block Manager
        self.dpm = dpm  # Data Progress Manager

        # setting up bit array
        self.limit = limit
        self.bit_array = bitarray(self.limit)
        self.bit_array.setall(True)
        self.sieve_string = ""
        self.metadata = {
            "array_start_value": None,
            "array_end_value": None,
            "last_prime": 4294967291,
            "trailing_zeros": 2,
            "max_gap": 336,
            "encoded_data_size": 209384241,
        }

    def reset_array(self) -> None:
        self.bit_array.setall(True)
        self.sieve_string = ""
        for key, value in self.metadata.items():
            self.metadata[key] = None
        self.print_data()
        return

    def print_data(self) -> None:
        print(json.dumps(self.metadata, indent=4))
        return

    @staticmethod
    def distance_exceed(number: int, prime: int) -> int:
        """
        Calculate the distance to the next multiple of a prime relative to the given number.
        :param number: The number to align.
        :param prime: The prime number used for alignment.
        :return: Distance to the next multiple of the prime.
        """
        remainder = number % prime
        return 0 if remainder == 0 else prime - remainder

    def genesis_sieve(self) -> None:
        stop = int(self.limit ** 0.5) + 1
        idx = 0
        gap = 0
        start_gap_location = 0
        end_gap_location = 0
        min_gap = 10000000
        total_primes = 0
        convert = BaseConvert()
        self.bit_array[:2] = False  # Mark 0 and 1 as non-prime

        while idx < self.limit:
            num = self.bit_array.find(1, idx)

            if num < 0:
                # No more primes; calculate trailing zeros and exit
                last_prime = idx - 1
                trailing_zeros = self.bit_array[idx:].count(0)
                print(f"Last prime: {last_prime:,}")
                self.sieve_string += f"[{convert.encode(trailing_zeros)}]"
                self.metadata["last_prime"] = last_prime
                self.metadata["trailing_zeros"] = trailing_zeros
                break

            if num < stop:  # Only mark multiples for primes ≤ sqrt(limit)
                self.bit_array[num * num: self.limit + 1: num] = False

            # Calculate gap and encode it
            gap_size = num - idx
            gap_encoding = convert.encode(gap_size)
            self.sieve_string += gap_encoding

            # Track maximum gap with location
            if gap_size > gap:
                gap = gap_size
                start_gap_location = idx - 1
                end_gap_location = num

            # Track minimum gap
            if gap_size < min_gap:
                min_gap = gap_size

            # Log progress for large gaps
            if gap_size > 175:
                progress = (num / self.limit) * 100
                print(
                    f"Stop Prime: {num:,} - Gap: {gap_size} - Encoded: {gap_encoding} - {progress:.2f}% Complete")

            # counting primes
            total_primes += 1
            idx = num + 1

        # Store metadata
        self.metadata["array_start_value"] = 0
        self.metadata["array_end_value"] = self.limit - 1
        self.metadata["max_gap"] = gap
        self.metadata["start_max_gap_location"] = start_gap_location
        self.metadata["end_max_gap_location"] = end_gap_location
        self.metadata["encoded_data_size"] = len(self.sieve_string)
        self.metadata["min_gap"] = min_gap
        self.metadata["total_primes"] = total_primes
        self.metadata["compression_size"] = len(self.sieve_string)

        return None

    def sieve(self, current_array=None, start_prime=None):
        # resets the bitarray without rebuilding it
        self.reset_array()
        idx = 0
        prime_count = 0
        value = ""
        while idx < len(current_array):
            if current_array[idx] == "[":
                break
            elif current_array[idx] == ":":
                start_idx = idx + 1
                end_idx = current_array.find("|", start_idx)
                if end_idx == -1 or end_idx - start_idx > 6:
                    end_idx = start_idx + 2
                value = current_array[start_idx:end_idx]
                idx += (end_idx - start_idx)
            else:
                value = current_array[idx]

            prime_count += self.bc.to_decimal(value)
            distance = self.distance_exceed(start_prime
                                            , prime_count)
            if distance > len(self.bit_array):
                self.bit_array[distance] = False
            else:
                self.bit_array[distance: self.limit: prime_count] = False
            idx += 1

        return None

    def convert_sieve(self) -> (int, str, int, int):
        last_idx = 0
        idx = 0
        p = 0
        gap = 0
        gap_size = 0
        min_gap = 1_000_000
        last_prime = 0
        s = ""
        c = ""
        last_p = 0
        # while idx <= self.limit:
        #     p = self.bit_array.find(1, idx)
        #     if p < 1:
        #         last_p = idx - 1
        #         s += f"[{BaseConvert((self.limit - 1) - idx).encode()}]"
        #         break
        #     if p == 1:
        #         p = 2
        #     gap_size = p - last_idx
        #     c = BaseConvert(gap_size).encode()
        #     s += c
        #     if gap_size > gap:
        #         gap = gap_size
        #     if gap_size > 125:
        #         d = ((idx / self.limit) * 100)
        #         print(f"Stop Prime: {p:,} - gap: {gap_size} - Converted: {c} - "
        #               f"{d:.2f}%")
        #     idx = p + 1
        #     last_idx = p
        while idx < self.limit:

            if self.bit_array[idx]:
                c = BaseConvert(gap_size).encode()
                s += c
                last_prime = idx
                if gap_size > gap:
                    gap = gap_size
                if gap_size < min_gap:
                    min_gap = gap_size
                if gap_size > 225:
                    d = ((idx / self.limit) * 100)
                    print(f"Stop Prime: {idx:,} - gap: {gap_size} - Converted: "
                          f"{c} - {d:.2f}%")
                gap_size = 0
            else:
                gap_size += 1
            idx += 1
        s += f"[{BaseConvert(gap_size).encode()}]"
        return gap, s, gap_size, min_gap, last_prime


if __name__ == '__main__':
    main()
