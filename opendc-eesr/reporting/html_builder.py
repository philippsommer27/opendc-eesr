from domonic.html import *
from domonic.ext.html5lib_ import getTreeBuilder
import html5lib
from util import load_json, generate_unique_id
from reporting import grapher


class HTMLBuilder:
    __templates = {
        "std": "reporting/library/templates/std_template.html",
        "compact": "reporting/library/templates/compact_template.html",
    }

    __profiles = {
        "std_prof": "reporting/library/profiles/std_prof.json",
        "sus_prof": "reporting/library/profiles/sus_prof.json",
        "ee_prof": "reporting/library/profiles/ee_prof.json"
    }

    def __init__(self, data, profile="std_prof", custom_profile=None, template="std", custom_template=None):
        self.page = self.read_template(custom_template or self.__templates[template])
        self.profile = load_json(custom_profile or self.__profiles[profile])
        self.metrics_library = load_json('reporting/library/metrics_library.json')
        self.data = data

    def __build_metric_div(self, name, value, icon, link, rating=None):
        return div(_class="h-organizer").html(
            div(_class="item-left").html(
                h1(_class="metric-text").html(
                    a(name,
                    _href=link,
                    _target="_blank",
                    _class="a-remover"
                    ))
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
                h2(_class="metric-text").html(f'{value:.2f}')
            )
        )

    def __build_graph(self, graph_data):
        img_path = grapher.selector(self.profile['graph'], graph_data)
        return img(src=img_path, _class='figure')

    def generate_domain(self):
        business_append = self.page.getElementById("businessAppend")

        for metric in self.data["domain"]:
            name = metric['name']
            value = metric['value']
            business_append.append(self.__build_business_div(name, value))       

    def generates_graph(self, graph_data):
        graph_append = self.page.getElementById("graphAppend")
        
        graph_append.append(self.__build_graph(graph_data))

        if "graph_comment" in self.data:
            comment = p(_class="comment").html(self.data['graph_comment'])        
            graph_append.append(comment)
        

    def generate_metrics(self):
        metrics_append = self.page.getElementById("metricAppend")

        for metric in self.profile['builtin_metrics']:
            value = self.data['builtin_metrics'][metric]
            icon = self.metrics_library[metric]['icon']
            link = self.metrics_library[metric]['documentation']

            metrics_append.append(self.__build_metric_div(metric, value, icon, link))

    def generate_meta(self):
        bottom_name_append = self.page.getElementById("bottomNameAppend")
        bottom_value_append = self.page.getElementById("bottomValueAppend")

        duration = self.data['metadata']['start_date'] + " to " + self.data['metadata']['end_date']
        bottom_name_append.append(p("Timeframe"))
        bottom_value_append.append(p(duration))

        bottom_name_append.append(p("Environment"))
        if "environment_link" in self.data['metadata']:
            bottom_value_append.append(p().html(a(
                self.data['metadata']['environment'],
                _href=self.data['metadata']['environment_link'],
                _target="_blank"
            )))
        else:
            bottom_value_append.append(p(self.data['metadata']['environment']))

        bottom_name_append.append(p("Report ID"))
        bottom_value_append.append(p(generate_unique_id(self.data)))

    def read_template(self, path):
        file = open(path, "r")
        parser = html5lib.HTMLParser(tree=getTreeBuilder())
        return parser.parse(file)

    def write_html(self, path="report.html"):
        f = open(path, "w")
        f.write(f"{self.page}")
        f.close()
