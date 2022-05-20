from random import randint
from xml.etree.ElementTree import TreeBuilder
from domonic.html import *
from domonic.ext.html5lib_ import getTreeBuilder
import html5lib
import json
from profiles import prof
from scipy.interpolate import make_interp_spline, BSpline
import grapher

class HTMLBuilder:

    __template_path = "template/std_template.html"
        
    def __init__(self, data, profile="std_prof", custom_profile=None, custom_template=None) -> None:
        self.page = self.read_template(custom_template)
        self.profile = self.read_profile(custom_profile or prof[profile])
        self.data = data

    def read_profile(self, path):
        with open(path, "r") as read_file:
            return json.load(read_file)
        
    def __build_metric_div(self, name, value, type, rating=None):
        return div(_class="h-organizer").html(
            div(_class="item-left").html(
                h1(_class="metric-text").html(name)
            ),
            div(_class="item-left").html(
                span(_class=("material-symbols-outlined green" if type == "eco" else "material-symbols-outlined yellow")).html(type)
            ),
            div(_class="item-right").html(
                h1(_class="metric-text").html(f'{value:.2f}')
            )
        )

    def __build_business_div(self, name, value):
        return div(_class="h-organizer").html(
            div(_class="item-left").html(
                h2(_class="metric-text").html(name)
            ),
            div(_class="item-right").html(
                h2(_class="metric-text").html(value)
            )
        )

    def __build_energy_graph(self, y1, y2, x):
        img_path = grapher.rn_energy_adapt(y1, y2, x)
        return img(src=img_path, _class='figure')

    def generate_business_related(self):
        business_append = self.page.getElementById("businessAppend")

        for metric in self.data["business"]:
            name, value = metric.popitem()
            business_append.append(self.__build_business_div(name, value))

    def generates_graphs(self):
        graph_append = self.page.getElementById("graphAppend")
        
        y1, y2, x = self.data["data_points"][0].popitem()[1]
        y1 = [x+10 for x in y1]
        energy_graph = self.__build_energy_graph(y1, y2, x)

        graph_append.append(energy_graph)
        
        comment = p(_class="comment").html("No significant adaptation of energy consumption.")
        graph_append.append(comment)

    def generate_metrics(self):
        metrics_append = self.page.getElementById("metricAppend")
        icons = self.profile["icons"]
        
        for metric in self.data["metrics"]:
            name, value = metric.popitem()
            icon_name = icons[name]
            metrics_append.append(self.__build_metric_div(name, value, icon_name))

    def read_template(self, path=None):
        file = open(path or self.__template_path, "r")
        parser = html5lib.HTMLParser(tree=getTreeBuilder())
        return parser.parse(file)

    def write_html(self, path="eesr-report.html"):
        f = open(path or "eesr-report.html", "w")
        f.write(f"{self.page}")
        f.close()
