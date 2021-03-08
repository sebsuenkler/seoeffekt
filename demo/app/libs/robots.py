from helpers import Helpers

def check_robots(main):
    robots_url = main+'robots.txt'
    source = Helpers.saveResult(robots_url)

    try:
        source = Helpers.saveResult(robots_url)
        s_robot = source.lower()


        value = 0

        p = "*crawl-delay*"
        if Helpers.matchText(s_robot, p):
            value = 1

        p = "*user agent*"
        if Helpers.matchText(s_robot, p):
            value = 1

        p = "*user-agent*"
        if Helpers.matchText(s_robot, p):
            value = 1

        p = "*sitemap*"
        if Helpers.matchText(s_robot, p):
            value = 1

        p = "*noindex*"
        if Helpers.matchText(s_robot, p):
            value = 1

    except:
        value  = -1

    return value
