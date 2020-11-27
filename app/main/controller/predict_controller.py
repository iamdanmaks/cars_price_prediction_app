from flask import request
from flask_restplus import Resource

from ..util.dto import PredictDto
from ..service.predict_service import make_prediction

api = PredictDto.api
_predict = PredictDto.predict


@api.route('/')
class Predict(Resource):
    @api.response(201, 'Price successfully predicted.')
    @api.doc('create a new prediction')
    @api.expect(_predict, validate=True)
    def post(self):
        """Predict car price """
        data = request.json
        return make_prediction(data=data)
