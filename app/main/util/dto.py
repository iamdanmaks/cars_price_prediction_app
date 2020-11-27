from flask_restplus import Namespace, fields


class PredictDto:
    api = Namespace('predict', description='predict related operations')
    predict_data = api.model('predict_data', {
        'engine_capacity': fields.String(required=True, description='car engine capacity'),
        'type': fields.String(required=True, description='car type'),
        'registration_year': fields.Integer(required=True, description='car registration year'),
        'gearbox': fields.String(required=True, description='car gearbox'),
        'power': fields.Integer(required=True, description='car power'),
        'model': fields.String(required=True, description='car model'),
        'mileage': fields.Integer(required=True, description='car mileage'),
        'fuel': fields.String(required=True, description='car fuel'),
        'brand': fields.String(required=True, description='car brand'),
        'damage': fields.Boolean(required=True, description='car damage'),
        'zipcode': fields.String(required=True, description='car zipcode'),
        'insurance_price': fields.String(required=True, description='car insurance price')
    })
    predict = api.model('predict', {
        'data': fields.Nested(predict_data)
    })


class VersionDto:
    api = Namespace('version', desription='model and package versions related operations')
