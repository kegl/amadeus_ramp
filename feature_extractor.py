import pandas as pd
import os


class FeatureExtractor(object):
    def __init__(self):
        pass
    
    def quarter(self, m):
        if m <= 3:
            return 1
        elif m <= 6:
            return 2
        elif m <= 9:
            return 3
        return 4

    def fit(self, X_df, y_array):
        pass

    def transform(self, X_df):
              
        #uncomment the line below in the submission
        path = os.path.dirname(__file__)
        X_encoded = X_df
        
        #data_holidays = pd.read_csv("data_holidays_3.csv")
        data_holidays = pd.read_csv(os.path.join(path, "data_holidays_3.csv"))
        X_holidays = data_holidays[['DateOfDeparture','Holy','around_holy']]
        X_encoded = X_encoded.merge(X_holidays, how='left', left_on=['DateOfDeparture'], right_on=['DateOfDeparture'], sort=False)

        #data_distance = pd.read_csv("data_distance.csv")
        data_distance = pd.read_csv(os.path.join(path, "data_distance.csv"))
        X_distance = data_distance[['Departure','Arrival','Distance']]
        X_encoded = X_encoded.merge(X_distance, how='left', left_on=['Departure','Arrival'], right_on=['Departure','Arrival'], sort=False)

        X_encoded['DateOfDeparture'] = pd.to_datetime(X_encoded['DateOfDeparture'])
        X_encoded['year'] = X_encoded['DateOfDeparture'].dt.year
        X_encoded['weekday'] = X_encoded['DateOfDeparture'].dt.weekday
        X_encoded['week'] = X_encoded['DateOfDeparture'].dt.week
        X_encoded['month'] = X_encoded['DateOfDeparture'].dt.month
        X_encoded['day'] = X_encoded['DateOfDeparture'].dt.day
        X_encoded['quarter'] = X_encoded['month'].apply(lambda m: self.quarter(m))
        X_encoded['n_days'] = X_encoded['DateOfDeparture'].apply(lambda date: (date - pd.to_datetime("1970-01-01")).days)
        
        #data_fares = pd.read_csv("data_fares_2.csv")
        data_fares = pd.read_csv(os.path.join(path, "data_fares_2.csv"))
        X_fares = data_fares[['Departure','Arrival','quarter','year','Avgfares']]
        X_encoded = X_encoded.merge(X_fares, how='left', left_on=['Departure','Arrival','quarter','year'], right_on=['Departure','Arrival','quarter','year'], sort=False)

        X_encoded = X_encoded.join(pd.get_dummies(X_encoded['year'], prefix='y'))
        X_encoded = X_encoded.join(pd.get_dummies(X_encoded['weekday'], prefix='wd'))
        X_encoded = X_encoded.join(pd.get_dummies(X_encoded['week'], prefix='w'))      
        X_encoded = X_encoded.join(pd.get_dummies(X_encoded['Departure'], prefix='d'))
        X_encoded = X_encoded.join(pd.get_dummies(X_encoded['Arrival'], prefix='a'))      
            
        X_encoded = X_encoded.drop('Departure', axis=1)
        X_encoded = X_encoded.drop('Arrival', axis=1)     
        X_encoded = X_encoded.drop('weekday', axis=1)
        X_encoded = X_encoded.drop('week', axis=1)
        X_encoded = X_encoded.drop('year', axis=1)
        X_encoded = X_encoded.drop('month', axis=1)
        X_encoded = X_encoded.drop('day', axis=1)
        X_encoded = X_encoded.drop('quarter', axis=1)
        X_encoded = X_encoded.drop('std_wtd', axis=1)
        X_encoded = X_encoded.drop('WeeksToDeparture', axis=1)        
        X_encoded = X_encoded.drop('DateOfDeparture', axis=1) 
                                    
        X_array = X_encoded.values
        return X_array