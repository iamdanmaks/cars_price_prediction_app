import joblib
import numpy as np


def load_model():
    return joblib.load('./app/main/util/state/model.pkl')


def predict(model, car_vec):
    return np.exp(model.predict(car_vec))
