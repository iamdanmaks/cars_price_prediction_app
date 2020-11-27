from flask import current_app
from flask_restplus import Resource

from ..util.dto import VersionDto

api = VersionDto.api


@api.route('/')
class Version(Resource):
    @api.response(200, 'Version successfully returned.')
    @api.doc('return model and package versions')
    def get(self):
        """Return model and package versions """
        return {
            "model": current_app.config['MODEL_VERSION'],
            "package": current_app.config['PACKAGE_VERSION']
        }, 200
