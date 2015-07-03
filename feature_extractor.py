import pandas as pd
import os

class FeatureExtractor(object):
    def __init__(self):
        pass

    def fit(self, X_df, y_array):
        pass

    def transform(self, X_df):
        X_encoded = X_df
        path = os.path.dirname(__file__)
        data_weather = pd.read_csv(os.path.join(path, "data_weather.csv"))
        X_weather = data_weather[['Date', 'AirPort', 'Max TemperatureC']]
        X_encoded = X_encoded.merge(X_weather, how='left',
            left_on=['DateOfDeparture', 'Arrival'], 
            right_on=['Date', 'AirPort'], sort=False)
         
        X_encoded = X_encoded.join(pd.get_dummies(X_encoded['Departure'], prefix='d'))
        X_encoded = X_encoded.join(pd.get_dummies(X_encoded['Arrival'], prefix='a'))
        X_encoded = X_encoded.drop(['Arrival', 'Departure', 
            'DateOfDeparture', 'Date', 'AirPort'], axis=1)

        X_array = X_encoded.values
        return X_array