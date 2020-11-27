import joblib


def load_model():
    return joblib.load('./app/main/util/state/model.pkl')


def predict(model, car_vec):
    print('\n', 2.1, '\n')
    return model.predict(car_vec)
