from operator import index
from reporting import run_basic_validation, html_builder, grapher
from analysis import GridAnalysis, process
import json
import logging
from util import inline
from pandas import Timestamp
import warnings
import pdfkit
import pandas as pd

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
    pdfkit.from_file(report, out)


# Analysis Methods
def opendc_grid_analysis(
    dc_path, key_path, offset, start: Timestamp, end: Timestamp, country, out
):
    df_dc = process(dc_path, offset)

    analysis = GridAnalysis(df_dc, start, end, key_path, country)
    df = analysis.analyze(out, "OpenDC Simulator", "https://opendc.org/")

    return df


if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    # trace = "C:/Users/phili/Documents/University/opendc/output/out.csv"
    trace = "C:/Users/phili/Desktop/output/out.csv"
    offset = "20181123"
    start = Timestamp("20181123", tz="Europe/Amsterdam")
    end = Timestamp("20190212", tz="Europe/Amsterdam")
    key_path = "G:/My Drive/VU Amsterdam/Year 3/Bachelor Project/entsoe_token.txt"
    res = "result.json"
    df = opendc_grid_analysis(trace, key_path, offset, start, end, "NL", res)

    df2 = df["DC Consumption"].sum()
    df2 = df2.rename(lambda x: x.replace("dc_cons_", ""))
    df2 = df2 / 1000

    generate_standard_profile(res, "sus_prof", [df2], True)
    to_pdf("report.html", "report.pdf")
