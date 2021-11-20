"""Error handling"""
# ------------------------ #
#       ERROR CLASS        #
# ------------------------ #
class Notification:
    """This class' methods can be called from everywhere.
    It'll be used for displaying error messages and warnings to the user via the GUI."""
    @classmethod
    def raise_error(cls, message):
        cls.error_message = message
        print(f"ERROR: {message}")
        return "ERROR"

    @classmethod
    def raise_warning(cls, message):
        cls.warning_message = message
        print(f"ERROR: {message}")
        return "ERROR"
