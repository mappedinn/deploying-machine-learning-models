from flask import Blueprint, request, jsonify
from regression_model.predict import make_prediction

from api.config import get_logger
from api.validation import validate_inputs
_logger = get_logger(logger_name=__name__)

from regression_model import __version__ as _version
from api import __version__ as api_version

import json

prediction_app = Blueprint('prediction_app', __name__)

@prediction_app.route('/', methods=['GET'])
@prediction_app.route('/health', methods=['GET'])
def health():
    if request.method == 'GET':
        _logger.info('health status OK')
        return 'ok'


@prediction_app.route('/version', methods=['GET'])
def version():
    if request.method == 'GET':
        return jsonify({'model_version': _version,
                        'api_version': api_version})

@prediction_app.route('/v1/predict/regression', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Step 1: Extract POST data from request body as JSON
        json_data = request.get_json()
        _logger.info(f'request.get_json() returns a dict,  type(json_data) : {type(json_data)}')

        # Step 2: Validate the input using marshmallow schema
        # _logger.error(f'json_data={json_data}')
        input_data, errors = validate_inputs(input_data=json.dumps(json_data))
        
        # Step 3: Model prediction
        result = make_prediction(input_data=input_data)

        # Step 4: Convert numpy ndarray to list
        predictions = result.get('predictions').tolist()
        version = result.get('version')
        _logger.debug(json.dumps({'predictions': predictions,
                        'version': version,
                        'errors': errors}))

        # Step 5: Return the response as JSON
        return json.dumps({'predictions': predictions,
                        'version': version,
                        'errors': errors})