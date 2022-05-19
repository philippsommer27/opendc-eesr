from cgitb import html
import html_builder
import json

def read_data(path):
    with open("test/test_values.json", "r") as read_file:
        return json.load(read_file)

def generate_standard_profile(data_path):
    data = read_data(data_path)
    
    page = html_builder.read_template()

    html_builder.insert_metrics(page, data)
    html_builder.insert_business_related(page, data)
    html_builder.insert_visuals(page, data)

    html_builder.write_html(page)