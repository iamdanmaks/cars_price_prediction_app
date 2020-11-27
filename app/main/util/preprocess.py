import datetime
import joblib
import numpy as np
import pandas as pd


def preprocess(data):
    result = data
    result['engine_capacity'] = fix_car(
        result['type'],
        result['engine_capacity']
    )
    result['fuel'] = group_rare_fuel(result['fuel'])
    result['gearbox'] = group_rare_gearbox(result['gearbox'])
    result['recency'] = recency(result['registration_year'])
    result['year'] = get_year(result['registration_year'])
    result['decade'] = get_decade(result['registration_year'])
    result['mileage'] = mileage_group(result['mileage'])
    coords = pd.read_csv(
        './app/main/util/state/zipcodes.csv'
    )
    zip_geo_groups = coords[['zipcode', 'group']].set_index('zipcode').to_dict()['group']

    result['geo_group'] = zipcode_group(result['zipcode'], zip_geo_groups, coords)

    del result['registration_year']
    del result['zipcode']

    result = fill_nans(result)
    result = encode_categorical(result)

    return pd.DataFrame({k: [v] for (k, v) in result.items()}).to_numpy()


def check_input(data):
    return check_type(data.get('type')) and check_model(data.get('model')) and \
        check_brand(data.get('brand')) and check_gearbox(data.get('gearbox')) and \
            check_fuel(data.get('fuel')) and check_zipcode(data.get('zipcode')) and \
                check_engine(data.get('engine_capacity')) and check_year(data.get('registration_year')) and \
                    check_power(data.get('power')) and check_mileage(data.get('mileage')) and \
                        check_insurance(data.get('insurance_price'))


def check_type(car_type):
    return car_type in ['bus', 'limousine', 'convertible', 'station wagon',
       'small car', 'coupé', 'other']


def check_model(model):
    return model in ['c4', 'vito', 'mondeo', 'andere', '2_reihe', 'c_klasse', 'a6',
       'twingo', 'golf', 'primera', 'astra', 'ibiza', '3er', 'escort',
       'a_klasse', 'a4', 'e_klasse', 'fabia', 'panda', 'kuga', 'vectra',
       'colt', 'fiesta', 'touran', 'sprinter', 'tigra', 'galant',
       '6_reihe', 'bora', '7er', 'transporter', 'clk', 'slk', 'a3',
       'focus', 'tiguan', 'passat', 'corsa', 'zafira', 'polo', 'megane',
       'clio', '1er', 'clubman', '5_reihe', 'tt', '100', 'berlingo',
       'one', 'fortwo', 'beetle', 'picanto', 'x_reihe', 'kangoo', 'leon',
       'grand', '5er', 'ka', 'caddy', 'a5', 'scirocco', 'up', 'punto',
       'nubira', 'civic', 'octavia', '80', '156', 'galaxy', 'laguna',
       '6er', 'aygo', 'lupo', 'agila', 'v70', 'm_reihe', 'modus',
       'kaefer', '3_reihe', 'c2', 'm_klasse', 'omega', 'q5', 'aveo',
       'almera', 'seicento', 'superb', 'jetta', 'cayenne', 'touareg',
       '911', '850', 'carisma', 'sharan', 'ptcruiser', 'bravo', 'eos',
       'sportage', 'cooper', 'qashqai', 'transit', 'getz', 'sirion', 'a2',
       'a8', 'yaris', 'rio', 'xc_reihe', 'i_reihe', 'wrangler',
       'defender', 'x_trail', 'vivaro', 'swift', 'note', 'combo', 's_max',
       'micra', 'fox', 'sorento', 'z_reihe', 'musa', 'pajero', 'v40',
       'exeo', '1_reihe', 'scenic', 'arosa', 'forester', 'sl', '147',
      'c1', 'kadett', 'crossfire', 'q7', 's_klasse', 'duster',
       'range_rover_sport', '159', 'mx_reihe', 'insignia', 'mustang',
       'phaeton', 'signum', 'rangerover', 'fusion', 'spider', 'yeti',
       'toledo', 'alhambra', 'santa', '4_reihe', 'doblo', 'jazz', 'a1',
       'c3', 'niva', 'captiva', 'corolla', 'meriva', 'antara', 'c5',
       'cherokee', 'cc', 'freelander', 'b_klasse', 'c_max', 'kalina',
       'accord', '500', 's_type', 'cordoba', 'g_klasse', 'discovery',
       'materia', 'ceed', 'cr_reihe', 'boxster', 'ducato', 'roadster',
       'sandero', 'viano', '90', 'calibra', 'avensis', 'espace',
       'outlander', 'stilo', 'lancer', 'forfour', '900', 'croma',
       'cx_reihe', 'ypsilon', 'auris', 'matiz', 'roomster', '601',
       'amarok', 'cuore', 'v50', 'spark', 'q3', '300c', 'r19', 'glk',
       'legacy', 'rx_reihe', '145', 'cl', 'tucson', 'altea', 'verso',
       'kalos', 'carnival', 'jimny', 'move', 's60', 'navara', 'v_klasse',
       'rav', 'citigo', 'voyager', 'charade', 'logan', 'range_rover',
       'c_reihe', 'x_type', 'impreza', 'range_rover_evoque', 'gl', 'v60',
       'lanos', 'terios', '9000', 'lybra', 'mii', 'justy', 'b_max',
       'lodgy', 'juke', 'discovery_sport', 'serie_2', '200', 'delta',
       'i3', 'serie_3', 'elefantino', 'samara', 'kappa', 'other']


