import os
import unittest

from flask_script import Manager

from app.main import create_app
from app import blueprint, index


app = create_app('prod')
app.register_blueprint(blueprint)

app.app_context().push()
app.add_url_rule('/', 'index', view_func=index)
