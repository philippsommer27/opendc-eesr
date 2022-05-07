from domonic.html import *
from domonic.ext.html5lib_ import getTreeBuilder
import html5lib
import domonic

f = open("output/template.html", "r")
parser = html5lib.HTMLParser(tree=getTreeBuilder())
page = parser.parse(f)

metric_1 = page.getElementById("metric_1")

print(metric_1)

# f = open("output/eesr-report.html", "w")
# f.write(f"{page}")
# f.close()

