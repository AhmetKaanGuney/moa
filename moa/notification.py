"""Error handling"""
# ------------------------ #
#       ERROR CLASS        #
# ------------------------ #
class Notification:
    """This class' methods can be called from everywhere.
    It'll be used for displaying error messages and warnings to the user via the GUI."""
    @staticmethod
    def raise_error(message):
        print(f"ERROR: {message}")
        return "ERROR"

    @staticmethod
    def raise_warning(message):
        print(f"ERROR: {message}")
        return "ERROR"
