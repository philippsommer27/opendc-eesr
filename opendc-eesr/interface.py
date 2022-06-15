from asyncio.log import logger
from cgitb import html

import html_builder
import json
import logging

logger = logging.getLogger(__name__)

def setup_logging():
    pass

def read_data(data_path):
    with open(data_path, "r") as read_file:
        return json.load(read_file)

def generate_standard_profile(data_path):
    data = read_data(data_path)
    builder = html_builder.HTMLBuilder(data)

    builder.generate_business_related()
    builder.generate_metrics()
    builder.generates_graphs()

    builder.write_html()