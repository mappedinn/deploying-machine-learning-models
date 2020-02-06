from flask import Blueprint, request
from api.config import get_logger

_logger = get_logger(logger_name=__name__)

prediction_app = Blueprint('prediction_app', __name__)

@prediction_app.route('/', methods=['GET'])
def home():
    if request.method == 'GET':
        return 'Landing page of the ML API'

@prediction_app.route('/health', methods=['GET'])
def health():
    if request.method == 'GET':
        _logger.info('health status OK')
        return 'ok'
