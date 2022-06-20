from domonic.html import *
from domonic.ext.html5lib_ import getTreeBuilder
import html5lib
from util import load_json
import grapher


class HTMLBuilder:
    __templates = {
        "std": "library/templates/std_template.html",
        "concise": "",
        "dashboard": ""
    }

    __profiles = {
        "std_prof": "library/profiles/std_prof.json",
        "sus_prof": "library/profiles/sus_prof.json",
        "ee_prof": "library/profiles/ee_prof.json"
    }

    def __init__(self, data, profile="std_prof", custom_profile=None, template="std", custom_template=None):
        self.page = self.read_template(custom_template or self.__templates[template])
        self.profile = load_json(custom_profile or self.__profiles[profile])
        self.metrics_library = load_json('library/metrics_library.json')
        self.data = data

    def __build_metric_div(self, name, value, icon, rating=None):
        return div(_class="h-organizer").html(
            div(_class="item-left").html(
                h1(_class="metric-text").html(name)
            ),
            div(_class="item-left").html(
                span(_class=(
                    "material-symbols-outlined green" if icon == "eco" else "material-symbols-outlined yellow")).html(
                    icon)
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
                img(_class="energy-icon", src="template/content/rating_ap.svg")
                if value == "A+" else
                h2(_class="metric-text").html(value)
            )
        )

    def __build_energy_graph(self, y1, y2, x):
        img_path = grapher.rn_energy_adapt(y1, y2, x)
        return img(src=img_path, _class='figure')

    def generate_domain(self):
        business_append = self.page.getElementById("businessAppend")

        for metric in self.data["domain"]:
            name = metric['name']
            value = metric['value']
            business_append.append(self.__build_business_div(name, value))       

    def generates_graphs(self):
        graph_append = self.page.getElementById("graphAppend")

        comment = p(_class="comment").html("No significant adaptation of energy consumption.")
        graph_append.append(comment)

    def generate_metrics(self):
        metrics_append = self.page.getElementById("metricAppend")

        for metric in self.profile['builtin_metrics']:
            value = self.data['builtin_metrics'][metric]
            icon = self.metrics_library[metric]['icon']

            metrics_append.append(self.__build_metric_div(metric, value, icon))

    def read_template(self, path):
        file = open(path, "r")
        parser = html5lib.HTMLParser(tree=getTreeBuilder())
        return parser.parse(file)

    def write_html(self, path="eesr-report.html"):
        f = open(path, "w")
        f.write(f"{self.page}")
        f.close()
