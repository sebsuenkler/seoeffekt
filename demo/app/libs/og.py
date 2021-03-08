from helpers import Helpers

def check_og(code):
    pattern = '*meta*og*'
    value = 0

    if Helpers.matchText(code, pattern):
        value = 1

    return value
