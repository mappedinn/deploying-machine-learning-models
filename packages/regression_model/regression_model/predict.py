import numpy as np
import pandas as pd

from regression_model.processing.data_management import load_pipeline
from regression_model.config import config
from regression_model.processing.validation import validate_inputs
from regression_model import __version__ as _version

import json

from regression_model.config import logging_config
_logger = logging_config.get_logger(__name__)

pipeline_file_name = f'{config.PIPELINE_SAVE_FILE}{_version}.pkl'
_price_pipe = load_pipeline(file_name=pipeline_file_name)


def make_prediction(*, input_data) -> dict:
    """Make a prediction using the saved model pipeline."""
    _logger.info('make_prediction started.............')
    # _logger.error(f'make_prediction iS HERE............{input_data}')
    # data = pd.read_json(input_data)
    # _logger.error(f'--------make_prediction() json.dumps(data) = {json.dumps(input_data)}')
    _logger.info(f'pd.read_json(json.dumps(input_data)).shape = {pd.read_json(json.dumps(input_data)).shape}')
    validated_data = validate_inputs(input_data=pd.read_json(json.dumps(input_data)))
    prediction = _price_pipe.predict(validated_data[config.FEATURES])
    output = np.exp(prediction)

    results = {'predictions': output, 'version': _version}
    _logger.info(f'make_prediction(): {results}')
    _logger.info('make_prediction ended.............')
    return results
