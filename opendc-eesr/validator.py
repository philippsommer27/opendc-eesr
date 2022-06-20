import jsonschema
import logging
from util import load_json

logger = logging.getLogger(__name__)

class MissingMetricsError(Exception):

    def __init__(self, missing, *args: object) -> None:
        super().__init__(*args)
        self.missing = missing

    def __str__(self) -> str:
        return f"Input is missing the following metrics required by the profile {self.missing}"

'''Validates that metric results input matches expected. '''
def validate_data_in(data):
    schema= load_json("library\schemas\metrics_input_schema.json")
    jsonschema.validate(data, schema)

'''Validate that the given input contains required values by profile'''
def validate_data_to_profile(data, profile):
    missing = []

    for metric in profile['builtin_metrics']:
        if metric not in data['builtin_metrics']:
            missing.append(metric)

    if 'additional_metrics' in profile:
        for metric in profile['additional_metrics']:
            if metric not in data['additional_metrics']:
                missing.append(metric)
    
    if len(missing) > 0:
        raise MissingMetricsError(missing)

    
def validate_custom_profile(profile):
    schema = load_json("library\profiles\schemas\profile_schema.json")
    jsonschema.validate(profile, schema)

def run_basic_validation(data, profile):
    validate_data_in(data)
    validate_data_to_profile(data, profile)