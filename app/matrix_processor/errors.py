"""Error handling"""
# ------------------------ #
#       ERROR CLASS        #
# ------------------------ #
class Error(Exception):
    """Base class for exeptions in this module."""
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    @classmethod
    def set_message(cls, message):
        cls.message = message
        print(f"{cls.WARNING}{message}{cls.ENDC}")


class DuplicationError(Error):
    "Raised when an operation attemps to create duplicate keys in a dictionary."
    def __init__(self, msg):
        Error.set_message(msg)


class EmptyError(Error):
    "Raised when something is empty when it shouldn't."
    def __init__(self, msg):
        Error.set_message(msg)


class NaNError(Error):
    "Raised when a NaN value is detected."
    def __init__(self, msg):
        Error.set_message(msg)

