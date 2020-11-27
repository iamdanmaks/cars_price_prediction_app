import joblib
import pandas as pd

from flask import Flask
from flask_cors import CORS

from .config import config_by_name
from .util.model import load_model


model = load_model()
cors = CORS()
coords = pd.read_csv(
        './app/main/util/state/zipcodes.csv'
    )
zip_geo_groups = coords[['zipcode', 'group']].set_index('zipcode').to_dict()['group']

les = []
cat_features = ["type", "model", "brand", "gearbox", "fuel"]
for cat_feature in cat_features:
    les.append(joblib.load(f'./app/main/util/state/label_encoder_{cat_feature}.pkl'))


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    
    cors.init_app(app, resources={r"/api/v1/*": {"origins": "*"}})

    return app
