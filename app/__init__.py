from flask_restplus import Api
from flask import Blueprint

from .main.controller.predict_controller import api as predict_ns
from .main.controller.version_controller import api as version_ns
from .main.controller.predict_ui import index


blueprint = Blueprint(
    'api', 
    __name__,
    url_prefix='/api/v1'
)

ui_blueprint = Blueprint(
    'ui',
    __name__
)

api = Api(blueprint,
          title='Car Price Prediction Service',
          version='1.0',
          description='Car price prediction api and service'
          )

api.add_namespace(predict_ns, path='/predict')
api.add_namespace(version_ns, path='/version')
