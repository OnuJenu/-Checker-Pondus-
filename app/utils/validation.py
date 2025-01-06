# Helper functions for input validation

from os.path import splitext

def validate_poll_input(question, option_one, option_two):
    # Logic to validate poll input
    pass

def check_file_extension(filename, allowed_extensions):
    _, ext = splitext(filename)
    return ext.lower() in allowed_extensions
