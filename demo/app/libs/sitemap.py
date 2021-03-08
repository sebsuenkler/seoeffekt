from helpers import Helpers


def check_sitemap(code):
    pattern = "*sitemap*"

    sitemap_counter = 0

    if (Helpers.matchText(code, pattern)):
        sitemap_counter = sitemap_counter + 1

    if sitemap_counter > 0:
        value = 1
    else:
        value = 0

    return value
