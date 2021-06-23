from lxml import html


xpath = "//a[@aria-label='Page 3']"

f = open("test.html", "r")
source = f.read()


tree = html.fromstring(source)
content = tree.xpath(xpath)

print(content)
