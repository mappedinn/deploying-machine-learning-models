import json

from regression_model.config import config
from regression_model.processing.data_management import load_dataset

from api.config import get_logger
_logger = get_logger(logger_name=__name__)


def test_prediction_endpoint_validation_200(flask_test_client):
    # Given
    # Load the test data from the regression_model package.
    # This is important as it makes it harder for the test
    # data versions to get confused by not spreading it
    # across packages.
    test_data = load_dataset(file_name=config.TESTING_DATA_FILE)
    post_json = test_data[1:100].to_json(orient='records')
    
    # When
    # _logger.error(f'TTTTTT type(json.loads(post_json)): {type(json.loads(post_json))}')
    response = flask_test_client.post('/v1/predict/regression',json=json.loads(post_json))
    # response = flask_test_client.post('/v1/predict/regression',json=post_json)

    # Then
    assert response.status_code == 200
    response_json = json.loads(response.data)
    # print(f'FINAL FINAL response_json = {response_json}')
    # print(f'FINAL FINAL response_json.get("predictions") = {response_json.get("predictions")}')
    # _logger.error(f'FINAL FINAL response_json.get("errors") = {response_json.get("errors")}')

    # Check correct number of errors removed
    if response_json.get('errors') == None:
        assert len(response_json.get('predictions'))  == len(test_data[1:100])
    else: 
        assert len(response_json.get('predictions')) + len(response_json.get('errors')) == len(test_data[1:100])
    
    # assert len(response_json.get('predictions')) + len(response_json.get('errors')) == len(test_data[1:10])
