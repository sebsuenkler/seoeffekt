from helpers import Helpers

def check_viewport(code):
    pattern = '*meta*viewport*'

    value = 0

    if Helpers.matchText(code, pattern):
        value = 1

    return value
