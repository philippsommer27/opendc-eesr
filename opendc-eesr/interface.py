from reporting import run_basic_validation, html_builder
import json
import logging
from util import inline

logger = logging.getLogger(__name__)

def setup_logging():
    pass

def read_data(data_path):
    with open(data_path, "r") as read_file:
        return json.load(read_file)

def generate_standard_profile(data_path, profile_name, domain=False):
    data = read_data(data_path)
    builder = html_builder.HTMLBuilder(data, profile_name)

    run_basic_validation(data, builder.profile)

    if domain : builder.generate_domain()
    builder.generate_metrics()
    builder.generates_graphs()
    builder.generate_meta()

    builder.write_html()

if __name__ == '__main__':
    generate_standard_profile('test/test_values.json', "std_prof", domain=True)
    inline()