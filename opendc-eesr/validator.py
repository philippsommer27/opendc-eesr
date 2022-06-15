import jsonschema
import logging
import json

from pip import main

logger = logging.getLogger(__name__)

'''Validates that metric results input matches expected. '''
def validate_data_in(data):
    schema="library\schemas\metrics_input_schema.json"
    jsonschema.validate(data, schema)

def check_profile_data_completeness(data, profile_name):
    pass

def validate_custom_profile(profile):
    schema = "library\profiles\schemas\profile_schema.json"
    jsonschema.validate(profile, schema)

if __name__ == "__main__":
    pass