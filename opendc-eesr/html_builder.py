from random import randint
from xml.etree.ElementTree import TreeBuilder
from domonic.html import *
from domonic.ext.html5lib_ import getTreeBuilder
import html5lib
import json
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline


def build_metric_div(name, value, type, rating=None):
    return div(_class="h-organizer").html(
        div(_class="item-left").html(
            h1(_class="metric-text").html(name)
        ),
        div(_class="item-left").html(
            span(_class=("material-symbols-outlined green" if type == 1 else "material-symbols-outlined yellow")).html("eco" if type == 1 else "electric_bolt")
        ),
        div(_class="item-right").html(
            h1(_class="metric-text").html(value)
        )
    )

def build_business_div(name, value):
    return div(_class="h-organizer").html(
        div(_class="item-left").html(
            h2(_class="metric-text").html(name)
        ),
        div(_class="item-right").html(
            h2(_class="metric-text").html(value)
        )
    )

def build_energy_graph(x1, x2):
    plt.figure(dpi=1200)
    plt.plot(x1)
    plt.plot(x2)
    plt.ylabel("Energy Consumption (MWh)")
    plt.xlabel("Time Period i")
    plt.grid(axis = 'y')
    plt.savefig('template/content/energy_graph.png')
    return img(src='content/energy_graph.png', _class='figure')

def insert_business_related(page, data):
    business_append = page.getElementById("businessAppend")

    for metric in data["business"]:
        name, value = metric.popitem()
        business_append.append(build_business_div(name, value))

def insert_visuals(page, data):
    graph_append = page.getElementById("graphAppend")
    
    x1, x2 = data["data_points"][0].popitem()[1]
    energy_graph = build_energy_graph(x1, x2)

    graph_append.append(energy_graph)

def insert_metrics(page, data):
    metrics_append = page.getElementById("metricAppend")

    for metric in data["metrics"]:
        name, value = metric.popitem()
        metrics_append.append(build_metric_div(name, value, randint(0,1)))

def read_template(path="template/template.html"):
    file = open(path, "r")
    parser = html5lib.HTMLParser(tree=getTreeBuilder())
    return parser.parse(file)

def write_html(page, path="template/eesr-report.html"):
    f = open("template/eesr-report.html", "w")
    f.write(f"{page}")
    f.close()
