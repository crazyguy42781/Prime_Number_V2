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

def main() -> None:
    # this is used for testing and imports in other parts of the program.
    convert = BaseConvert()
    print(f"Encoding 2542415: {convert.encode(2542415)}")
    print(f"Decoding ajJJD: {convert.to_decimal('ajJJD'):_}")

    return


class BaseConvert:
    """
    This is Base Convert class. it accepts base 10 numbers and converts it to base 174
    """

    # Class base variables
    NUMERAL = "0123456789"
    UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    LOWER = "abcdefghijklmnopqrstuvwxyz"
    EXTRAS = "!@#$%^&*-_=+<,.>/?"
    ABOVE_EXTRAS = "¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ"
    BASE = NUMERAL + UPPER + LOWER + EXTRAS + ABOVE_EXTRAS
    FOLDER_PATH = "database/"

    def __init__(self, value=None):
        self.value = value

    def __lt__(self, other):
        return self.to_decimal() < other.to_decimal()

    def __le__(self, other):
        return self.to_decimal() <= other.to_decimal()

    def __eq__(self, other):
        return self.to_decimal() == other.to_decimal()

    def __ne__(self, other):
        return self.to_decimal() != other.to_decimal()

    def __ge__(self, other):
        return self.to_decimal() >= other.to_decimal()

    def __gt__(self, other):
        return self.to_decimal() > other.to_decimal()

    def to_decimal(self, value=None) -> int:
        """
        to_decimal takes in an str and returns a int value
        """
        self.value = value if value is not None else self.value
        if self.value is None:
            raise ValueError("Value not provided.")
        base = len(self.BASE)
        result = 0

        for char in self.value:
            result = result * base + self.BASE.index(char)
        return result

    def __repr__(self):
        return f"Base{len(self.BASE)}Number({self.value})"

    def encode(self, value=None) -> str:
        """
        encode takes in an int and returns a str. If the length of the string is
        bigger than 1. it adds a : in front of the string. if the len is > than 2.
        it adds | to the end to sigal the end of the group.
        """
        self.value = value if value is not None else self.value
        if self.value is None:
            raise ValueError("Value not provided.")
        if self.value == 0:
            return self.BASE[0]

        result = ""
        base = len(self.BASE)
        while self.value > 0:
            self.value, remainder = divmod(self.value, base)
            result = self.BASE[remainder] + result
        if len(result) > 1:
            result = ":" + result
        if len(result[1:]) > 2:
            result = result + "|"
        return result


if __name__ == '__main__':
    main()
