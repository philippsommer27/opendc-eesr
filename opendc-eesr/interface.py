from operator import index
from reporting import run_basic_validation, html_builder, grapher
from analysis import GridAnalysis, process
import json
import logging
from util import inline
from pandas import Timestamp
import warnings
import pandas as pd
from weasyprint import HTML

logger = logging.getLogger(__name__)


def setup_logging():
    pass


def read_data(data_path):
    with open(data_path, "r") as read_file:
        return json.load(read_file)


def generate_standard_profile(
    data_path, profile_name, graph_data, generate_domain=False
):
    data = read_data(data_path)
    builder = html_builder.HTMLBuilder(data, profile_name)

    run_basic_validation(data, builder.profile)

    if generate_domain:
        builder.generate_domain()
    builder.generate_metrics()
    builder.generates_graph(graph_data)
    builder.generate_meta()

    builder.write_html()


def generate_compact_profile(data_path, profile_name, generate_domain=False):
    data = read_data(data_path)
    builder = html_builder.HTMLBuilder(data, profile_name, template="compact")

    run_basic_validation(data, builder.profile)

    if generate_domain:
        builder.generate_domain()
    builder.generate_metrics()
    builder.generate_meta()

    builder.write_html()


def to_pdf(report, out):
    HTML(report).write_pdf(out)

def to_image(report, out):
    pass

# Analysis Methods
def opendc_grid_analysis(
    dc_path, key_path, start: Timestamp, country, out, tz="Europe/Amsterdam"
):
    df_dc = process(dc_path, start, tz)

    analysis = GridAnalysis(df_dc, key_path, country)
    df = analysis.analyze(out, "OpenDC Simulator", "https://opendc.org/")

    return df


if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    # trace = "C:/Users/phili/Documents/University/opendc/output/out.csv"
    trace = "C:/Users/phili/Desktop/output/out.csv"
    start = Timestamp("20181123", tz="Europe/Amsterdam")
    key_path = "G:/My Drive/VU Amsterdam/Year 3/Bachelor Project/entsoe_token.txt"
    res = "result.json"
    df = opendc_grid_analysis(trace, key_path, start, "NL", res)

    df2 = df["DC Consumption"].sum()
    df2 = df2.rename(lambda x: x.replace("dc_cons_", ""))
    df2 = df2 / 1000

    generate_standard_profile(res, "sus_prof", [df2], True)
    to_pdf("report.html", "report.pdf")