def check_brand(brand):
    return brand in ['citroen', 'mercedes_benz', 'ford', 'peugeot', 'audi', 'renault',
       'volkswagen', 'nissan', 'opel', 'seat', 'bmw', 'suzuki', 'skoda',
       'fiat', 'mitsubishi', 'kia', 'sonstige_autos', 'mazda', 'porsche',
       'mini', 'smart', 'toyota', 'jeep', 'hyundai', 'daewoo', 'honda',
       'alfa_romeo', 'saab', 'volvo', 'chevrolet', 'chrysler', 'daihatsu',
       'land_rover', 'lancia', 'subaru', 'dacia', 'rover', 'lada',
       'jaguar', 'trabant']


def check_gearbox(gearbox):
    return gearbox in ['auto', 'manual', 'other']
    

def check_fuel(fuel):
    return fuel in ['gasoline', 'diesel', 'liquefied petroleum gas',
       'compressed natural gas', 'other']


def check_zipcode(zipcode):
    return len(str(zipcode)) == 5 and \
        int(str(zipcode)[:2]) >= 0 and int(str(zipcode)[:2]) <= 99


def check_engine(engine_capacity):
    return engine_capacity is np.nan or (engine_capacity >= 0 and engine_capacity <= 10)


def check_year(year):
    return year >= 1920 and year <= datetime.datetime.now().year


def check_power(power):
    return power >= 0 and power < 25000


def check_mileage(mileage):
    return mileage >= 0


def check_insurance(insurance):
    return insurance is np.nan or insurance >= 0


def fix_car(car_type, engine_capacity):
    if car_type == 'small car' and engine_capacity > 5:
        return np.nan
    elif engine_capacity > 9:
        return np.nan
    elif engine_capacity < 0.5:
        return np.nan
    
    return engine_capacity


def group_rare_fuel(fuel):
    if fuel != 'diesel':
        return 'other'
    return fuel


def group_rare_gearbox(gearbox):
    if gearbox != 'manual':
        return 'other'
    return gearbox


def recency(year):
    today_year = datetime.datetime.now().year
    if year <= 20:
        return today_year - (year + 2000)
    elif year > 20 and year < 100:
        return today_year - (year + 1900)
    else:
        return today_year - year


def get_year(year):
    if year <= 20:
        return (year + 2000) % 10
    elif year > 20 and year < 100:
        return (year + 1900) % 10
    else:
        return year % 10


def get_decade(year):
    if year <= 20:
        return (year + 2000) % 100
    elif year > 20 and year < 100:
        return (year + 1900) % 100
    else:
        return year % 100


def mileage_group(mileage):
    if mileage <= 30000:
        return 0 #low
    elif mileage > 30000 and mileage <= 60000:
        return 1 #less than average
    elif mileage > 60000 and mileage <= 80000:
        return 2 #average
    elif mileage > 80000 and mileage <= 120000:
        return 3 #more than average
    else:
        return 4 #high


def zipcode_group(zipcode, zip_geo_groups, coords):
    if zip_geo_groups.get(zipcode):
        return zip_geo_groups.get(zipcode)
    else:
        for i, z in enumerate(coords['zipcode']):
            if abs(z - int(zipcode)) < 50:
                return coords['group'][i]


def fill_nans(data):
    if data['type'] == np.nan or data['type'] == None:
        data['type'] = 'other'
    if data['damage'] == np.nan or data['damage'] == None:
        data['damage'] = -1
    if data['model'] == np.nan or data['model'] == None:
        data['model'] = 'other'
    if data['engine_capacity'] == np.nan or data['engine_capacity'] == None:
        data['engine_capacity'] = -1
    if data['insurance_price'] == np.nan or data['insurance_price'] == None:
        data['insurance_price'] = -1
    return data


def encode_categorical(data):
    cat_features = ["type", "model", "brand", "gearbox", "fuel"]
    for cat_feature in cat_features:
        le = joblib.load(f'./app/main/util/state/label_encoder_{cat_feature}.pkl')
        data[cat_feature] = le.transform(np.array([data[cat_feature]]))[0]
    return data
